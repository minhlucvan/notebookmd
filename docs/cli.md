# CLI Reference

notebookmd includes a command-line interface for running report scripts, managing the cache, and checking the version.

## Installation

The CLI is installed automatically with the package:

```bash
pip install notebookmd
notebookmd version
```

## Commands

### `notebookmd run`

Execute a Python script that generates a notebookmd report.

```bash
notebookmd run <script.py> [options]
```

#### Options

| Flag | Description |
|------|-------------|
| `--live` | Stream Markdown output to stderr in real time |
| `--watch` | Watch the script file for changes and re-run automatically |
| `--output PATH`, `-o PATH` | Override the output Markdown file path |
| `--var KEY=VALUE` | Inject a variable into the script (repeatable) |
| `--cache-dir PATH` | Custom cache directory (default: `.notebookmd_cache`) |
| `--no-cache` | Disable caching for this run |
| `--log-level LEVEL` | Logging verbosity: `DEBUG`, `INFO`, `WARNING`, `ERROR` (default: `INFO`) |

#### Basic Usage

```bash
# Run a report script
notebookmd run analysis.py

# Stream output to terminal as it's generated
notebookmd run analysis.py --live

# Override the output path
notebookmd run analysis.py -o reports/custom_output.md
```

#### Live Output

The `--live` flag streams Markdown chunks to stderr as they are generated, so you can watch the report build in real time:

```bash
notebookmd run analysis.py --live
```

This works by hooking into the `Notebook._w()` method and echoing each chunk to stderr while the script runs. The final report is still saved to the file specified in the script.

#### Watch Mode

The `--watch` flag monitors the script file for changes and automatically re-runs it:

```bash
notebookmd run analysis.py --watch
notebookmd run analysis.py --watch --live  # Combine with live output
```

For efficient file watching, install the `watchdog` extra:

```bash
pip install "notebookmd[watch]"
```

Without watchdog, notebookmd falls back to simple polling.

#### Variable Injection

Use `--var` to inject variables into the script's global namespace:

```bash
notebookmd run analysis.py --var TICKER=AAPL --var PERIOD=quarterly
```

In your script, these are available as global variables:

```python
# analysis.py
from notebookmd import nb

# TICKER and PERIOD are injected by the CLI
n = nb(f"output/{TICKER}_report.md", title=f"{TICKER} Analysis")
n.section(f"{PERIOD.title()} Results")
# ...
n.save()
```

### `notebookmd cache`

Manage the notebookmd cache.

#### `notebookmd cache show`

Display cache statistics:

```bash
notebookmd cache show
notebookmd cache show --cache-dir /custom/cache
```

Shows hit/miss counts, cache size, and eviction statistics for both data and resource caches.

#### `notebookmd cache clear`

Clear all cached data:

```bash
notebookmd cache clear
notebookmd cache clear --data-only    # Only clear data cache, keep resources
notebookmd cache clear --cache-dir /custom/cache
```

### `notebookmd version`

Print the installed notebookmd version:

```bash
notebookmd version
# notebookmd 0.3.0
```

## Runner

The CLI is built on top of the `Runner` class, which can also be used programmatically.

### `RunConfig`

```python
from notebookmd.runner import Runner, RunConfig

config = RunConfig(
    live=True,            # Stream output to stderr
    output="report.md",   # Override output path
    variables={"KEY": "VALUE"},  # Inject variables
    cache_dir=".cache",   # Custom cache directory
    no_cache=False,       # Disable caching
    log_level="INFO",     # Logging level
)
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `live` | `bool` | `False` | Stream Markdown to stderr |
| `output` | `str \| None` | `None` | Override output file path |
| `variables` | `dict[str, str]` | `{}` | Variables injected into script globals |
| `cache_dir` | `str \| None` | `None` | Custom cache directory |
| `log_level` | `str` | `"INFO"` | Logging verbosity |
| `no_cache` | `bool` | `False` | Disable caching |
| `stream` | `TextIO \| None` | `None` | Where to write live output (default: stderr) |

### `RunResult`

```python
from notebookmd.runner import RunResult, RunStatus
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | `RunStatus` | `SUCCESS`, `ERROR`, or `INTERRUPTED` |
| `script` | `str` | Path to the executed script |
| `output_path` | `str \| None` | Path to the generated Markdown file |
| `duration_seconds` | `float` | Execution time |
| `error` | `str \| None` | Error message if failed |
| `traceback` | `str \| None` | Full traceback if failed |
| `artifacts` | `list[str]` | List of generated artifact paths |
| `ok` | `bool` | Property: `True` if status is `SUCCESS` |

### Programmatic Usage

```python
from notebookmd.runner import Runner, RunConfig

config = RunConfig(live=True)
runner = Runner(config)
result = runner.execute("analysis.py")

if result.ok:
    print(f"Report saved to {result.output_path}")
    print(f"Generated {len(result.artifacts)} artifacts")
    print(f"Completed in {result.duration_seconds:.1f}s")
else:
    print(f"Error: {result.error}")
```

## Examples

### CI/CD Integration

```bash
# In your CI pipeline
notebookmd run reports/daily_metrics.py -o artifacts/daily.md --no-cache
```

### Development Workflow

```bash
# Live-reload while developing a report
notebookmd run my_report.py --watch --live
```

### Parameterized Reports

```bash
# Generate reports for different configurations
for region in US EU APAC; do
    notebookmd run regional_report.py --var REGION=$region -o "output/${region}.md"
done
```
