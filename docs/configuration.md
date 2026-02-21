# Configuration

## NotebookConfig

`NotebookConfig` is a dataclass that controls rendering behavior. Pass it when creating a notebook:

```python
from notebookmd import nb, NotebookConfig

cfg = NotebookConfig(
    max_table_rows=50,
    float_format="{:.2f}",
)
n = nb("output/report.md", title="Report", cfg=cfg)
```

### Options

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `max_table_rows` | `int` | `30` | Maximum rows displayed in tables. Tables exceeding this limit get an ellipsis row and a shape note. |
| `float_format` | `str` | `"{:.4f}"` | Format string for floating-point numbers in tables and formatted output. |

### Table Truncation

When a DataFrame has more rows than `max_table_rows`, the table is truncated:

```python
cfg = NotebookConfig(max_table_rows=5)
n = nb("report.md", cfg=cfg)

# If df has 1000 rows, only 5 are shown plus:
# - An ellipsis row (all cells contain "…")
# - A note: "1,000 rows × 8 columns"
n.table(df, name="Large Dataset")
```

You can override per-call:

```python
n.table(df, name="Full Data", max_rows=100)  # Override config
n.table(df, name="Preview", max_rows=5)       # Show just 5
```

### Float Formatting

The `float_format` string is used when rendering numeric values:

```python
# Default: 4 decimal places
cfg = NotebookConfig()  # float_format="{:.4f}"
# 3.14159 → "3.1416"

# Financial: 2 decimal places
cfg = NotebookConfig(float_format="{:.2f}")
# 3.14159 → "3.14"

# Scientific: exponential notation
cfg = NotebookConfig(float_format="{:.2e}")
# 0.000314 → "3.14e-04"
```

## Output Paths

### Markdown Output

The first argument to `nb()` sets where the report is saved:

```python
n = nb("output/report.md")       # Relative path
n = nb("/tmp/report.md")          # Absolute path
n = nb("reports/2024/q4.md")      # Nested directories (created automatically)
```

The output directory is created automatically when `save()` is called.

### Assets Directory

By default, assets (chart images, CSV exports) are saved to an `assets/` subdirectory next to the Markdown file:

```
output/
├── report.md
└── assets/
    ├── chart_1.png
    └── data.csv
```

Override with the `assets_dir` parameter:

```python
# Custom assets directory
n = nb("output/report.md", assets_dir="output/images")

# Result:
# output/
# ├── report.md
# └── images/
#     ├── chart_1.png
#     └── data.csv
```

### Relative Paths in Markdown

All asset references in the generated Markdown use relative paths, so the report and its assets directory can be moved together:

```markdown
![Line Chart](assets/chart_1.png)
```

## Artifacts Index

Every report ends with an automatically generated **Artifacts** section that lists all saved files:

```markdown
## Artifacts

- [assets/chart_1.png](assets/chart_1.png)
- [assets/chart_2.png](assets/chart_2.png)
- [assets/quarterly_data.csv](assets/quarterly_data.csv)
```

If no artifacts were generated, it shows:

```markdown
## Artifacts

_No artifacts generated._
```

## Optional Dependencies

notebookmd is designed with a zero-dependency core. Features that need external packages use lazy imports with graceful fallbacks.

### Without pandas

`table()` and `dataframe()` work **without pandas** using plain Python data (list of dicts, list of lists, column-oriented dicts). pandas is only needed for DataFrame-specific features like `summary()` and `export_csv()`.

```python
# Works without pandas
n.table([{"name": "Alice", "score": 95}], name="Results")

# Requires pandas
n.summary(df)
n.export_csv(df, "data.csv")
```

### Without matplotlib

Chart methods (`line_chart()`, `area_chart()`, `bar_chart()`) work in two modes:

1. **With matplotlib**: Renders a PNG image and saves it to assets
2. **Without matplotlib**: Emits a text description of the chart data with summary statistics

```python
n.line_chart(df, x="date", y="value", title="Trend")

# With matplotlib: saves "assets/chart_1.png" and embeds image link
# Without matplotlib: renders a text description with data stats
```

The `figure()` method requires matplotlib since it directly takes a matplotlib Figure object.

### Without Plotly/Altair

`plotly_chart()` requires `plotly`. For static image export, `kaleido` is also needed (falls back to HTML without it).

`altair_chart()` requires `altair`. For static image export, `vl-convert-python` is needed (falls back to HTML, then JSON spec).

## Environment Variables

| Variable | Description |
|----------|-------------|
| `NOTEBOOKMD_CACHE_DIR` | Override the default cache directory (`.notebookmd_cache`) |

## Environment Patterns

### CI/CD Pipeline

```bash
# Run a report script in CI
notebookmd run reports/daily_metrics.py -o artifacts/daily.md --no-cache
```

```python
from notebookmd import nb, NotebookConfig

cfg = NotebookConfig(max_table_rows=20)
n = nb(
    f"reports/{build_id}/test_results.md",
    title=f"Test Results - Build {build_id}",
    cfg=cfg,
)
```

### Templated Reports

```bash
# Generate reports for different parameters
notebookmd run regional_report.py --var REGION=US -o output/us.md
notebookmd run regional_report.py --var REGION=EU -o output/eu.md
```

```python
from notebookmd import nb
from datetime import date

today = date.today().isoformat()
n = nb(
    f"output/daily_{today}.md",
    title=f"Daily Report - {today}",
)
```

### Development with Live Reload

```bash
# Watch for changes and stream output
notebookmd run my_report.py --watch --live
```

### In-Memory Only

Use `to_markdown()` when you don't need a file:

```python
n = nb("/dev/null", title="Ephemeral Report")
n.metric("Score", "42")
md = n.to_markdown()
# Use md as a string -- no file written
```
