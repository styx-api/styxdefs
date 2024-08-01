"""Types for styx generated wrappers."""

import pathlib
import shlex
import typing

InputPathType: typing.TypeAlias = pathlib.Path | str
"""Input host file type."""
OutputPathType: typing.TypeAlias = pathlib.Path
"""Output host file type."""


class Execution(typing.Protocol):
    """Execution object used to execute commands.

    Created by `Runner.start_execution()`.
    """

    def input_file(self, host_file: InputPathType) -> str:
        """Resolve host input files.

        Returns a local filepath.
        Called (potentially multiple times) after
        `Runner.start_execution()` and before `Runner.run()`.
        """
        ...

    def run(self, cargs: list[str]) -> None:
        """Run the command.

        Called after all `Execution.input_file()`
        and `Execution.output_file()` calls.
        """
        ...

    def output_file(self, local_file: str, optional: bool = False) -> OutputPathType:
        """Resolve local output files.

        Returns a host filepath.
        Called (potentially multiple times) after all
        `Runner.input_file()` calls.
        """
        ...


class Metadata(typing.NamedTuple):
    """Static tool metadata.

    This is structured static metadata that is known at compile time.
    Runners can use this to set up execution environments.
    """

    id: str
    """Unique identifier of the tool."""
    name: str
    """Name of the tool."""
    package: str | None = None
    """Name of the package that provides the tool."""
    citations: list[str] | None = None
    """List of references to cite when using the tool."""
    container_image_type: str | None = None
    """Type of container image. Example: docker, singularity."""
    container_image_tag: str | None = None
    """Name of an image where the tool is installed and configured.
    Example: bids/mriqc.
    """
    container_image_index: str | None = None
    """Optional index where the image is available, if not the standard location.
    Example: docker.io
    """
    container_image_opts: str | None = None
    """Container-level arguments for the application.
    Example: --privileged
    """


class Runner(typing.Protocol):
    """Runner object used to execute commands.

    Possible examples would be `LocalRunner`,
    `DockerRunner`, `DebugRunner`, ...
    Used as a factory for `Execution` objects.
    """

    def start_execution(self, metadata: Metadata) -> Execution:
        """Start an execution.

        Called before any `Execution.input_file()` calls.
        """
        ...


class StyxRuntimeError(Exception):
    """Styx runtime error.

    Raised when a command reports a non-zero return code.
    """

    def __init__(
        self,
        return_code: int | None = None,
        command_args: list[str] | None = None,
        message_extra: str | None = None,
    ) -> None:
        """Initialize the error."""
        self.return_code = return_code
        self.command_args = command_args

        if return_code is not None:
            message = f"Command failed with return code {return_code}."
        else:
            message = "Command failed."

        if command_args is not None:
            message += f"\n- Command args: {shlex.join(command_args)}"

        if message_extra is not None:
            message += f"\n{message_extra}"

        super().__init__(message)
