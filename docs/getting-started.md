# Getting Started

## Installation

notebookmd requires Python 3.11+.

```bash
# Core package (zero dependencies -- text/Markdown output only)
pip install notebookmd

# With pandas support (tables, DataFrames, CSV export)
pip install "notebookmd[pandas]"

# With matplotlib support (chart images)
pip install "notebookmd[plotting]"

# All optional dependencies
pip install "notebookmd[all]"
```

### Dependency Matrix

| Extra | Packages Added | Enables |
|-------|---------------|---------|
| _(core)_ | None | Text, metrics, status, layout widgets |
| `pandas` | pandas | `table()`, `dataframe()`, `summary()`, `export_csv()` |
| `plotting` | matplotlib | `line_chart()`, `area_chart()`, `bar_chart()`, `figure()` |
| `all` | pandas + matplotlib | Everything |

Plotly and Altair are supported but not bundled -- install them separately if needed:

```bash
pip install plotly kaleido   # For plotly_chart()
pip install altair vl-convert-python  # For altair_chart()
```

## Your First Report

```python
from notebookmd import nb

# Create a notebook that writes to output/report.md
n = nb("output/report.md", title="My First Report")

# Add some content
n.section("Overview")
n.md("This report was generated with **notebookmd**.")
n.metric("Status", "OK", delta="+100%")

# Save to disk
n.save()
```

Running this script creates `output/report.md` with a formatted Markdown report.

## Core Concepts

### The `n` Variable Convention

By convention, the Notebook instance is always named `n`. This keeps code concise and distinguishes notebookmd from Streamlit's `st` convention:

```python
# notebookmd
n = nb("report.md", title="Report")
n.metric("Revenue", "$1.2M")

# Compare with Streamlit
# st.metric("Revenue", "$1.2M")
```

### The `nb()` Factory

`nb()` is the primary entry point. It creates a configured `Notebook` instance:

```python
from notebookmd import nb, NotebookConfig

cfg = NotebookConfig(max_table_rows=50, float_format="{:.2f}")
n = nb(
    "output/report.md",     # Output file path
    title="Sales Report",    # Report title (appears as H1)
    assets_dir="output/img", # Where to save figures/CSVs (default: output/assets/)
    cfg=cfg,                 # Optional configuration
)
```

### Sections

Use `n.section()` to organize your report into logical sections. Each section emits an H2 heading:

```python
n.section("Key Metrics")
n.metric("Revenue", "$1.2M")
n.metric("Profit", "$300K")

n.section("Detailed Analysis")
n.table(df, name="Revenue by Region")
```

Sections can also be used as context managers -- the context manager adds a divider when the section ends:

```python
with n.section("Analysis"):
    n.metric("Score", "95")
    n.table(results_df)
# Divider is automatically added here
```

### Saving Output

Two ways to get your report:

```python
# Write to disk
path = n.save()  # Returns Path to the saved file

# Get as string (no file written)
md_text = n.to_markdown()
```

## Building a Report

A typical report follows this pattern:

```python
from notebookmd import nb, NotebookConfig
import pandas as pd

# 1. Load data
df = pd.read_csv("data/sales.csv")

# 2. Create notebook
n = nb("output/sales_report.md", title="Sales Report")

# 3. Add summary metrics
n.section("Summary")
n.metric_row([
    {"label": "Total Revenue", "value": f"${df['revenue'].sum():,.0f}"},
    {"label": "Avg Order", "value": f"${df['revenue'].mean():,.2f}"},
    {"label": "Total Orders", "value": f"{len(df):,}"},
])

# 4. Add tables
n.section("Data")
n.table(df.head(20), name="Recent Orders")

# 5. Add charts
n.section("Trends")
n.line_chart(df, x="date", y="revenue", title="Daily Revenue")

# 6. Add status messages
n.success("Report generated successfully")

# 7. Export artifacts
n.export_csv(df, "sales_data.csv")

# 8. Save
n.save()
```

## What Gets Generated

When you call `n.save()`, notebookmd creates:

1. **The Markdown file** at the path you specified
2. **An assets directory** containing any saved figures (PNG), CSVs, or other artifacts
3. **An artifacts index** at the end of the report listing all generated files

```
output/
├── report.md           # The generated report
└── assets/
    ├── chart_1.png     # Chart images
    ├── chart_2.png
    └── sales_data.csv  # Exported data
```

## Next Steps

- [Widgets Reference](widgets.md) -- see all 48 available methods
- [Configuration](configuration.md) -- customize table limits, float formatting, and asset paths
- [Plugin System](plugins.md) -- extend notebookmd with custom widgets
- [Examples](examples.md) -- full end-to-end report examples
