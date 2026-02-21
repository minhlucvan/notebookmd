"""Script runner with enhanced runtime features.

Executes user scripts in a controlled environment with:
- Live output streaming (real-time markdown rendering to terminal)
- Timing and profiling
- Error handling with structured output
- Variable injection
- Cache integration

Usage (from CLI)::

    notebookmd run analysis.py --live --var ticker=AAPL

Programmatic usage::

    from notebookmd.runner import Runner, RunConfig

    runner = Runner(RunConfig(live=True, variables={"ticker": "AAPL"}))
    result = runner.execute("analysis.py")
"""

from __future__ import annotations

import logging
import os
import sys
import time
import traceback
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, TextIO

logger = logging.getLogger("notebookmd.runner")


class RunStatus(Enum):
    """Outcome of a script execution."""

    SUCCESS = "success"
    ERROR = "error"
    INTERRUPTED = "interrupted"


@dataclass
class RunResult:
    """Result of a script execution."""

    status: RunStatus
    script: str
    output_path: str | None = None
    duration_seconds: float = 0.0
    error: str | None = None
    traceback: str | None = None
    artifacts: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.status == RunStatus.SUCCESS

    def summary(self) -> str:
        """Human-readable summary of the run."""
        lines = []
        icon = {RunStatus.SUCCESS: "[OK]", RunStatus.ERROR: "[FAIL]", RunStatus.INTERRUPTED: "[INTERRUPTED]"}
        lines.append(f"{icon.get(self.status, '[ ]')} {self.script}")
        lines.append(f"  Duration: {self.duration_seconds:.2f}s")
        if self.output_path:
            lines.append(f"  Output:   {self.output_path}")
        if self.artifacts:
            lines.append(f"  Artifacts: {len(self.artifacts)} file(s)")
        if self.error:
            lines.append(f"  Error:    {self.error}")
        return "\n".join(lines)


@dataclass
class RunConfig:
    """Configuration for a script run."""

    live: bool = False
    output: str | None = None
    variables: dict[str, str] = field(default_factory=dict)
    cache_dir: str | None = None
    log_level: str = "INFO"
    no_cache: bool = False
    stream: TextIO | None = None  # Where to write live output (default: stderr)


class LiveWriter:
    """Hooks into Notebook._w() to stream markdown chunks in real time.

    When live mode is enabled, each chunk written to the report buffer is also
    echoed to the terminal so the user sees results as they're generated.
    """

    def __init__(self, stream: TextIO | None = None) -> None:
        self._stream = stream or sys.stderr
        self._total_bytes = 0
        self._chunk_count = 0

    def on_write(self, chunk: str) -> None:
        """Called for every markdown chunk written to the notebook."""
        self._chunk_count += 1
        self._total_bytes += len(chunk.encode("utf-8"))
        try:
            self._stream.write(chunk)
            self._stream.flush()
        except (BrokenPipeError, OSError):
            pass

    @property
    def total_bytes(self) -> int:
        return self._total_bytes

    @property
    def chunk_count(self) -> int:
        return self._chunk_count


