"""Command-line interface for notebookmd.

Provides ``notebookmd run``, ``notebookmd cache``, and ``notebookmd version``
commands.  Inspired by Streamlit's CLI (``streamlit run``).

Usage::

    # Run a report script with live output
    notebookmd run analysis.py --live

    # Run with variable injection
    notebookmd run report.py --var ticker=AAPL --var period=1y

    # Watch mode — re-run automatically on file changes
    notebookmd run report.py --watch

    # Combine features
    notebookmd run analysis.py --live --watch --var ticker=AAPL

    # Cache management
    notebookmd cache show
    notebookmd cache clear

    # Version
    notebookmd version
"""

from __future__ import annotations

import argparse
import hashlib
import logging
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .runner import Runner

logger = logging.getLogger("notebookmd.cli")


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    result: int = args.func(args)
    return result


# ---------------------------------------------------------------------------
# Parser construction
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="notebookmd",
        description="notebookmd — Markdown report generation for AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  notebookmd run analysis.py --live\n"
            "  notebookmd run report.py --watch --var ticker=AAPL\n"
            "  notebookmd cache clear\n"
            "  notebookmd version\n"
        ),
    )

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # ── run ──
    run_parser = sub.add_parser(
        "run",
        help="Execute a notebookmd script",
        description="Execute a Python script that generates a notebookmd report.",
    )
    run_parser.add_argument("script", help="Path to the Python script (.py)")
    run_parser.add_argument(
        "--live",
        action="store_true",
        default=False,
        help="Stream markdown output to stderr in real time",
    )
    run_parser.add_argument(
        "--watch",
        action="store_true",
        default=False,
        help="Watch script file for changes and re-run automatically",
    )
    run_parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Override the output markdown file path",
    )
    run_parser.add_argument(
        "--var",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Inject a variable into the script (can be repeated)",
    )
    run_parser.add_argument(
        "--cache-dir",
        type=str,
        default=None,
        help="Custom cache directory (default: .notebookmd_cache)",
    )
    run_parser.add_argument(
        "--no-cache",
        action="store_true",
        default=False,
        help="Disable caching for this run",
    )
    run_parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging verbosity (default: INFO)",
    )
    run_parser.set_defaults(func=_cmd_run)

    # ── cache ──
    cache_parser = sub.add_parser(
        "cache",
        help="Manage the notebookmd cache",
        description="View or clear cached data.",
    )
    cache_sub = cache_parser.add_subparsers(dest="cache_action")

    show_parser = cache_sub.add_parser("show", help="Display cache statistics")
    show_parser.add_argument("--cache-dir", type=str, default=None)
    show_parser.set_defaults(func=_cmd_cache_show)

    clear_parser = cache_sub.add_parser("clear", help="Clear all cached data")
    clear_parser.add_argument("--cache-dir", type=str, default=None)
    clear_parser.add_argument(
        "--data-only",
        action="store_true",
        default=False,
        help="Only clear data cache, keep resource cache",
    )
    clear_parser.set_defaults(func=_cmd_cache_clear)

    def _cache_help(args: argparse.Namespace) -> int:
        cache_parser.print_help()
        return 0

    cache_parser.set_defaults(func=_cache_help)

    # ── version ──
    ver_parser = sub.add_parser("version", help="Show notebookmd version")
    ver_parser.set_defaults(func=_cmd_version)

    return parser


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def _cmd_run(args: argparse.Namespace) -> int:
    """Execute a notebookmd script."""
    from .runner import RunConfig, Runner

    # Parse --var KEY=VALUE pairs
    variables: dict[str, str] = {}
    for item in args.var:
        if "=" not in item:
            _err(f"Invalid --var format: {item!r}  (expected KEY=VALUE)")
            return 1
        k, v = item.split("=", 1)
        variables[k.strip()] = v.strip()

    config = RunConfig(
        live=args.live,
        output=args.output,
        variables=variables,
        cache_dir=args.cache_dir,
        no_cache=args.no_cache,
        log_level=args.log_level,
    )

    runner = Runner(config)

    if args.watch:
        return _run_watch_loop(runner, args.script)

    result = runner.execute(args.script)
    _print_result(result)
    return 0 if result.ok else 1


