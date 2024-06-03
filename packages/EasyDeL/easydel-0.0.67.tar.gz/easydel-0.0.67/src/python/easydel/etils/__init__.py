from ..utils.lazy_import import _LazyModule
from typing import TYPE_CHECKING

_import_structure = {
    "etils": [
        "EasyDeLGradientCheckPointers",
        "EasyDeLOptimizers",
        "EasyDeLSchedulers",
        "AVAILABLE_OPTIMIZERS",
        "AVAILABLE_SCHEDULERS",
        "AVAILABLE_GRADIENT_CHECKPOINTS",
        "define_flags_with_default",
        "set_loggers_level",
        "get_logger"
    ],
    "errors": [
        "EasyDeLTimerError",
        "EasyDeLRuntimeError",
        "EasyDeLSyntaxRuntimeError"
    ],
    "easystate": [
        "EasyDeLState"
    ],
    "partition_module": [
        "PartitionAxis",
        "AxisType"
    ],
    "auto_tx": [
        "get_optimizer_and_scheduler"
    ]
}

if TYPE_CHECKING:
    from .etils import (
        EasyDeLGradientCheckPointers,
        EasyDeLOptimizers,
        EasyDeLSchedulers,
        AVAILABLE_OPTIMIZERS,
        AVAILABLE_SCHEDULERS,
        AVAILABLE_GRADIENT_CHECKPOINTS,
        define_flags_with_default,
        set_loggers_level,
        get_logger
    )
    from .errors import (
        EasyDeLTimerError,
        EasyDeLRuntimeError,
        EasyDeLSyntaxRuntimeError
    )
    from .easystate import (
        EasyDeLState
    )
    from .partition_module import (
        PartitionAxis,
        AxisType
    )
    from .auto_tx import (
        get_optimizer_and_scheduler
    )
else:
    import sys

    sys.modules[__name__] = _LazyModule(__name__, globals()["__file__"], _import_structure, module_spec=__spec__)
