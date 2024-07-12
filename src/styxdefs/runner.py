"""Default runner implementation."""

import logging
import os
import pathlib
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from subprocess import PIPE, CalledProcessError, Popen

from .types import Execution, InputPathType, Metadata, OutputPathType, Runner


class _DefaultExecution(Execution):
    """Default execution implementation."""

    def __init__(self, logger: logging.Logger, dir: pathlib.Path) -> None:
        """Initialize the execution."""
        self.logger: logging.Logger = logger
        self.dir: pathlib.Path = dir

        while self.dir.exists():
            self.logger.warning(
                f"Execution directory {self.dir} already exists. Trying another."
            )
            self.dir = self.dir.with_name(f"{self.dir.name}_1")
        self.dir.mkdir(parents=True, exist_ok=True)

    def input_file(self, host_file: InputPathType) -> str:
        """Resolve host input files."""
        return str(pathlib.Path(host_file).absolute())

    def output_file(self, local_file: str, optional: bool = False) -> OutputPathType:
        """Resolve local output files."""
        return self.dir / local_file

    def run(self, cargs: list[str]) -> None:
        """Run the command."""
        self.logger.debug(f"Running command: {cargs} in '{self.dir}'.")

        def _stdout_handler(line: str) -> None:
            self.logger.info(line)

        def _stderr_handler(line: str) -> None:
            self.logger.error(line)

        with Popen(cargs, text=True, stdout=PIPE, stderr=PIPE, cwd=self.dir) as process:
            with ThreadPoolExecutor(2) as pool:  # two threads to handle the streams
                exhaust = partial(pool.submit, partial(deque, maxlen=0))
                exhaust(_stdout_handler(line[:-1]) for line in process.stdout)  # type: ignore
                exhaust(_stderr_handler(line[:-1]) for line in process.stderr)  # type: ignore
        return_code = process.poll()
        if return_code:
            raise CalledProcessError(return_code, process.args)


class DefaultRunner(Runner):
    """Default runner implementation."""

    logger_name = "styx_default_runner"

    def __init__(self, data_dir: InputPathType | None = None) -> None:
        """Initialize the runner."""
        self.data_dir = pathlib.Path(data_dir or "styx_tmp")
        self.uid = os.urandom(8).hex()
        self.execution_counter = 0

        # Configure logger
        self.logger = logging.getLogger(self.logger_name)
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter("[%(levelname).1s] %(message)s")
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def start_execution(self, metadata: Metadata) -> Execution:
        """Start a new execution."""
        self.execution_counter += 1
        return _DefaultExecution(
            logger=self.logger,
            dir=self.data_dir
            / f"{self.uid}_{self.execution_counter - 1}_{metadata.name}",
        )


_DEFAULT_RUNNER: Runner | None = None


def get_global_runner() -> Runner:
    """Get the default runner."""
    global _DEFAULT_RUNNER
    if _DEFAULT_RUNNER is None:
        _DEFAULT_RUNNER = DefaultRunner()
    return _DEFAULT_RUNNER


def set_global_runner(runner: Runner) -> None:
    """Set the default runner."""
    global _DEFAULT_RUNNER
    _DEFAULT_RUNNER = runner
