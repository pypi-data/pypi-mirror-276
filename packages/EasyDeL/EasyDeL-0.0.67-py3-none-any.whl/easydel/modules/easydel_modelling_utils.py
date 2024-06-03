import warnings

import chex
import fjformer.linen
import flax
from jax.experimental.mesh_utils import create_device_mesh
from transformers import PretrainedConfig, FlaxPreTrainedModel, AutoModelForCausalLM
import jax
from jax import numpy as jnp
from typing import Sequence, Union, Optional, Literal, Tuple, Any
from dataclasses import dataclass
from jax.sharding import PartitionSpec, Mesh
from ..etils.etils import get_logger
from ..etils.easystate import EasyDeLState
from ..etils.partition_module import PartitionAxis

logger = get_logger(__name__)
AVAILABLE_ATTENTION_MECHANISMS = Literal[
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
]


def set_attrs_smartly(self, attr_name: str, default: Any, new_attr: Any):
    if not hasattr(self, attr_name):
        setattr(self, attr_name, default)
    if not new_attr == Ellipsis:
        setattr(self, attr_name, new_attr)


@dataclass
class EasyMethod:
    TRAIN: str = "train"
    SERVE: str = "serve"
    EVAL: str = "serve"
    CONVERT: str = "convert"


class EasyDeLPretrainedConfig(PretrainedConfig):
    """It initializes all the attributes of an object, and it's called when you create a new instance of that class.

    Args:
        self: Refer to the instance of the class
        axis_dims: Sequence[int]: Specify the number of dimensions for
            each axis
        axis_names: Sequence[str]: Set the names of the axes
        attn_mechanism: Literal["vanilla", "flash", "splash", "ring"]:
            attention mechanism to use
        block_k: int: block size of key_states
        block_q: int: block size of query_states
        block_b: int: block size of bias
        block_q_major_dkv: int: block size of block_q_major_dkv
        block_k_major_dkv: int: block size of block_k_major_dkv
        block_k_dkv: int: block size of block_k_dkv
        block_q_dkv: int: block size of block_q_dkv
        block_k_major_dq: int: block size of block_k_major_dq
        block_k_dq: int: block size of block_k_dq
        block_q_dq: int: block size of block_q_dq
        partition_axis (PartitionAxis) : PartitionAxis is new module used for partitioning arrays in easydel.
        shard_attention_computation: bool: whenever to shard qkv b for
            attention
        use_sharding_constraint: bool: whether to use sharding
            constraint for the arrays
        use_scan_mlp: bool: Determine whether to use scan_mlp or not
        backend: Optional[None]: Specify the backend to use
        flash_attention_backward_pass_impl: Literal["triton", "xla"]:
            Specify the backward pass kernel for flash attention
    """

    def __init__(
            self,
            axis_dims: Sequence[int] = (1, -1, 1, 1),
            axis_names: Sequence[str] = ("dp", "fsdp", "tp", "sp"),
            attn_mechanism: AVAILABLE_ATTENTION_MECHANISMS = "sharded_vanilla",
            block_k: int = 128,
            block_q: int = 128,
            block_b: int = 1,
            block_k_major: int = 128,
            block_q_major_dkv: int | None = None,
            block_k_major_dkv: int | None = None,
            block_k_dkv: int | None = None,
            block_q_dkv: int | None = None,
            block_k_major_dq: int | None = None,
            block_k_dq: int | None = None,
            block_q_dq: int | None = None,
            partition_axis: PartitionAxis = PartitionAxis(),
            shard_attention_computation: bool = True,
            use_sharded_kv_caching: bool = True,
            use_sharding_constraint: bool = False,
            backend: Optional[None] = jax.default_backend(),
            easy_method: Literal["train", "serve", "convert"] = EasyMethod.TRAIN,
            bits: Optional[int] = None,
            scan_ring_attention: bool = True,
            scan_attention_layers: bool = False,
            use_scan_mlp: bool = True,
            scan_mlp_chunk_size: int = 1024,
            attention_axis_name: str = "sp",
            quantize_kv_cache: bool = False,
            flash_attention_backward_pass_impl: Literal["triton", "xla"] = "triton",
            **kwargs
    ):
        self.axis_dims = axis_dims
        self.axis_names = axis_names
        self.backend = backend if backend is not None else ""
        self.easy_method = easy_method
        self.attn_mechanism = attn_mechanism
        self.block_b = block_b
        self.block_k = block_k
        self.block_q = block_q
        self.block_k_major = block_k_major
        self.block_q_major_dkv = block_q_major_dkv or block_q
        self.block_k_major_dkv = block_k_major_dkv or block_k
        self.block_k_dkv = block_k_dkv or block_k
        self.block_q_dkv = block_q_dkv or block_q
        self.block_k_major_dq = block_k_major_dq or block_k
        self.block_k_dq = block_k_dq or block_k
        self.block_q_dq = block_q_dq or block_q
        self.partition_axis = partition_axis
        self.shard_attention_computation = shard_attention_computation
        self.bits = bits
        self.scan_attention_layers = scan_attention_layers
        self.scan_ring_attention = scan_ring_attention
        self.use_sharded_kv_caching = use_sharded_kv_caching
        self.use_scan_mlp = use_scan_mlp
        self.scan_mlp_chunk_size = scan_mlp_chunk_size
        self.use_sharding_constraint = use_sharding_constraint
        self.attention_axis_name = attention_axis_name
        self.quantize_kv_cache = quantize_kv_cache
        self.flash_attention_backward_pass_impl = flash_attention_backward_pass_impl
        super().__init__(**kwargs)

    @staticmethod
    def create_mesh(
            axis_dims: Sequence[int] = (1, -1, 1, 1),
            axis_names: Sequence[str] = ("dp", "fsdp", "tp", "sp"),
            backend=""
    ):
        """The create_mesh function creates a mesh object that can be used to shard arrays.

        Args:
            axis_dims: Sequence[int]: Specify the dimensions of the mesh
            axis_names: Sequence[str]: Name the axes of the mesh
            backend: Specify the backend to use

        Returns:
            A mesh object
        """
        array_devices = jax.numpy.ones(
            (len(jax.devices() if backend == "" else jax.devices(backend)), 1))
        if isinstance(axis_dims, str):
            axis_dims = eval(axis_dims)
            warnings.warn(
                "axis_dims argument is not a Sequence of int and it's an string. "
                "(backbone Warning in EasyDeLModuleConfig)\n"
                f"\tchanged to {axis_dims}"
            )
        if isinstance(axis_names, str):
            axis_names = eval(axis_names)
            warnings.warn(
                "axis_names argument is not a Sequence of strings and it's an string class. "
                "(backbone Warning in EasyDeLModuleConfig)\n"
                f"\tchanged to {axis_names}"
            )
        resh = array_devices.reshape(axis_dims).shape

        return Mesh(
            create_device_mesh(resh), axis_names
        )

    def get_mesh(self) -> Mesh:
        """The get_mesh function is a helper function that creates a Mesh object from the
        axis_dims and axis_names attributes of an object, which are assumed to be lists of integers and strings, respectively.
        The backend attribute is also used if it exists.

        Args:
            self: Refer to the object itself

        Returns:
            A jaxMesh
        """
        return self.create_mesh(
            axis_dims=[v for k, v in self.axis_dims.items()] if isinstance(
                self.axis_dims,
                dict
            ) else self.axis_dims,
            axis_names=[v for k, v in self.axis_names.items()] if isinstance(
                self.axis_names,
                dict
            ) else self.axis_names,
            backend=(self.backend if self.backend is not None else "") if hasattr(self, 'backend') else ""
        )

    @property
    def mesh(self):
        return self.get_mesh()

    def jax_mesh(self):
        warnings.warn("`jax_mesh` is deprecated use `get_mesh` or `mesh`")
        return self.get_mesh()

    def get_partition_rules(self, fully_sharded_data_parallel: bool = True):

        """The get_partition_rules function is used to specify how the parameters of a model are partitioned across devices.

        Args:
            self: Access the attributes of the class
            fully_sharded_data_parallel: bool: Determine whether the
                model is fully sharded or not

        Returns:
            A tuple of tuples
        """
        if not fully_sharded_data_parallel:
            raise NotImplementedError()
        else:
            return (
                ('.*', PartitionSpec(("fsdp", "sp"), ),),
            )

    def get_axis_dims(self) -> Sequence[int]:
        """The get_axis_dims function returns a sequence of integers representing the dimensions of each axis.

        Args:
            self: Represent the instance of the class

        Returns:
            The dimensions of the axes
        """
        return self.axis_dims

    def get_axis_names(self) -> Sequence[str]:
        """The get_axis_names function returns a list of the names of the axes.

        Args:
            self: Represent the instance of the class

        Returns:
            A list of the names of all axes
        """
        return self.axis_names

    def get_backend(self) -> str:
        """The get_backend function returns the backend that is currently being used.
        If no backend has been set, it will return the default JAX backend.

        Args:
            self: Bind the method to an object

        Returns:
            The backend platform
        """
        return self.backend if not self.backend == "" else jax.lib.xla_bridge.get_backend().platform

    def add_basic_configurations(
            self,
            axis_dims: Sequence[int] = ...,
            axis_names: Sequence[str] = ...,
            attn_mechanism: AVAILABLE_ATTENTION_MECHANISMS = ...,
            block_k: int = ...,
            block_q: int = ...,
            block_b: int = ...,
            block_k_major: int = ...,
            block_q_major_dkv: int | None = ...,
            block_k_major_dkv: int | None = ...,
            block_k_dkv: int | None = ...,
            block_q_dkv: int | None = ...,
            block_k_major_dq: int | None = ...,
            block_k_dq: int | None = ...,
            block_q_dq: int | None = ...,
            partition_axis: PartitionAxis = ...,
            shard_attention_computation: bool = ...,
            use_sharded_kv_caching: bool = ...,
            backend: Optional[None] = ...,
            easy_method: Literal["train", "serve", "convert"] = ...,
            bits: Optional[int] = ...,
            scan_ring_attention: bool = ...,
            scan_attention_layers: bool = ...,
            use_sharding_constraint: bool = ...,
            use_scan_mlp: bool = ...,
            scan_mlp_chunk_size: int = ...,
            attention_axis_name: str = ...,
            quantize_kv_cache: bool = ...,
            flash_attention_backward_pass_impl: Literal["triton", "xla"] = ...
    ):
        """It initializes all the attributes of an object, and it's called when you create a new instance of that class.

        Args:
            self: Refer to the instance of the class
            axis_dims: Sequence[int]: Specify the number of dimensions
                for each axis
            axis_names: Sequence[str]: Set the names of the axes
            attn_mechanism: Literal["vanilla", "flash", "splash"]:
                attention mechanism to use
            block_k: int: block size of key_states
            block_q: int: block size of query_states
            block_b: int: block size of bias
            block_k_major: int: block size if key major
            block_q_major_dkv: int: block size of block_q_major_dkv
            block_k_major_dkv: int: block size of block_k_major_dkv
            block_k_dkv: int: block size of block_k_dkv
            block_q_dkv: int: block size of block_q_dkv
            block_k_major_dq: int: block size of block_k_major_dq
            block_k_dq: int: block size of block_k_dq
            block_q_dq: int: block size of block_q_dq

            partition_axis (PartitionAxis) : PartitionAxis is new module used for partitioning arrays in easydel.
            shard_attention_computation: bool: whenever to use shard_map
                for attention
            use_sharded_kv_caching: bool: whenever to use shard_map and
                sharding for key and value
            backend: Optional[None]: Specify the backend to use
            easy_method: Literal["train", "serve", "convert"]: easydel
                Quantization Method to be applied for
            bits: Optional[int]: Model bits for quantization
            use_sharding_constraint: bool: whether to use sharding
                constraint for the arrays
            scan_ring_attention: bool: Whether to use can for ring
                attention
            scan_attention_layers: bool: Whether to use can for
                attention layers
            use_scan_mlp: bool: Determine whether to use scan_mlp or not
            scan_mlp_chunk_size: int: Size of chunks in scan MLP.
            attention_axis_name: str: Name of the attention axis name
            quantize_kv_cache: bool: Whether to quantize Key/Value in
                attention for generation process.
            flash_attention_backward_pass_impl: Literal["triton", "xla"]: Specify the backward pass kernel for flash attention
        in generation process
        in generation process
        """
        set_attrs_smartly(self, "axis_dims", (1, -1, 1, 1), axis_dims)
        set_attrs_smartly(self, "axis_names", ("dp", "fsdp", "tp", "sp"), axis_names)

        set_attrs_smartly(self, "block_q", 1024, block_q)
        set_attrs_smartly(self, "block_k", 1024, block_k)
        set_attrs_smartly(self, "block_b", 1024, block_b)

        set_attrs_smartly(self, "partition_axis", PartitionAxis(), partition_axis)

        set_attrs_smartly(self, "use_sharding_constraint", False, use_sharding_constraint)
        set_attrs_smartly(self, "backend", jax.default_backend(), backend)
        set_attrs_smartly(self, "shard_attention_computation", True, shard_attention_computation)
        set_attrs_smartly(self, "use_sharded_kv_caching", True, use_sharded_kv_caching)
        set_attrs_smartly(self, "attn_mechanism", "sharded_vanilla", attn_mechanism)

        set_attrs_smartly(self, "block_k_dkv", block_k_dkv or self.block_k, block_k_dkv)
        set_attrs_smartly(self, "block_q_dkv", block_q_dkv or self.block_q, block_q_dkv)

        set_attrs_smartly(self, "block_q_major_dkv", block_q_major_dkv or self.block_q, block_q_major_dkv)
        set_attrs_smartly(self, "block_k_major_dkv", block_k_major_dkv or self.block_k, block_k_major_dkv)

        set_attrs_smartly(self, "block_k_major", block_k_major or self.block_k, block_k_major)
        set_attrs_smartly(self, "block_k_major_dq", block_k_major_dq or self.block_k, block_k_major_dq)

        set_attrs_smartly(self, "block_k_dq", block_k_dq or self.block_k, block_k_dq)
        set_attrs_smartly(self, "block_q_dq", block_q_dq or self.block_q, block_q_dq)

        set_attrs_smartly(self, "easy_method", EasyMethod.TRAIN, easy_method)
        set_attrs_smartly(self, "bits", None, bits)
        set_attrs_smartly(self, "scan_attention_layers", True, scan_attention_layers)
        set_attrs_smartly(self, "scan_ring_attention", True, scan_ring_attention)
        set_attrs_smartly(self, "use_scan_mlp", True, use_scan_mlp)
        set_attrs_smartly(self, "scan_mlp_chunk_size", 1024, scan_mlp_chunk_size)
        set_attrs_smartly(self, "attention_axis_name", "sp", attention_axis_name)
        set_attrs_smartly(self, "quantize_kv_cache", False, quantize_kv_cache)
        set_attrs_smartly(self, "flash_attention_backward_pass_impl", "triton", flash_attention_backward_pass_impl)

    def __repr__(self):

        """The __repr__ function is used to generate a string representation of an object.
        This function should return a string that can be parsed by the Python interpreter
        to recreate the object. The __repr__ function is called when you use print() on an
        object, or when you type its name in the REPL.

        Args:
            self: Refer to the instance of the class

        Returns:
            A string representation of the object
        """
        string = f"{self.__class__.__name__}(\n"
        for k, v in self.__dict__.items():
            if not k.startswith("_"):
                try:
                    repr_src = f"\t{k} : " + v.__str__().replace("\n", "\n\t") + "\n"
                    string += repr_src if len(repr_src) < 500 else f"\t{k} : " + f"{v.__class__.__name__}(...)" + "\n"
                except TypeError:
                    pass
        return string + ")"

    def add_jax_args(self, **kwargs):
        for k, v in kwargs.items():
            set_attrs_smartly(self, "k", v, v)

    def __str__(self):

        """The __str__ function is called when you use the print function or when str() is used.
        It should return a string representation of the object.

        Args:
            self: Refer to the instance of the class

        Returns:
            The object's string representation
        """
        return self.__repr__()


