# notebookmd

**A Streamlit-like API for generating structured Markdown reports.**

notebookmd lets you build rich, readable Markdown reports using a familiar API. Call `n.metric()`, `n.table()`, `n.line_chart()`, and 40+ other methods to produce clean, structured output -- no browser or notebook server required.

Designed for AI agents doing data analysis, automated pipelines, and anyone who needs programmatic report generation.

## Key Features

- **Streamlit-compatible API** -- methods like `metric()`, `table()`, `bar_chart()`, `expander()` work the way you expect
- **Zero-dependency core** -- text and Markdown output works with no external packages
- **Tables without pandas** -- pass plain Python dicts, lists, or tuples directly to `table()`
- **Optional integrations** -- pandas for DataFrames, matplotlib for chart images, Plotly and Altair support
- **CLI with live output** -- run scripts via `notebookmd run`, with `--live` streaming and `--watch` mode
- **Caching decorators** -- `@cache_data` and `@cache_resource` for expensive computations (Streamlit-compatible API)
- **Plugin architecture** -- extend with custom widgets via a simple base class
- **Asset management** -- figures, CSVs, and other artifacts are saved and indexed automatically

## Quick Example

```python
from notebookmd import nb

n = nb("output/report.md", title="Sales Report")

n.section("Key Metrics")
n.metric("Revenue", "$1.2M", delta="+12%")
n.metric("Customers", "8,421", delta="+3.2%")

n.section("Monthly Trend")
n.table(monthly_df, name="Monthly Revenue")
n.line_chart(monthly_df, x="month", y="revenue", title="Revenue Over Time")

n.save()
```

This produces a complete Markdown file with formatted metrics, tables, and chart images.

## Documentation

| Page | Description |
|------|-------------|
| [Getting Started](getting-started.md) | Installation, first report, core concepts |
| [CLI Reference](cli.md) | `notebookmd run`, `--live`, `--watch`, cache management |
| [Widgets Reference](widgets.md) | All 48 widget methods organized by category |
| [Caching](caching.md) | `@cache_data`, `@cache_resource`, cache management |
| [Configuration](configuration.md) | NotebookConfig options and asset management |
| [Plugin System](plugins.md) | Custom plugins, registration, and entry points |
| [API Reference](api-reference.md) | Core classes: Notebook, NotebookConfig, AssetManager, Runner |
| [Examples](examples.md) | End-to-end report examples |

## Install

```bash
# Core (zero dependencies)
pip install notebookmd

# With pandas support
pip install "notebookmd[pandas]"

# With chart image rendering
pip install "notebookmd[plotting]"

# Everything
pip install "notebookmd[all]"
```

## Architecture

```
notebookmd/
├── __init__.py          # Public API: nb(), Notebook, NotebookConfig, PluginSpec, cache_data, cache_resource
├── core.py              # Notebook class -- core engine + plugin loading
├── cli.py               # CLI entry point (notebookmd run / cache / version)
├── runner.py            # Script runner with live output and variable injection
├── cache.py             # @cache_data / @cache_resource decorators and cache stores
├── plugins.py           # PluginSpec base class, global registry, entry-point discovery
├── plugins_builtin.py   # 8 built-in plugins (text, data, charts, status, layout, media, analytics, utility)
├── widgets.py           # 40+ widget renderers (metrics, charts, layout, status)
├── emitters.py          # Low-level Markdown emitters (table, figure, code, kv)
├── capture.py           # Stdout/stderr capture utilities
├── assets.py            # AssetManager -- saves figures, CSVs, tracks artifacts
└── py.typed             # PEP 561 type checking marker
```

The package uses a **core + plugin** architecture. The `Notebook` class is a thin core that handles markdown buffering, asset management, and report lifecycle. All widget methods are provided by 8 built-in plugins that are auto-loaded on import. The CLI layer (`cli.py` + `runner.py`) provides script execution with live streaming, file watching, and caching.
