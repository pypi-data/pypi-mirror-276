import math
import time
import warnings
from functools import partial
from typing import Tuple, Callable, Optional, Literal, Any

import fjformer
import jax
from chex import Array
from fjformer import with_sharding_constraint
from .easydel_modelling_utils import EasyDeLPretrainedConfig
from ..etils.partition_module import PartitionAxis

try:
    from jax.experimental.pallas.ops.tpu.flash_attention import flash_attention as tpu_flash_attention
    from jax.experimental.pallas.ops.tpu.flash_attention import BlockSizes as BlockSizesFlashAttn

except (ModuleNotFoundError, ImportError) as e:
    from fjformer.pallas_operations.tpu_flash_attention.tpu import flash_attention as tpu_flash_attention
    from fjformer.pallas_operations.tpu_flash_attention.tpu import BlockSizes as BlockSizesFlashAttn
from fjformer.pallas_operations.ring_attention import ring_flash_attention_tpu

try:
    from jax.experimental.pallas.ops.tpu.splash_attention import (
        make_splash_mha,
        CausalMask,
        MultiHeadMask,
        SegmentIds
    )
    from jax.experimental.pallas.ops.tpu.splash_attention import BlockSizes as BlockSizesSplashAttn
except (ModuleNotFoundError, ImportError) as e:
    from fjformer.pallas_operations.splash_attention import (
        make_splash_mha,
        CausalMask,
        MultiHeadMask,
        SegmentIds,
        BlockSizes as BlockSizesSplashAttn
    )  # doesn't work on jax version 0.4.28
from flax.linen.dtypes import promote_dtype
from flax.struct import dataclass
from jax import numpy as jnp, lax, random
from jax.experimental.shard_map import shard_map
from jax.sharding import PartitionSpec, Mesh
from fjformer.pallas_operations import flash_attention
from ._vanilla_attention import (
    vanilla_attention,
    shard_vanilla_attention
)
from ._ring_attention import (
    ring_attention_standard,
    wise_ring_attention,
)
from ._blockwise_attention import blockwise_attn
from .flax_modelling_utils import get_gradient_checkpoint_policy
from ..etils.etils import get_logger

logger = get_logger(__name__)

# DEFAULT VALUES ...

DEFAULT_K_BLOCK = 512
DEFAULT_Q_BLOCK = 512
DEFAULT_QPS = PartitionSpec(("dp", "fsdp"), "sp", "tp", None)
DEFAULT_KPS = PartitionSpec(("dp", "fsdp"), "sp", "tp", None)
DEFAULT_VPS = PartitionSpec(("dp", "fsdp"), "sp", "tp", None)
DEFAULT_BPS = PartitionSpec(("dp", "fsdp"), None, "sp", None)
DEFAULT_APS = PartitionSpec(("dp", "fsdp"), "sp", "tp", None)
DEFAULT_G_QPS = PartitionSpec(("dp", "fsdp"), None, "tp", None)
DEFAULT_G_BPS = PartitionSpec(("dp", "fsdp"), None, None, None)
DEFAULT_G_APS = PartitionSpec(("dp", "fsdp"), None, "tp", None)


@dataclass
class AttentionOutput:
    attention_weights: Optional[Array] = None
    attention_outputs: Optional[Array] = None


def combine_flash_masks(causal_mask, segment_ids):
    causal_mask = causal_mask.astype(jnp.bool_)
    if causal_mask.ndim == 2:
        query_sequence_length, key_sequence_length = causal_mask.shape
        causal_mask = causal_mask.reshape(1, 1, query_sequence_length, key_sequence_length)
    elif causal_mask.ndim == 4:
        *_, query_sequence_length, key_sequence_length = causal_mask.shape
    else:
        raise ValueError("unexpected shape for `causal_mask`")
    if segment_ids.ndim == 2:
        b, seq_query_sequence_length = segment_ids.shape
        seq_key_sequence_length = seq_query_sequence_length
    elif segment_ids.ndim == 4:
        b, _, _, seq_key_sequence_length = segment_ids.shape
        seq_query_sequence_length = seq_key_sequence_length
        segment_ids = segment_ids[:, 0, -1]  # taking final mask
    else:
        raise ValueError("unexpected shape for `segment_ids`")

    assert seq_query_sequence_length == query_sequence_length, (
        "`segment_ids` and `causal_mask` don't have same query axis length"
    )
    assert seq_key_sequence_length == key_sequence_length, (
        "`segment_ids` and `causal_mask` don't have same key/value axis length"
    )
    assert segment_ids.ndim == 2, f"`segment_ids` don't have excepted shape {segment_ids.shape}"
    segment_ids = jnp.expand_dims(
        ~jnp.equal(
            jnp.expand_dims(segment_ids, axis=2),
            jnp.expand_dims(segment_ids, axis=1)
        ).astype(jax.numpy.bool_),
        1
    )
    return jnp.logical_or(~causal_mask, segment_ids)


def get_flash_attention() -> Tuple[Callable, bool, bool]:
    """return: FlashAttention FN, Upcast Needed to float32,do_shard_map"""
    platform = jax.lib.xla_bridge.get_backend().platform
    if platform == "gpu":
        warnings.warn("for GPU backend use `cudnn` or `pallas_flash`")
        float32_logits = False
        ring_attention_fn = flash_attention
        do_shard_map = True
    elif platform == "tpu":
        float32_logits = True
        ring_attention_fn = tpu_flash_attention
        do_shard_map = False
    else:
        raise ValueError(f"Unsupported platform {platform}")

    return ring_attention_fn, float32_logits, do_shard_map


def set_attrs_smartly_with_prp(self, attr_name: str, default: Any, new_attr: Any, prp: EasyDeLPretrainedConfig = None):
    if not hasattr(self, attr_name) or getattr(self, attr_name, ...) == Ellipsis:
        setattr(self, attr_name, default if prp is None else getattr(prp, attr_name))
    if not new_attr == Ellipsis:
        setattr(self, attr_name, new_attr)


