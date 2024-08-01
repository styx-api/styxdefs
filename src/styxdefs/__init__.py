""".. include:: ../../README.md"""  # noqa: D415

from .global_state import (
    get_global_runner,
    set_global_runner,
)
from .local_runner import (
    LocalRunner,
)
from .types import (
    Execution,
    InputPathType,
    Metadata,
    OutputPathType,
    Runner,
    StyxRuntimeError,
)

__all__ = [
    "Execution",
    "InputPathType",
    "Metadata",
    "OutputPathType",
    "Runner",
    "LocalRunner",
    "get_global_runner",
    "set_global_runner",
    "StyxRuntimeError",
]