class Runner:
    """Execute a notebookmd script with runtime enhancements.

    The runner:
    1. Sets up logging
    2. Configures the cache manager
    3. Injects variables into the script's global namespace
    4. Optionally enables live output streaming
    5. Executes the script
    6. Collects timing and artifact information
    7. Returns a structured RunResult
    """

    def __init__(self, config: RunConfig | None = None) -> None:
        self.config = config or RunConfig()
        self._live_writer: LiveWriter | None = None
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configure logging for the run."""
        level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
            datefmt="%H:%M:%S",
        )

    def execute(self, script_path: str) -> RunResult:
        """Execute a Python script and return the run result.

        Args:
            script_path: Path to the Python script to execute.

        Returns:
            A RunResult with status, timing, and artifact information.
        """
        script = Path(script_path).resolve()
        if not script.exists():
            return RunResult(
                status=RunStatus.ERROR,
                script=str(script),
                error=f"Script not found: {script}",
            )
        if script.suffix != ".py":
            return RunResult(
                status=RunStatus.ERROR,
                script=str(script),
                error=f"Expected a .py file, got: {script.suffix}",
            )

        logger.info("Running %s", script.name)
        start_time = time.monotonic()

        # Set up cache
        if not self.config.no_cache:
            self._setup_cache()

        # Set up live output
        if self.config.live:
            self._live_writer = LiveWriter(stream=self.config.stream)
            self._install_live_hook()

        # Prepare the execution environment
        script_globals = self._build_globals(script)

        try:
            # Change to the script's directory so relative paths work
            original_cwd = os.getcwd()
            os.chdir(script.parent)

            # Add script directory to sys.path
            script_dir = str(script.parent)
            if script_dir not in sys.path:
                sys.path.insert(0, script_dir)

            # Execute the script
            code = compile(script.read_text(encoding="utf-8"), str(script), "exec")
            exec(code, script_globals)

            duration = time.monotonic() - start_time

            # Collect results
            output_path = self._find_output_path(script_globals)
            artifacts = self._collect_artifacts(script_globals)

            logger.info("Completed in %.2fs", duration)
            if output_path:
                logger.info("Output: %s", output_path)

            return RunResult(
                status=RunStatus.SUCCESS,
                script=str(script),
                output_path=output_path,
                duration_seconds=duration,
                artifacts=artifacts,
            )

        except KeyboardInterrupt:
            duration = time.monotonic() - start_time
            logger.warning("Interrupted after %.2fs", duration)
            return RunResult(
                status=RunStatus.INTERRUPTED,
                script=str(script),
                duration_seconds=duration,
            )

        except Exception as exc:
            duration = time.monotonic() - start_time
            tb = traceback.format_exc()
            logger.error("Failed after %.2fs: %s", duration, exc)
            return RunResult(
                status=RunStatus.ERROR,
                script=str(script),
                duration_seconds=duration,
                error=str(exc),
                traceback=tb,
            )

        finally:
            os.chdir(original_cwd)
            self._uninstall_live_hook()

    def _setup_cache(self) -> None:
        """Initialize the cache manager with configured directory."""
        from .cache import get_cache_manager

        cache_dir = Path(self.config.cache_dir) if self.config.cache_dir else None
        get_cache_manager(cache_dir=cache_dir)

    def _install_live_hook(self) -> None:
        """Monkey-patch Notebook._w to also stream live output."""
        from .core import Notebook

        if self._live_writer is None:
            return

        original_w = Notebook._w
        writer = self._live_writer

        def hooked_w(notebook_self: Any, s: str) -> None:
            original_w(notebook_self, s)
            # Also call on_write callback if set on the instance
            if hasattr(notebook_self, "_on_write") and notebook_self._on_write:
                notebook_self._on_write(s)
            writer.on_write(s)

        Notebook._w = hooked_w  # type: ignore[assignment]
        self._original_w = original_w

    def _uninstall_live_hook(self) -> None:
        """Restore original Notebook._w."""
        if hasattr(self, "_original_w"):
            from .core import Notebook

            Notebook._w = self._original_w  # type: ignore[assignment]
            del self._original_w

    def _build_globals(self, script: Path) -> dict[str, Any]:
        """Build the global namespace for the script."""
        g: dict[str, Any] = {
            "__name__": "__main__",
            "__file__": str(script),
            "__builtins__": __builtins__,
        }

        # Inject user-defined variables as NOTEBOOKMD_VAR_<KEY>
        for key, value in self.config.variables.items():
            env_key = f"NOTEBOOKMD_VAR_{key.upper()}"
            os.environ[env_key] = value
            g[key] = value

        return g

    def _find_output_path(self, script_globals: dict[str, Any]) -> str | None:
        """Try to find the output path from the executed script's namespace."""
        from .core import Notebook

        for value in script_globals.values():
            if isinstance(value, Notebook):
                return str(value.out_path)
        return self.config.output

    def _collect_artifacts(self, script_globals: dict[str, Any]) -> list[str]:
        """Collect artifact paths from any Notebook instances in the namespace."""
        from .core import Notebook

        artifacts: list[str] = []
        for value in script_globals.values():
            if isinstance(value, Notebook):
                artifacts.extend(value._asset_mgr.artifacts)
        return artifacts