class AttentionModule:
    """
    Manages different attention mechanisms for efficient computation in EasyDeL models.

    This class serves as a central hub for handling various attention mechanisms, including
    optimized implementations like FlashAttention, SplashAttention, RingAttention, and more traditional
    approaches like vanilla (dot-product) attention. It provides a unified interface to
    select and execute the appropriate attention mechanism based on the model's configuration and
    hardware platform.

    Key Features:

    * **Attention Mechanism Selection:** Supports a wide range of attention mechanisms,
      allowing users to choose the most suitable option based on performance and hardware constraints.
    * **Sharding and Partitioning:** Integrates with JAX's sharding capabilities, enabling efficient
      distribution of computations and data across multiple devices.
    * **Block-wise Computation:** Implements block-wise attention computations for optimized memory
      usage and speed, particularly beneficial for large models.
    * **Performance Optimization:** Includes support for highly optimized implementations like
      FlashAttention, SplashAttention, and RingAttention for TPU and GPU acceleration.
    * **Flexibility and Customization:** Offers fine-grained control over attention parameters,
      sharding specifications, and block sizes, providing flexibility for different use cases.
    * **Testing and Evaluation:** Includes a `test_attentions` method to systematically evaluate
      different attention mechanisms and help users identify the best-performing option.

    Example Usage:

    ```python
    # Initialize an AttentionModule instance
    attention_module = AttentionModule(
        mesh=mesh,
        attn_mechanism="ring",  # Select the desired attention mechanism
        sm_scale=1.0 / math.sqrt(head_dim),
        num_attention_heads=num_heads,
        head_dims=head_dim,
        # ... other configuration parameters ...
    )

    # Compute attention outputs
    attention_output = attention_module(
        query_states=query_states,
        key_states=key_states,
        value_states=value_states,
        # ... other attention inputs ...
    )

    # Access attention outputs
    attention_outputs = attention_output.attention_outputs
    attention_weights = attention_output.attention_weights
    ```
    The AttentionModule class is a crucial component within EasyDeL, responsible for managing and optimizing attention
    computations. It provides a user-friendly way to select and execute different attention mechanisms,
    leveraging JAX's sharding capabilities and offering performance enhancements through specialized implementations
     like FlashAttention and SplashAttention. Its ability to handle block-wise computations and customization options
      makes it adaptable to a variety of model architectures and hardware configurations.

    Attributes:
        mesh (Mesh): JAX mesh for device distribution.
        attn_mechanism (str): The selected attention mechanism.
        sm_scale (float): Scaling factor for attention scores.
        num_attention_heads (int): Number of attention heads.
        head_dims (int): Dimensionality of each attention head.
        # ... other attributes for block sizes, partitioning, dropout, etc. ...
    """

    def __init__(
            self,
            mesh: Mesh,
            attn_mechanism: Literal[
                "vanilla",
                "flash",
                "splash",
                "ring",
                "cudnn",
                "local_ring",
                "sharded_vanilla",
                "legacy_sharded_vanilla",
                "wise_ring",
                "blockwise",
                "pallas_flash"
            ],
            sm_scale: float,
            num_attention_heads: int,
            head_dims: int,
            block_k: int = ...,
            block_q: int = ...,
            block_b: int = ...,
            block_k_major: int = ...,
            block_q_major_dkv: int = ...,
            block_k_major_dkv: int = ...,
            block_k_dkv: int = ...,
            block_q_dkv: int = ...,
            block_k_major_dq: int = ...,
            block_k_dq: int = ...,
            block_q_dq: int = ...,
            partition_axis: PartitionAxis = ...,
            scan_ring_attention: bool = ...,
            scan_attention_layers: bool = ...,
            attention_dropout: float = 0.0,
            dtype: jnp.dtype = jnp.float32,
            precision: lax.Precision = ...,
            force_float32_tpu: bool = ...,
            shard_attention_computation: bool = ...,
            use_sharding_constraint: Optional[bool] = ...,
            axis_name: str = ...,
            backward_pass_impl: Literal["triton", "xla"] = "triton",
            base_module_class: Optional[EasyDeLPretrainedConfig] = None,
            _do_check: bool = True
    ):

        self.block_k: int = ...
        self.block_q: int = ...
        self.block_b: int = ...
        self.block_k_major: int = ...
        self.block_q_major_dkv: int = ...
        self.block_k_major_dkv: int = ...
        self.block_k_dkv: int = ...
        self.block_q_dkv: int = ...
        self.block_k_major_dq: int = ...
        self.block_k_dq: int = ...
        self.block_q_dq: int = ...
        self.partition_axis: PartitionAxis = ...
        self.scan_ring_attention: bool = ...
        self.precision: lax.Precision = ...
        self.force_float32_tpu: bool = ...
        self.shard_attention_computation: bool = ...
        self.use_sharding_constraint: Optional[bool] = ...
        self.axis_name: str = ...
        set_attrs_smartly_with_prp(self, "use_sharding_constraint", False, use_sharding_constraint, base_module_class)
        set_attrs_smartly_with_prp(self, "block_k_major", DEFAULT_K_BLOCK, block_k_major, base_module_class)
        set_attrs_smartly_with_prp(self, "block_b", 1, block_b, base_module_class)
        set_attrs_smartly_with_prp(self, "block_q", DEFAULT_Q_BLOCK, block_q, base_module_class)
        set_attrs_smartly_with_prp(self, "block_k", DEFAULT_K_BLOCK, block_k, base_module_class)
        set_attrs_smartly_with_prp(self, "block_q_major_dkv", DEFAULT_Q_BLOCK, block_q_major_dkv, base_module_class)
        set_attrs_smartly_with_prp(self, "block_k_major_dkv", DEFAULT_K_BLOCK, block_k_major_dkv, base_module_class)
        set_attrs_smartly_with_prp(self, "block_k_major_dq", DEFAULT_K_BLOCK, block_k_major_dq, base_module_class)
        set_attrs_smartly_with_prp(self, "block_k_dkv", DEFAULT_K_BLOCK, block_k_dkv, base_module_class)
        set_attrs_smartly_with_prp(self, "block_q_dkv", DEFAULT_Q_BLOCK, block_q_dkv, base_module_class)
        set_attrs_smartly_with_prp(self, "block_q_dq", DEFAULT_Q_BLOCK, block_q_dq, base_module_class)
        set_attrs_smartly_with_prp(self, "block_k_dq", DEFAULT_K_BLOCK, block_k_dq, base_module_class)
        set_attrs_smartly_with_prp(self, "shard_attention_computation", True, shard_attention_computation,
                                   base_module_class)
        set_attrs_smartly_with_prp(self, "scan_ring_attention", True, scan_ring_attention, base_module_class)
        set_attrs_smartly_with_prp(self, "partition_axis", PartitionAxis(), partition_axis, base_module_class)
        set_attrs_smartly_with_prp(self, "precision", lax.Precision("fastest"), precision)  # DON'T READ FROM CONFIG
        set_attrs_smartly_with_prp(self, "force_float32_tpu", True, force_float32_tpu)  # DON'T READ FROM CONFIG
        set_attrs_smartly_with_prp(self, "axis_name", "sp", axis_name)  # DON'T READ FROM CONFIG

        self.mesh = mesh
        self.attn_mechanism = attn_mechanism
        self.platform = jax.lib.xla_bridge.get_backend().platform
        self.sm_scale = sm_scale
        self.num_attention_heads = num_attention_heads
        self.head_dims = head_dims

        self.scan_attention_layers = scan_attention_layers
        self.attention_dropout = attention_dropout
        self.dtype = dtype
        self.backward_pass_impl = backward_pass_impl
        self._do_check = _do_check
        if attn_mechanism == "splash" and self.platform != "tpu":
            raise OSError("splash attention is only supported on TPU.")
        if attn_mechanism == "flash" and self.platform != "tpu":
            error_msg = "flash attention is only supported on TPU"
            if self.platform == "gpu":
                error_msg += ", for GPUs flash attention you can use `cudnn`."
            raise OSError(error_msg)
        if attn_mechanism == "cudnn" and self.platform != "gpu":
            raise OSError("flash attention is only supported on GPU.")

    def get_block_size_splash_attn(self, q_seq, k_seq):
        return BlockSizesSplashAttn(
            block_q=min(self.block_q, q_seq),
            block_kv_compute=min(self.block_k, k_seq),
            block_kv=min(self.block_k, k_seq),
            block_q_dkv=min(self.block_q_dkv, q_seq),
            block_kv_dkv=min(self.block_k_dkv, k_seq),
            block_kv_dkv_compute=min(self.block_k_dkv, k_seq),
            block_q_dq=min(self.block_q_dq, q_seq),
            block_kv_dq=min(self.block_k_dq, k_seq),
        )

    def get_block_size_flash_attn(self, q_seq, k_seq):
        return BlockSizesFlashAttn(
            block_q=min(self.block_q, q_seq),
            block_k=min(self.block_k, k_seq),
            block_q_dkv=min(self.block_q_dkv, q_seq),
            block_k_dq=min(self.block_k_dkv, k_seq),
            block_k_dkv=min(self.block_k_dkv, k_seq),
            block_q_dq=min(self.block_q_dq, q_seq),
            block_b=min(self.block_b, 1),
            block_k_major=min(self.block_k_major, k_seq),
            block_k_major_dq=min(self.block_k_major_dq, k_seq),
            block_k_major_dkv=min(self.block_k_major_dkv, k_seq),
            block_q_major_dkv=min(self.block_q_major_dkv, q_seq)
        )

    def get_bshd_partition_specs(self, query_sequence_length) -> Tuple[
        PartitionSpec,
        PartitionSpec,
        PartitionSpec,
        PartitionSpec,
        PartitionSpec,
        bool
    ]:
        is_generating = query_sequence_length == 1
        if is_generating:
            query_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.query_sequence_axis,
                self.partition_axis.head_axis,
                self.partition_axis.attention_dim_axis,
            )
            key_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.key_sequence_axis,
                self.partition_axis.head_axis,
                self.partition_axis.attention_dim_axis,
            )
            value_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.key_sequence_axis,
                self.partition_axis.head_axis,
                self.partition_axis.attention_dim_axis,
            )
            bias_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.bias_head_sequence_axis,
                self.partition_axis.query_sequence_axis,
                self.partition_axis.bias_key_sequence_axis
            )
            attention_partition_spec = query_partition_spec
        else:

            query_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.generation_query_sequence_axis,
                self.partition_axis.head_axis,
                self.partition_axis.attention_dim_axis,
            )
            key_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.generation_key_sequence_axis,
                self.partition_axis.head_axis,
                self.partition_axis.attention_dim_axis,
            )
            value_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.generation_key_sequence_axis,
                self.partition_axis.head_axis,
                self.partition_axis.attention_dim_axis,
            )
            bias_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.bias_head_sequence_axis,
                self.partition_axis.generation_query_sequence_axis,
                self.partition_axis.bias_key_sequence_axis
            )
            attention_partition_spec = query_partition_spec
        return (
            query_partition_spec,
            key_partition_spec,
            value_partition_spec,
            bias_partition_spec,
            attention_partition_spec,
            is_generating
        )

    def get_bhsd_partition_specs(self, query_sequence_length) -> Tuple[
        PartitionSpec,
        PartitionSpec,
        PartitionSpec,
        PartitionSpec,
        PartitionSpec,
        bool
    ]:
        is_generating = query_sequence_length == 1
        if is_generating:
            query_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.head_axis,
                self.partition_axis.query_sequence_axis,
                self.partition_axis.attention_dim_axis,
            )
            key_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.head_axis,
                self.partition_axis.key_sequence_axis,
                self.partition_axis.attention_dim_axis,
            )
            value_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.head_axis,
                self.partition_axis.key_sequence_axis,
                self.partition_axis.attention_dim_axis,
            )
            bias_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.bias_head_sequence_axis,
                self.partition_axis.query_sequence_axis,
                self.partition_axis.bias_key_sequence_axis
            )
            attention_partition_spec = query_partition_spec
        else:

            query_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.head_axis,
                self.partition_axis.generation_query_sequence_axis,
                self.partition_axis.attention_dim_axis,
            )
            key_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.head_axis,
                self.partition_axis.generation_key_sequence_axis,
                self.partition_axis.attention_dim_axis,
            )
            value_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.head_axis,
                self.partition_axis.generation_key_sequence_axis,
                self.partition_axis.attention_dim_axis,
            )
            bias_partition_spec = PartitionSpec(
                self.partition_axis.batch_axis,
                self.partition_axis.bias_head_sequence_axis,
                self.partition_axis.generation_query_sequence_axis,
                self.partition_axis.bias_key_sequence_axis
            )
            attention_partition_spec = query_partition_spec
        return (
            query_partition_spec,
            key_partition_spec,
            value_partition_spec,
            bias_partition_spec,
            attention_partition_spec,
            is_generating
        )

    def _check_states(
            self,
            query_states: Array,
            key_states: Array,
            value_states: Array,
            query_sequence_length: int,
            key_value_sequence_length: int,
    ):
        batch_size = query_states.shape[0]
        assert batch_size == key_states.shape[0] == value_states.shape[0], "Batch Size for q,k,v wont match"
        k_v_req_shape = (
            batch_size,
            key_value_sequence_length,
            self.num_attention_heads,
            self.head_dims
        )
        q_shape = (
            batch_size,
            query_sequence_length,
            self.num_attention_heads,
            self.head_dims
        )

        assertion_mkv_err = f"""
        query_states, key_states, value_states and bias shapes must be like
        query_states Shape : [batch_size, q_seq_len , {self.num_attention_heads=}, {self.head_dims=}]
        key_states   Shape : [batch_size, kv_seq_len, {self.num_attention_heads=}, {self.head_dims=}]
        value_states Shape : [batch_size, kv_seq_len, {self.num_attention_heads=}, {self.head_dims=}]
        bias         Shape : [batch_size, {self.num_attention_heads=}, q_seq_len , kv_seq_len]
            """

        assert query_states.shape == q_shape, assertion_mkv_err + (
            f"\nMiss Match {query_states.shape} and "
            f"required Shape {q_shape}"
        )
        assert key_states.shape == k_v_req_shape, assertion_mkv_err + (
            f"\nMiss Match {key_states.shape} and "
            f"required Shape {k_v_req_shape}"
        )
        assert value_states.shape == k_v_req_shape, assertion_mkv_err + (
            f"\nMiss Match {value_states.shape} and "
            f"required Shape {k_v_req_shape}"
        )

    def __call__(
            self,
            query_states: Array,
            key_states: Array,
            value_states: Array,
            causal_mask: Optional[Array] = None,
            query_sequence_length: Optional[int] = None,
            key_value_sequence_length: Optional[int] = None,
            bias: Optional[Array] = None,
            attention_mask: Optional[Array] = None,
            segment_ids: Optional[Array] = None,
            causal: bool = True,
            deterministic: bool = False,
            dropout_rng: Optional[random.PRNGKey] = None,
            uses_cache: bool = False
    ):
        if query_sequence_length is None:
            query_sequence_length = query_states.shape[1]
        if key_value_sequence_length is None:
            key_value_sequence_length = key_states.shape[1]
        with self.mesh:
            if self._do_check:
                self._check_states(
                    query_states=query_states,
                    key_states=key_states,
                    value_states=value_states,
                    query_sequence_length=query_sequence_length,
                    key_value_sequence_length=key_value_sequence_length
                )
            if self.attn_mechanism == "flash":
                if segment_ids is not None:
                    warnings.warn(
                        "Flash attention don't support `segment_ids` this argument will be ignored",
                        UserWarning
                    )
                if self.attention_dropout != 0.0:
                    warnings.warn(
                        "Flash attention don't support `attention_dropout` this argument will be ignored",
                        UserWarning
                    )

                return self.flash_attention(
                    query_states=query_states,
                    key_states=key_states,
                    value_states=value_states,
                    bias=bias,
                    causal=causal,
                    query_sequence_length=query_sequence_length,
                    key_value_sequence_length=key_value_sequence_length
                )

            elif self.attn_mechanism == "vanilla":

                return self.vanilla_attention(
                    query_states=query_states,
                    key_states=key_states,
                    value_states=value_states,
                    bias=bias,
                    dropout_rng=dropout_rng,
                    deterministic=deterministic,
                    query_sequence_length=query_sequence_length,
                    key_value_sequence_length=key_value_sequence_length
                )
            elif self.attn_mechanism == "sharded_vanilla":
                return self.sharded_vanilla_attention(
                    query_states=query_states,
                    key_states=key_states,
                    value_states=value_states,
                    bias=bias,
                    dropout_rng=dropout_rng,
                    deterministic=deterministic,
                    query_sequence_length=query_sequence_length,
                    key_value_sequence_length=key_value_sequence_length
                )
            elif self.attn_mechanism == "legacy_sharded_vanilla":
                return self.legacy_sharded_vanilla_attention(
                    query_states=query_states,
                    key_states=key_states,
                    value_states=value_states,
                    bias=bias,
                    dropout_rng=dropout_rng,
                    deterministic=deterministic,
                    query_sequence_length=query_sequence_length,
                    key_value_sequence_length=key_value_sequence_length
                )
            elif self.attn_mechanism == "ring":
                return self.ring_attention(
                    query_states=query_states,
                    key_states=key_states,
                    value_states=value_states,
                    bias=bias,
                    dropout_rng=dropout_rng,
                    deterministic=deterministic,
                    segment_ids=segment_ids,
                    attention_mask=attention_mask,
                    query_sequence_length=query_sequence_length,
                    key_value_sequence_length=key_value_sequence_length
                )
            elif self.attn_mechanism == "pallas_flash":
                return self.pallas_flash_attention(
                    query_states=query_states,
                    key_states=key_states,
                    value_states=value_states,
                    query_sequence_length=query_sequence_length,
                    bias=bias,
                )
            elif self.attn_mechanism == "splash":
                if segment_ids is not None:
                    warnings.warn(
                        "Splash attention don't support `segment_ids` this argument will be ignored",
                        UserWarning
                    )
                if self.attention_dropout != 0.0:
                    warnings.warn(
                        "Splash attention don't support `attention_dropout` this argument will be ignored",
                        UserWarning
                    )
                if bias is not None:
                    warnings.warn(
                        "Splash attention don't support `bias` this argument will be ignored",
                        UserWarning
                    )

                return self.splash_attention(
                    query_states=query_states,
                    key_states=key_states,
                    value_states=value_states,
                    query_sequence_length=query_sequence_length,
                    key_value_sequence_length=key_value_sequence_length,
                    attention_mask=attention_mask
                )
            elif self.attn_mechanism == "blockwise":
                if segment_ids is not None:
                    warnings.warn(
                        "BlockWise Attention don't support `segment_ids` this argument will be ignored",
                        UserWarning
                    )
                return self.blockwise_attention(
                    query_states=query_states,
                    key_states=key_states,
                    value_states=value_states,
                    bias=bias,
                    deterministic=deterministic,
                    dropout_rng=dropout_rng,
                    query_sequence_length=query_sequence_length,
                    key_value_sequence_length=key_value_sequence_length
                )
            elif self.attn_mechanism == "cudnn":
                return self.cuddn_flash_attention(
                    query_states=query_states,
                    key_states=key_states,
                    value_states=value_states,
                    bias=bias,
                    causal=causal,
                    deterministic=deterministic,
                    query_sequence_length=query_sequence_length,
                    key_value_sequence_length=key_value_sequence_length
                )
            elif self.attn_mechanism == "local_ring":
                if segment_ids is not None:
                    warnings.warn(
                        "LocalRing Attention don't support `segment_ids` this argument will be ignored",
                        UserWarning
                    )
                if self.attention_dropout != 0.0:
                    warnings.warn(
                        "LocalRing Attention don't support `attention_dropout` this argument will be ignored",
                        UserWarning
                    )

                return self.local_ring_attention(
                    query_states=query_states,
                    key_states=key_states,
                    value_states=value_states,
                    bias=bias,
                    query_sequence_length=query_sequence_length,
                    key_value_sequence_length=key_value_sequence_length
                )
            elif self.attn_mechanism == "wise_ring":
                if segment_ids is not None:
                    warnings.warn(
                        "WiseRing Attention don't support `segment_ids` this argument will be ignored",
                        UserWarning
                    )
                if self.attention_dropout != 0.0:
                    warnings.warn(
                        "WiseRing Attention don't support `attention_dropout` this argument will be ignored",
                        UserWarning
                    )

                return self.wise_ring_attention(
                    query_states=query_states,
                    bias=bias,
                    value_states=value_states,
                    key_states=key_states,
                    segment_ids=segment_ids,
                    query_sequence_length=query_sequence_length,
                    key_value_sequence_length=key_value_sequence_length
                )
            else:
                raise ValueError(f"Unknown Attention mechanism of {self.attn_mechanism}")

    def local_ring_attention(
            self,
            *,  # it's Kwarg Only
            query_states: Array,
            key_states: Array,
            value_states: Array,
            query_sequence_length: int,
            key_value_sequence_length: int,
            bias: Optional[Array] = None,
    ):
        qps, kps, vps, bps, aps, _ = self.get_bshd_partition_specs(query_sequence_length)
        attention_outputs = shard_map(
            partial(
                ring_attention_standard,
                axis_name=self.axis_name,
                scale=1 / self.sm_scale,
                float32_logits=True,
            ),
            mesh=self.mesh,
            in_specs=(qps, kps, vps, bps,),
            out_specs=aps,
            check_rep=False
        )(
            query_states, key_states, value_states, bias
        )
        return AttentionOutput(
            attention_weights=None,
            attention_outputs=attention_outputs
        )

    def ring_attention(
            self,
            *,  # it's Kwarg Only
            query_states: Array,
            key_states: Array,
            value_states: Array,
            query_sequence_length: int,
            key_value_sequence_length: int,
            bias: Optional[Array] = None,
            attention_mask: Optional[Array] = None,
            deterministic: bool = False,
            dropout_rng: Optional[random.PRNGKey] = None,
            segment_ids: Optional[Array] = None,
    ):
        qps, kps, vps, bps, aps, _ = self.get_bshd_partition_specs(query_sequence_length)
        if segment_ids is None:
            segment_ids = jnp.zeros((query_states.shape[0], query_sequence_length), dtype="i4")
        if self.scan_ring_attention and query_states.shape[1] > max(
                self.block_q,
                self.block_k
        ):
            if self.platform == "tpu":
                ring_attention_fn = ring_flash_attention_tpu
            else:
                ring_attention_fn = fjformer.pallas_operations.ring_attention
            ring_attention_sharded = shard_map(
                partial(
                    ring_attention_fn,
                    axis_name=self.axis_name,
                    float32_logits=True,
                    blockwise_kwargs=dict(
                        deterministic=deterministic,
                        dropout_rng=dropout_rng,
                        attn_pdrop=self.attention_dropout,
                        causal=True,
                        query_chunk_size=self.block_q,
                        key_chunk_size=self.block_k,
                        dtype=self.dtype,
                        policy=get_gradient_checkpoint_policy("nothing_saveable"),
                        precision=self.precision,
                        prevent_cse=not self.scan_attention_layers,
                    )
                ),
                mesh=self.mesh,
                in_specs=(
                    qps,
                    kps,
                    vps,
                    bps,
                    PartitionSpec(self.partition_axis.batch_axis, None),
                ),
                out_specs=aps,
                check_rep=False
            )
            attn_output = ring_attention_sharded(query_states, key_states, value_states, bias, segment_ids)
            attn_output = with_sharding_constraint(attn_output, aps)
        else:
            if self.platform != "tpu":
                warnings.warn(
                    "Using Ring attention on CPUs or GPUs are not recommended due to miss computations at the moment. "
                    "please refer to other types of attention mechanism.your are bing fell back on "
                    "`ring_attention_sharded`"
                    f" Usage conditions was\nscan_ring_attention = {self.scan_ring_attention} [MUST BE TRUE]"
                    f"\nquery_states.shape[1]({query_states.shape[1]}) > max({self.block_q},{self.block_k})"
                    f"({max(self.block_q, self.block_k)})"
                )
            query_sequence_partition = self.partition_axis.generation_query_sequence_axis if (
                    query_states.shape[1] == 1
            ) else self.partition_axis.query_sequence_axis
            ring_attention_sharded = shard_map(
                partial(
                    ring_attention_standard,
                    axis_name=self.axis_name,
                    scale=self.sm_scale
                ),
                mesh=self.mesh,
                in_specs=(
                    qps,
                    kps,
                    vps,
                    PartitionSpec(self.partition_axis.batch_axis, None, query_sequence_partition, None)
                ),
                out_specs=PartitionSpec(
                    self.partition_axis.batch_axis,
                    query_sequence_partition,
                    self.partition_axis.head_axis,
                    None
                ),
                check_rep=False
            )
            attn_output = ring_attention_sharded(
                query_states, key_states, value_states, attention_mask
            )
        return AttentionOutput(
            attention_weights=None,
            attention_outputs=attn_output
        )

    def wise_ring_attention(
            self,
            *,  # it's Kwarg Only
            query_states: Array,
            key_states: Array,
            value_states: Array,
            query_sequence_length: int,
            key_value_sequence_length: int,
            bias: Optional[Array] = None,
            deterministic: bool = False,
            dropout_rng: Optional[random.PRNGKey] = None,
            segment_ids: Optional[Array] = None
    ):
        qps, kps, vps, bps, aps, _ = self.get_bshd_partition_specs(query_sequence_length)
        if segment_ids is None:
            segment_ids = jnp.zeros((query_states.shape[0], query_sequence_length), dtype="i4")
        if self.scan_ring_attention and query_states.shape[1] > max(self.block_q, self.block_k):
            ring_attention_sharded = shard_map(
                partial(
                    wise_ring_attention,
                    axis_name=self.axis_name,
                    float32_logits=True,
                    block_wise_kwargs=dict(
                        deterministic=deterministic,
                        dropout_rng=dropout_rng,
                        attn_pdrop=self.attention_dropout,
                        causal=True,
                        query_chunk_size=self.block_q,
                        key_chunk_size=self.block_k,
                        dtype=self.dtype,
                        policy=get_gradient_checkpoint_policy("nothing_saveable"),
                        precision=self.precision,
                        prevent_cse=not self.scan_attention_layers,
                    )
                ),
                mesh=self.mesh,
                in_specs=[qps, kps, vps, bps, PartitionSpec(qps[0], qps[1])],
                out_specs=aps,
                check_rep=False
            )
            attn_output = ring_attention_sharded(query_states, key_states, value_states, bias, segment_ids)
            attn_output = with_sharding_constraint(attn_output, aps)
            return AttentionOutput(
                attention_weights=None,
                attention_outputs=attn_output
            )
        else:
            seq_length = query_states.shape[1]
            chunk = seq_length > max(self.block_q, self.block_k)
            warnings.warn(
                f"generation process detected, switching to local ring attention"
                f" [CHUNK : {chunk}, SCAN : {self.scan_ring_attention}, {self.block_k=}, {self.block_q=}, {seq_length=}]"
            )
            return self.local_ring_attention(
                query_states=query_states,
                key_states=key_states,
                value_states=value_states,
                bias=bias,
                query_sequence_length=query_sequence_length,
                key_value_sequence_length=key_value_sequence_length
            )

    def vanilla_attention(
            self,
            *,  # it's Kwarg Only
            query_states: Array,
            key_states: Array,
            value_states: Array,
            bias: Optional[Array] = None,
            deterministic: bool = False,
            dropout_rng: Optional[random.PRNGKey] = None,
            query_sequence_length: int,
            key_value_sequence_length: int,
    ) -> AttentionOutput:
        dtype = jnp.promote_types(self.dtype, jnp.float32)
        with self.mesh:
            o, w = vanilla_attention(
                query_states=query_states,
                key_states=key_states,
                value_states=value_states,
                bias=bias,
                deterministic=deterministic,
                dtype=dtype,
                dropout_rng=dropout_rng,
                precision=self.precision,
                attention_dropout=self.attention_dropout,
                shard_attention_computation=self.shard_attention_computation,
            )
            return AttentionOutput(
                attention_weights=w,
                attention_outputs=o
            )

    def blockwise_attention(
            self,
            *,  # it's Kwarg Only
            query_states: Array,
            key_states: Array,
            value_states: Array,
            bias: Optional[Array] = None,
            deterministic: bool = False,
            dropout_rng: Optional[random.PRNGKey] = None,
            query_sequence_length: int,
            key_value_sequence_length: int,
    ) -> AttentionOutput:
        dtype = jnp.promote_types(self.dtype, jnp.float32)
        qps, kps, vps, bps, aps, is_gen = self.get_bshd_partition_specs(query_sequence_length)
        block_size = self.get_block_size_flash_attn(query_sequence_length, key_value_sequence_length)
        with self.mesh:
            query_states = with_sharding_constraint(query_states, qps)
            key_states = with_sharding_constraint(key_states, kps)
            value_states = with_sharding_constraint(value_states, vps)
            bias = with_sharding_constraint(bias, bps)
            o = blockwise_attn(
                query=query_states,
                key=key_states,
                value=value_states,
                bias=bias,
                deterministic=deterministic,
                dtype=dtype,
                dropout_rng=dropout_rng,
                precision=self.precision,
                attn_pdrop=self.attention_dropout,
                key_chunk_size=block_size.block_k,
                query_chunk_size=block_size.block_q,
                prevent_cse=not self.scan_attention_layers,
                causal=True,
                float32_logits=True
            )

            o = with_sharding_constraint(o, aps)
            return AttentionOutput(
                attention_weights=None,
                attention_outputs=o
            )

    def sharded_vanilla_attention(
            self,
            *,  # it's Kwarg Only
            query_states: Array,
            key_states: Array,
            value_states: Array,
            bias: Optional[Array] = None,
            deterministic: bool = False,
            dropout_rng: Optional[random.PRNGKey] = None,
            query_sequence_length: int,
            key_value_sequence_length: int,
    ) -> AttentionOutput:
        dtype = jnp.promote_types(self.dtype, jnp.float32)

        qps, kps, vps, bps, aps, is_gen = self.get_bshd_partition_specs(query_sequence_length)

        with self.mesh:
            query_states = fjformer.with_sharding_constraint(query_states, qps)
            key_states = fjformer.with_sharding_constraint(key_states, kps)
            value_states = fjformer.with_sharding_constraint(value_states, vps)

            query_states, key_states, value_states = promote_dtype(
                query_states, key_states, value_states,
                dtype=dtype
            )

            depth = query_states.shape[-1]
            query_states = query_states / jnp.sqrt(depth).astype(dtype)
            attention_weight = jnp.einsum("...qhd,...khd->...hqk", query_states, key_states, precision=self.precision)
            if bias is not None:
                bias = fjformer.with_sharding_constraint(bias, bps)
                attention_weight = jnp.add(attention_weight, bias)

            attention_weight = jax.nn.softmax(
                attention_weight.astype(jnp.float32)
            ).astype(dtype)

            if not deterministic and self.attention_dropout > 0.0:
                keep_prob = 1.0 - self.attention_dropout
                dropout_shape = tuple([1] * (key_states.ndim - 2)) + attention_weight.shape[-2:]
                keep = random.bernoulli(dropout_rng, keep_prob, dropout_shape)  # type: ignore

                multiplier = keep.astype(dtype) / jnp.asarray(keep_prob, dtype=dtype)
                attention_weight = attention_weight * multiplier

            attention = jnp.einsum(
                "...hqk,...khd->...qhd",
                attention_weight,
                value_states,
                precision=self.precision
            )
            attention = fjformer.with_sharding_constraint(attention, aps)
            return AttentionOutput(
                attention_weights=attention_weight,
                attention_outputs=attention
            )

    def legacy_sharded_vanilla_attention(
            self,
            *,  # it's Kwarg Only
            query_states: Array,
            key_states: Array,
            value_states: Array,
            bias: Optional[Array] = None,
            deterministic: bool = False,
            dropout_rng: Optional[random.PRNGKey] = None,
            query_sequence_length: int,
            key_value_sequence_length: int,
    ) -> AttentionOutput:
        dtype = jnp.promote_types(self.dtype, jnp.float32)

        qps, kps, vps, bps, aps, is_gen = self.get_bshd_partition_specs(query_sequence_length)

        with self.mesh:
            attention_outputs = shard_map(
                partial(
                    shard_vanilla_attention,
                    deterministic=deterministic,
                    dropout_rng=dropout_rng,
                    dtype=dtype,
                    precision=self.precision,
                    attention_dropout=self.attention_dropout
                ),
                in_specs=(
                    qps,
                    kps,
                    vps,
                    PartitionSpec(bps[0], None, None, None) if bias is not None else None
                ),
                out_specs=aps,
                check_rep=False,
                mesh=self.mesh
            )(query_states, key_states, value_states, bias)
            attention_outputs = fjformer.with_sharding_constraint(attention_outputs, aps)

            return AttentionOutput(
                attention_weights=None,
                attention_outputs=attention_outputs
            )

    def flash_attention(
            self,
            *,  # it's Kwarg Only
            query_states: Array,
            key_states: Array,
            value_states: Array,
            query_sequence_length: int,
            key_value_sequence_length: int,
            bias: Optional[Array] = None,
            causal: bool = False,
    ) -> AttentionOutput:

        qps, kps, vps, bps, aps, is_gen = self.get_bhsd_partition_specs(query_sequence_length)
        block_size = self.get_block_size_flash_attn(query_sequence_length, key_value_sequence_length)
        query_states = query_states.transpose(0, 2, 1, 3)
        key_states = key_states.transpose(0, 2, 1, 3)
        value_states = value_states.transpose(0, 2, 1, 3)

        batch_size, num_attention_heads, query_sequence_length, head_dims = query_states.shape
        if bias is not None:
            if bias.shape[1] != num_attention_heads:
                bias = bias.repeat(num_attention_heads, 1, )

        flash_func, float32_logits, _ = get_flash_attention()
        if float32_logits:
            query_states, key_states, value_states = map(
                lambda s: s.astype(jnp.float32),
                (query_states, key_states, value_states)
            )

        if self.sm_scale is None:
            self.sm_scale = 1 / math.sqrt(query_states[-1])
        attention_o = shard_map(
            partial(
                flash_func,
                causal=causal,
                sm_scale=self.sm_scale,
                block_sizes=block_size,
                debug=False
            ),
            in_specs=(qps, kps, vps, bps),
            out_specs=aps,
            mesh=self.mesh,
            check_rep=False,
        )(
            query_states,
            key_states,
            value_states,
            bias,
        )

        attention_o = attention_o.transpose(0, 2, 1, 3)
        return AttentionOutput(
            attention_outputs=attention_o,
            attention_weights=None
        )

    def splash_attention(
            self,
            query_states: Array,
            key_states: Array,
            value_states: Array,
            query_sequence_length: int,
            key_value_sequence_length: int,
            attention_mask: Array
    ) -> AttentionOutput:

        qps, kps, vps, bps, aps, is_gen = self.get_bhsd_partition_specs(query_sequence_length)

        query_states = query_states.transpose(0, 2, 1, 3)
        key_states = key_states.transpose(0, 2, 1, 3)
        value_states = value_states.transpose(0, 2, 1, 3)

        query_states, key_states, value_states = map(
            lambda s: s.astype(jnp.float32),
            (query_states, key_states, value_states)
        )
        if attention_mask is not None:
            if attention_mask.ndim == 4:
                attention_mask = attention_mask[:, 0, -1]
            attention_mask = SegmentIds(attention_mask, attention_mask)
        else:
            warnings.warn("`attention_mask` is not passed to SplashAttention. (except miss computation problem)")

        @partial(
            shard_map,
            in_specs=(qps, kps, vps, PartitionSpec(qps[0], qps[2])),  # make it easier
            out_specs=qps,
            mesh=self.mesh,
            check_rep=False,
        )
        def splash_attention_call(q, k, v, am):
            block_size = self.get_block_size_splash_attn(query_sequence_length, key_value_sequence_length)
            masks = [CausalMask(shape=(q.shape[2], k.shape[2])) for _ in range(q.shape[1])]
            multi_head_mask = MultiHeadMask(masks=masks)
            splash_kernel = make_splash_mha(
                mask=multi_head_mask,
                head_shards=1,
                q_seq_shards=1,
                block_sizes=block_size
            )

            return jax.vmap(splash_kernel)(q, k, v, segment_ids=am)

        attention_o = splash_attention_call(query_states, key_states, value_states, attention_mask)

        attention_o = attention_o.transpose(0, 2, 1, 3)
        return AttentionOutput(
            attention_outputs=attention_o,
            attention_weights=None
        )

    def pallas_flash_attention(
            self,
            *,
            query_states: Array,
            key_states: Array,
            value_states: Array,
            query_sequence_length: int = None,
            bias: Optional[Array] = None,
    ) -> AttentionOutput:
        if query_sequence_length is None:
            query_sequence_length = query_states.shape[1]
        qps, kps, vps, bps, aps, is_gen = self.get_bshd_partition_specs(query_sequence_length)

        query_states, key_states, value_states = map(
            lambda s: s.astype(jnp.float32),
            (query_states, key_states, value_states)
        )
        # query_states = with_sharding_constraint(query_states, qps)
        # key_states = with_sharding_constraint(key_states, kps)
        # value_states = with_sharding_constraint(value_states, vps)
        # bias = with_sharding_constraint(bias, bps)
        wrapped_fn = partial(
            flash_attention,
            sm_scale=self.sm_scale,
            block_k=self.block_k,
            block_q=self.block_q,
            interpret=True if self.platform == "cpu" else None,  # auto-decide
            backward_pass_impl=self.backward_pass_impl,
            debug=False
        )
        attention_outputs = shard_map(
            f=wrapped_fn,
            in_specs=(qps, kps, vps, bps),
            out_specs=aps,
            mesh=self.mesh,
            check_rep=False,
        )(
            query_states,
            key_states,
            value_states,
            bias,
        )
        attention_outputs = with_sharding_constraint(attention_outputs, aps)
        return AttentionOutput(
            attention_weights=None,
            attention_outputs=attention_outputs
        )

    def cuddn_flash_attention(
            self,
            *,  # it's Kwarg Only
            query_states: Array,
            key_states: Array,
            value_states: Array,
            bias: Optional[Array] = None,
            causal: bool = False,
            deterministic: bool = True,
            query_sequence_length: int,
            key_value_sequence_length: int,
    ) -> AttentionOutput:
        """CUDNN Flash Attention with Transformer Engine."""
        try:
            import transformer_engine.jax.fused_attn as fused_attn
            from transformer_engine.jax.fused_attn import AttnBiasType, AttnMaskType, QKVLayout
            from transformer_engine.jax.fused_attn import is_fused_attn_kernel_available
        except (ModuleNotFoundError, ImportError) as err:
            raise RuntimeError(
                "Please install transformer_engine first. you can install that by running "
                f"`pip install git+https://github.com/NVIDIA/TransformerEngine`"
                f"\nhere's extra information on error\n{err}"
            )
        batch, query_sequence_length, num_attention_heads, head_dim = query_states.shape

        qkv_layout = QKVLayout.BS3HD
        attn_mask_type = AttnMaskType.CAUSAL_MASK
        attn_bias_type = AttnBiasType.NO_BIAS

        if self.sm_scale is None:
            self.sm_scale = 1 / math.sqrt(head_dim)
        has_fused_attn_kernel = is_fused_attn_kernel_available(
            self.dtype, self.dtype, qkv_layout,
            attn_bias_type,
            attn_mask_type,
            self.attention_dropout,
            self.num_attention_heads,
            key_states.shape[2],
            query_sequence_length,
            key_value_sequence_length,
            head_dim
        )

        if not has_fused_attn_kernel:
            raise ValueError(
                "Flash attention kernel is not supported for current requested arrays"
                " for details check this repo https://github.com/NVIDIA/TransformerEngine/"
            )

        return AttentionOutput(
            attention_weights=None,
            attention_outputs=fused_attn.self_fused_attn(
                qkv=jnp.concatenate(
                    (
                        jnp.reshape(query_states, (*query_states.shape[:2], 1, *query_states.shape[-2:])),
                        jnp.reshape(key_states, (*query_states.shape[:2], 1, *query_states.shape[-2:])),
                        jnp.reshape(value_states, (*query_states.shape[:2], 1, *query_states.shape[-2:]))
                    ),
                    axis=2
                ),
                bias=bias,
                mask=jnp.zeros((batch, 1, query_sequence_length, key_value_sequence_length)) if causal else None,
                seed=None,
                attn_bias_type=attn_bias_type,
                attn_mask_type=attn_mask_type,
                scaling_factor=self.sm_scale,
                dropout_probability=self.attention_dropout,
                is_training=deterministic
            )
        )

    @staticmethod
    def test_attentions(
            batch_size=8,
            sequence_length=128 * 8,
            num_attention_heads=32,
            num_key_value_heads=32,
            chunk_size=128,
            axis_dims=(1, -1, 1, 1)
    ):
        """creates a test for attention module to help you find the best attention mechanism you can use."""
        import flax
        try:
            import pandas
        except (ModuleNotFoundError, ImportError):
            warnings.warn("couldn't import pandas ... please install pandas")
            pandas = None
        from ..modules.mistral import MistralConfig
        from fjformer import GenerateRNG
        head_dim = 128
        rng = GenerateRNG()

        config = MistralConfig(
            axis_dims=axis_dims,
            block_q=chunk_size,
            block_k=chunk_size
        )

        def value_and_grad_wrapper(fn, **kwargs):
            @partial(jax.value_and_grad, **kwargs)
            def inner(*args, **kwargs):
                return jnp.sum(fn(*args, **kwargs))

            return inner

        def diff(t1, t2):
            return jnp.max(jnp.abs(t1 - t2))

        @value_and_grad_wrapper
        def call_dot_product(q, k, v, b, ):
            attention_pred = flax.linen.dot_product_attention(q, k, v, b, )
            return attention_pred

        @value_and_grad_wrapper
        def call_attention_module(q, k, v, b, a, attn_mechanism):
            attention_pred = AttentionModule(
                attn_mechanism=attn_mechanism,
                axis_name="sp",
                dtype=jnp.float32,
                mesh=config.get_mesh(),
                head_dims=q.shape[-1],
                sm_scale=1 / math.sqrt(q.shape[-1]),
                num_attention_heads=q.shape[-2],
                block_q=config.block_q,
                block_k=config.block_k,
                base_module_class=config,
            )(
                query_states=q,
                key_states=k,
                value_states=v,
                bias=b,
                attention_mask=a
            ).attention_outputs
            return attention_pred

        def make_inputs():
            q = jax.random.normal(
                rng.rng,
                (batch_size, sequence_length, num_attention_heads, head_dim),
                dtype="float32"
            )
            k = jax.random.normal(
                rng.rng,
                (batch_size, sequence_length, num_key_value_heads, head_dim),
                dtype="float32"
            )
            v = jax.random.normal(
                rng.rng,
                (batch_size, sequence_length, num_key_value_heads, head_dim),
                dtype="float32"
            )
            c = flax.linen.attention.make_causal_mask(jnp.ones((batch_size, sequence_length)))
            a = jnp.ones((batch_size, sequence_length))
            a = a.at[:, sequence_length // 2:].set(0)
            b = jnp.where(flax.linen.attention.combine_masks(jnp.expand_dims(jnp.expand_dims(a, 1), 1), c), 0, -jnp.inf)

            return q, k, v, b, a

        q, k, v, b, a = make_inputs()
        excepted_output, excepted_grads = call_dot_product(q, k, v, b)
        test_attentions = [
            "local_ring",
            "blockwise",
            "vanilla",
            "wise_ring",
            "sharded_vanilla",
            "legacy_sharded_vanilla",
            "flash",
            "splash",
            "cudnn",
            "pallas_flash"
        ]
        fns = {
            k: partial(call_attention_module, attn_mechanism=k) for k in test_attentions
        }
        outs_and_grads = {}
        for nm, fn in fns.items():
            try:
                start = time.time()
                out = jax.block_until_ready(fn(q, k, v, b, a))
                end = time.time() - start
                outs_and_grads[nm] = out + (end,)
            except Exception as e:
                print(f"{nm} is Failed :\n\n{e}")
                outs_and_grads[nm] = (None, None, None)
        frame_out = {}
        for key, (out, grad, time_took) in outs_and_grads.items():

            if out is None and grad is None:
                frame_out[key.upper()] = {
                    "OUT DIFF": "NA",
                    "GRADIENT DIFF SUM": "NA",
                    "TEST PASSED": "NA",
                    "COMP TIME": "NA"
                }
            else:
                output_diff = diff(excepted_output, out)
                g_diff = [diff(*args) for args in zip(excepted_grads, grad)]
                sum_g = sum(g_diff)
                # TODO : Fix this
                # XlaRuntimeError: FAILED_PRECONDITION: The program continuator has halted unexpectedly.
                # sum_g = jax.device_get(sum_g)
                # output_diff = jax.device_get(output_diff)
                frame_out[key.upper()] = {
                    "OUT DIFF": output_diff,
                    "GRADIENT DIFF SUM": sum_g,
                    "TEST PASSED": sum_g < 1 and output_diff < 1e-2,
                    "COMP TIME": time_took
                }
        if pandas is not None:
            result = pandas.DataFrame.from_dict(frame_out)
            result = result.transpose()
            return result
        else:
            return frame_out