def _run_watch_loop(runner: Runner, script_path: str) -> int:
    """Poll-based watch mode: re-run the script when it changes.

    Uses file modification time polling so there's no dependency on watchdog.
    If watchdog is installed, uses its observer for more efficient detection.
    """
    script = Path(script_path).resolve()
    if not script.exists():
        _err(f"Script not found: {script}")
        return 1

    _info(f"Watching {script.name} for changes (Ctrl+C to stop)")

    # Try to use watchdog if available, else fall back to polling
    try:
        return _watch_with_watchdog(runner, script)
    except ImportError:
        return _watch_with_polling(runner, script)


def _watch_with_polling(runner: Runner, script: Path) -> int:
    """Simple polling-based file watcher."""

    last_hash = _file_hash(script)

    # Initial run
    result = runner.execute(str(script))
    _print_result(result)

    try:
        while True:
            time.sleep(1.0)
            current_hash = _file_hash(script)
            if current_hash != last_hash:
                last_hash = current_hash
                _info(f"\nFile changed, re-running {script.name} ...")
                result = runner.execute(str(script))
                _print_result(result)
    except KeyboardInterrupt:
        _info("\nStopped watching.")
        return 0


def _watch_with_watchdog(runner: Runner, script: Path) -> int:
    """File watcher using watchdog library for efficient OS-level file monitoring."""
    from watchdog.events import FileModifiedEvent, FileSystemEventHandler
    from watchdog.observers import Observer

    class ScriptHandler(FileSystemEventHandler):
        def __init__(self) -> None:
            self.changed = False
            self._last_hash = _file_hash(script)

        def on_modified(self, event: FileModifiedEvent) -> None:  # type: ignore[override]
            if Path(str(event.src_path)).resolve() == script:
                new_hash = _file_hash(script)
                if new_hash != self._last_hash:
                    self._last_hash = new_hash
                    self.changed = True

    handler = ScriptHandler()
    observer = Observer()
    observer.schedule(handler, str(script.parent), recursive=False)
    observer.start()

    # Initial run
    result = runner.execute(str(script))
    _print_result(result)

    try:
        while True:
            time.sleep(0.5)
            if handler.changed:
                handler.changed = False
                _info(f"\nFile changed, re-running {script.name} ...")
                result = runner.execute(str(script))
                _print_result(result)
    except KeyboardInterrupt:
        observer.stop()
        _info("\nStopped watching.")
    finally:
        observer.stop()
        observer.join()

    return 0


def _cmd_cache_show(args: argparse.Namespace) -> int:
    """Display cache statistics."""
    from .cache import get_cache_manager

    cache_dir = Path(args.cache_dir) if args.cache_dir else None
    mgr = get_cache_manager(cache_dir=cache_dir)
    info = mgr.summary()

    _info("notebookmd cache")
    _info(f"  Directory: {info['cache_dir']}")
    _info("")
    _info("  Data cache:")
    _info(f"    Memory entries: {info['data']['memory_keys']}")
    _info(f"    Disk entries:   {info['data']['disk_keys']}")
    _info(f"    Hits:           {info['data']['hits']}")
    _info(f"    Misses:         {info['data']['misses']}")
    _info(f"    Hit rate:       {info['data']['hit_rate']}")
    _info("")
    _info("  Resource cache:")
    _info(f"    Memory entries: {info['resource']['memory_keys']}")
    _info(f"    Hits:           {info['resource']['hits']}")
    _info(f"    Misses:         {info['resource']['misses']}")
    _info(f"    Hit rate:       {info['resource']['hit_rate']}")

    return 0


def _cmd_cache_clear(args: argparse.Namespace) -> int:
    """Clear cached data."""
    from .cache import get_cache_manager

    cache_dir = Path(args.cache_dir) if args.cache_dir else None
    mgr = get_cache_manager(cache_dir=cache_dir)

    if args.data_only:
        mgr.clear_data()
        _info("Data cache cleared.")
    else:
        mgr.clear_all()
        _info("All caches cleared.")

    return 0


def _cmd_version(args: argparse.Namespace) -> int:
    """Show version information."""
    from . import __version__

    print(f"notebookmd {__version__}")
    return 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _file_hash(path: Path) -> str:
    """Get a hash of a file's contents for change detection."""
    try:
        return hashlib.md5(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _print_result(result: Any) -> None:
    """Print a RunResult summary to stderr."""
    from .runner import RunStatus

    _info("")
    _info("-" * 50)
    _info(result.summary())
    _info("-" * 50)

    if result.status == RunStatus.ERROR and result.traceback:
        _err(result.traceback)


def _info(msg: str) -> None:
    """Print an info message to stderr."""
    print(msg, file=sys.stderr)


def _err(msg: str) -> None:
    """Print an error message to stderr."""
    print(f"ERROR: {msg}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