class EasyDeLFlaxPretrainedModel(FlaxPreTrainedModel):
    def __init__(
            self,
            config: Optional[PretrainedConfig] = None,
            module: Optional[flax.linen.Module] = None,
            input_shape: Tuple = (1, 1),
            seed: int = 0,
            dtype: jnp.dtype = jnp.float32,
            param_dtype: jnp.dtype = jnp.float32,  # Ignored
            precision: Optional[Union[jax.lax.Precision, str]] = None,  # Ignored
            _do_init: bool = True,
    ):
        assert config is not None, "`config` must be provided.`"
        assert module is not None, "`module` must be provided.`"
        super().__init__(
            config=config,
            module=module,
            input_shape=input_shape,
            seed=seed,
            dtype=dtype,
            _do_init=_do_init
        )

    @property
    def mesh(self):
        return self.config.get_mesh()

    def get_named_sharding(self, partition_rules=None, partition_specs=None):
        if partition_rules is None:
            partition_rules = self.config.get_partition_rules(True)
        if partition_specs is None:
            partition_specs = fjformer.match_partition_rules(partition_rules, self.params_shape_tree)
        return jax.tree_util.tree_map(
            lambda spec: jax.sharding.NamedSharding(spec=spec, mesh=self.mesh, ),
            partition_specs
        )

    def get_input_embeddings(self):
        """The get_input_embeddings function returns the embedding layer of the model.

        Args:
            self: Refer to the current object

        Returns:
            The embedding layer of the model
        """
        raise NotImplementedError()

    def set_input_embeddings(self, value):
        """The set_input_embeddings function is used to set the embedding module of the model.

        Args:
            self: Represent the instance of the class
            value: Set the embeddings of the model
        """
        raise NotImplementedError()

    def get_output_embeddings(self):
        """The get_output_embeddings function returns the output embeddings of a model.

        Args:
            self: Represent the instance of the class

        Returns:
            The output embeddings of the model
        """
        raise NotImplementedError()

    def set_output_embeddings(self, new_embeddings):
        """The set_output_embeddings function is used to set the output embeddings of a model.
        This function can be used to change the output embedding layer of a pretrained model in order to finetune it
        to some downstream task. Changing this layer has an effect only if the model has already been fine-tuned on some
        task (e.g., for classification). If you are training your own language models, you should call this function before
        you start training.

        Args:
            self: Represent the instance of the class
            new_embeddings: Set the embeddings of the output layer

        Returns:
            A new embedding layer
        """
        raise NotImplementedError()

    def set_decoder(self, decoder):
        """The set_decoder function is used to set the decoder for a given encoder.

        Args:
            self: Refer to the object itself
            decoder: Set the decoder for a given encoder

        Returns:
            A decoder
        """
        raise NotImplementedError()

    def get_decoder(self):
        """The get_decoder function is used to create a decoder object.

        Args:
            self: Represent the instance of the class

        Returns:
            A decoder object
        """
        raise NotImplementedError()

    def init_cache(self, batch_size: int, max_length: int):
        raise NotImplementedError("init_cache is not Implemented Yet!")

    def prepare_inputs_for_generation(self, input_ids, max_length, attention_mask: Optional[chex.Array] = None):
        """The prepare_inputs_for_generation function is used to prepare the inputs for a generation task.

        Args:
            self: Access variables that belong to the class
            input_ids: Pass in the input tokens
            max_length: Set the length of the sequence to be generated
            attention_mask: Optional[chex.Array]: Mask the attention
                weights

        Returns:
            A dictionary of the past_key_values, attention_mask and
            position ids
        """
        batch_size, seq_length = input_ids.shape

        past_key_values = self.init_cache(batch_size, max_length)
        extended_attention_mask = jnp.ones(
            (batch_size, max_length), dtype="i4")
        if attention_mask is not None:
            position_ids = attention_mask.cumsum(axis=-1) - 1
            extended_attention_mask = jax.lax.dynamic_update_slice(
                extended_attention_mask, attention_mask, (0, 0))
        else:
            position_ids = jnp.broadcast_to(jnp.arange(seq_length, dtype="i4")[
                                            None, :], (batch_size, seq_length))

        return {
            "past_key_values": past_key_values,
            "attention_mask": extended_attention_mask,
            "position_ids": position_ids,
        }

    def update_inputs_for_generation(self, model_outputs, model_kwargs):
        model_kwargs["past_key_values"] = model_outputs.past_key_values
        model_kwargs["position_ids"] = model_kwargs["position_ids"][:, -1:] + 1
        return model_kwargs

    def __call__(
            self,
            input_ids: chex.Array,
            attention_mask: Optional[chex.Array] = None,
            position_ids: Optional[chex.Array] = None,
            params: dict = None,
            past_key_values: dict = None,
            dropout_rng: jax.random.PRNGKey = None,
            train: bool = False,
            output_attentions: Optional[bool] = None,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
            extra_embedding: Optional[Union[jnp.ndarray, None]] = None,
            add_params_field: bool = False,
            vision_mask: Optional[chex.Array] = None,
            **kwargs
    ):
        raise NotImplementedError("Not Implemented Yet")

    def __repr__(self):

        """The __repr__ function is used to generate a string representation of an object.
        This function should return a string that can be parsed by the Python interpreter
        to recreate the object. The __repr__ function is called when you use print() on an
        object, or when you type its name in the REPL.

        Args:
            self: Refer to the instance of the class

        Returns:
            A string representation of the object
        """
        string = f"{self.__class__.__name__}(\n"
        for k, v in self.__dict__.items():
            if not k.startswith("_"):
                try:
                    repr_src = f"\t{k} : " + v.__str__().replace("\n", "\n\t") + "\n"
                    string += repr_src if len(repr_src) < 500 else f"\t{k} : " + f"{v.__class__.__name__}(...)" + "\n"
                except TypeError:
                    pass
        return string + ")"

    def __str__(self):

        """The __str__ function is called when you use the print function or when str() is used.
        It should return a string representation of the object.

        Args:
            self: Refer to the instance of the class

        Returns:
            The object's string representation
        """
        return self.__repr__()

    @property
    def config(self) -> EasyDeLPretrainedConfig:
        return self._config  # type:ignore

    def to_easydel_state(
            self,
            params: flax.core.FrozenDict,
            auto_check_params: bool = True
    ):
        """
        Convert the Model to EasyDeLState
        """
        if auto_check_params:
            gp = params.get("params", None)
            params = flax.core.FrozenDict({"params": params} if gp is None else {"params": gp})
        return EasyDeLState.load(
            apply_fn=self.__call__,
            params=params,
            opt_state=None,
            module_config=self.config,
            module=self,
            step=0
        )

    def to_pytorch(
            self,
            params: flax.core.FrozenDict,
            base_hf_auto_class=AutoModelForCausalLM,
            easystate_to_huggingface_model_kwargs: Optional[dict] = None
    ):
        """
        Return the Huggingface / Pytorch implementation of the model with same weights  (if model is available in HF)
        """

        from ..transform.easydel_transform import easystate_to_huggingface_model
        state = self.to_easydel_state(params=params)
        if easystate_to_huggingface_model_kwargs is None:
            easystate_to_huggingface_model_kwargs = {}

        model_config = state.module_config
        if model_config is None:
            model_config = state.module.config_class
        # model_type = model_config.model_type
        model_class = base_hf_auto_class._model_mapping[type(model_config)]  # noqa
        hf_model = easystate_to_huggingface_model(
            state=state,
            base_huggingface_module=model_class,
            config=model_config,

            **easystate_to_huggingface_model_kwargs
        )
        return hf_model

    @staticmethod
    def to_8bit(params, quantization_fields=None):
        if quantization_fields is None:
            quantization_fields = ["kernel", "embedding"]
        return fjformer.linen.quantize_int8_parameters(quantization_fields, params)
