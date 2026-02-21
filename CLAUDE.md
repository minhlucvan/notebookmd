# notebookmd — Project Instructions

## Overview

notebookmd is a Python package that provides a **Streamlit-like API** for generating structured
Markdown reports. It is designed for AI agents doing data analysis — agents call `n.metric()`,
`n.table()`, `n.line_chart()` etc. and get clean, structured Markdown output.

## Architecture

```
notebookmd/
├── __init__.py      # Public API: nb() factory, Notebook, NotebookConfig
├── core.py          # Notebook class — 913 lines, full Streamlit-compatible API
├── widgets.py       # 40+ widget renderers (metrics, charts, layout, status)
├── emitters.py      # Low-level Markdown emitters (table, figure, code, kv)
├── capture.py       # Stdout/stderr capture utilities
├── assets.py        # AssetManager — saves figures, CSVs, tracks artifacts
└── py.typed         # PEP 561 type checking marker
```

## Key Patterns

### Creating a report
```python
from notebookmd import nb, NotebookConfig

cfg = NotebookConfig(max_table_rows=30)
n = nb("output/report.md", title="My Report", cfg=cfg)

n.section("Section Name")
n.metric("Label", "Value", delta="+10%")
n.table(df, name="Data Table")
n.line_chart(df, x="date", y="value", title="Trend")
n.save()
```

### The `n` variable convention
Always name the Notebook instance `n` (from `nb()`). This keeps code concise and
distinguishes notebookmd from Streamlit's `st` convention.

## Dependencies

- **Core**: Zero dependencies (text/markdown only)
- **pandas**: `pip install "notebookmd[pandas]"` — tables, DataFrames, CSV export
- **matplotlib**: `pip install "notebookmd[plotting]"` — chart images
- **All**: `pip install "notebookmd[all]"`

## Testing

```bash
pytest tests/ -v                    # Run all 128 tests
pytest tests/unit/ -v               # Unit tests only
pytest tests/integration/ -v        # Integration tests only
```

## Code Style

- Python 3.11+, type hints everywhere
- Black formatting (120 char line length)
- isort with black profile
- Docstrings on all public methods

## Important Rules

- Never break the zero-dependency core — pandas/matplotlib must stay optional
- All optional deps use try/except with graceful fallback messages
- Tests must pass with AND without optional dependencies
- Widget methods should mirror Streamlit's API as closely as possible
- The `section()` method is the primary organizational unit (replaces old `cell()` API)
