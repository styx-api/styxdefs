""".. include:: ../../README.md"""  # noqa: D415

from .dummy_runner import (
    DummyRunner,
)
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
    "DummyRunner",
    "get_global_runner",
    "set_global_runner",
    "StyxRuntimeError",
]
