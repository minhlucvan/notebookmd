# notebookmd — AI Agent Data Analysis Skill

> **Markup-to-Markdown toolkit for AI agents.** Use `notebookmd` to produce
> structured Markdown reports with metrics, charts, tables, and analytics —
> the same way a human analyst uses Jupyter, Streamlit, or Excel.

## Quick Start

```python
from notebookmd import nb

n = nb("dist/report.md", title="My Analysis")

n.section("Key Metrics")
n.metric_row([
    {"label": "Revenue", "value": "$4.2M", "delta": "+18%"},
    {"label": "Users", "value": "34.5K", "delta": "+2,100"},
    {"label": "Churn", "value": "1.8%", "delta": "-0.3%", "delta_color": "inverse"},
])

n.section("Revenue Trend")
n.line_chart(df, x="date", y="revenue", title="Monthly Revenue")

n.section("Details")
n.table(df.head(20), name="Top 20 Records")
n.kv({"LTV": "$14,400", "CAC": "$2,100", "LTV/CAC": "6.9x"}, title="Unit Economics")

n.success("Analysis complete!")
n.save()
```

## Installation

```bash
pip install notebookmd              # Core (zero dependencies)
pip install "notebookmd[pandas]"    # + DataFrames, tables, CSV export
pip install "notebookmd[plotting]"  # + matplotlib charts
pip install "notebookmd[all]"       # Everything (pandas, matplotlib, plotly, altair, pillow)
```

## When to Use This Skill

Use `notebookmd` when the task requires:

- Generating a **data analysis report** from CSV, DataFrame, or API data
- Building a **metrics dashboard** with KPIs, deltas, and trends
- Creating a **structured Markdown document** with tables, charts, status indicators
- Producing **reproducible analysis artifacts** (Markdown file + figures + CSV exports)
- Any task where a human would open Jupyter Notebook, Streamlit, or Excel

## Core Concepts

### Factory

```python
from notebookmd import nb, NotebookConfig

cfg = NotebookConfig(
    max_table_rows=30,       # Truncate tables beyond this (default: 30)
    float_format="{:.4f}",   # Number format for floats (default: "{:.4f}")
)
n = nb("dist/report.md", title="Report Title", cfg=cfg)
```

- `out_md` — Path to the output `.md` file (directories created automatically)
- `title` — Report title rendered as `# Title`
- `assets_dir` — Directory for figures/CSVs (default: `<out_dir>/assets/`)
- `cfg` — Optional `NotebookConfig` for rendering settings

### Report Lifecycle

1. **Create** — `n = nb("dist/report.md", title="...")`
2. **Build** — Call `n.*` methods sequentially (no cells, no execution context)
3. **Save** — `n.save()` writes the `.md` file and returns its `Path`

### Optional Dependencies

notebookmd gracefully degrades when optional packages are missing:

| Feature | Requires |
|---------|----------|
| `n.table()`, `n.dataframe()`, `n.summary()` | `pandas` |
| `n.line_chart()`, `n.bar_chart()`, `n.area_chart()` | `pandas`, `matplotlib` |
| `n.plotly_chart()` | `plotly` |
| `n.altair_chart()` | `altair` |
| `n.export_csv()` | `pandas` |

Missing deps produce a clear fallback message in output — they never crash.

## API Overview

### Text Elements

```python
n.title("Title")                           # # Title
n.header("Header")                         # ## Header
n.subheader("Sub")                         # ### Sub
n.caption("Caption text")                  # _Caption text_
n.text("Preformatted text")                # Monospace code block
n.md("**Bold** and _italic_")             # Raw markdown passthrough
n.code("print('hello')", lang="python")   # Syntax-highlighted code block
n.latex(r"\sum_{i=1}^{n} x_i")           # LaTeX math block
n.note("Important note")                  # Blockquote with Note label
n.write("Any text or value")              # Auto-formatted output
n.divider()                                # Horizontal rule ---
```

### Metrics & KPIs

```python
# Single metric with delta indicator
n.metric("Revenue", "$1.2M", delta="+12%")
n.metric("Churn", "2.1%", delta="-0.3%", delta_color="inverse")

# Row of metrics (dashboard-style)
n.metric_row([
    {"label": "Revenue", "value": "$1.2M", "delta": "+12%"},
    {"label": "Profit", "value": "$340K", "delta": "+8%"},
    {"label": "Users", "value": "3,400", "delta": "+200"},
])

# Key-value dictionary display
n.kv({"LTV": "$14,400", "CAC": "$2,100", "Ratio": "6.9x"}, title="Unit Economics")
```

### Data Display

```python
# DataFrames and tables (requires pandas)
n.table(df, name="Table Title", max_rows=30)
n.dataframe(df, name="DataFrame Title")
n.summary(df, title="Auto Summary")           # Shape, nulls, numeric stats

# JSON display
n.json({"key": "value", "nested": {"a": 1}}, expanded=True)
```

### Charts (requires matplotlib)

```python
n.line_chart(df, x="date", y="close", title="Price Trend")
n.bar_chart(df, x="category", y="count", title="Distribution")
n.area_chart(df, x="date", y="volume", title="Volume Over Time")

# Raw matplotlib figure
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(x, y)
n.figure(fig, "chart.png", caption="My Chart")
```

### Analytics Helpers

```python
# Single statistic with formatting
n.stat("Average Price", 95.4, fmt=".2f")
n.stat("Total", 1_234_567, description="All-time total", fmt=",.0f")

# Multiple inline stats
n.stats([
    {"label": "Mean", "value": 95.4, "fmt": ".2f"},
    {"label": "Std", "value": 3.2, "fmt": ".2f"},
    {"label": "N", "value": 1000, "fmt": ",d"},
])

# Period-over-period change
n.change("Revenue", current=1_200_000, previous=1_000_000, fmt=",.0f", pct=True)
# Output: **Revenue**: 1,200,000 (+200,000 / +20.0%)

# Ranking with context
n.ranking("Product A", value="$1.2M", rank=1, total=50)
n.ranking("Strategy X", value="12.3%", rank=3, total=20, percentile=85)

# Status badge
n.badge("BULLISH", style="success")   # success | warning | error | info
```

### Status Messages

```python
n.success("Operation successful!")
n.error("Something failed!")
n.warning("Be careful!")
n.info("For your information...")
n.exception(ValueError("Bad input"))
n.progress(0.75, "Loading data...")
```

### Layout

```python
# Sections (primary organizational unit)
n.section("Section Title")
n.section("Section Title", "Optional description")

# Section as context manager
with n.section("Analysis"):
    n.write("Content inside section")

# Collapsible content
with n.expander("Click to expand", expanded=False):
    n.write("Hidden content")

# Tabs
tabs = n.tabs(["Tab 1", "Tab 2"])
with tabs.tab("Tab 1"):
    n.write("Tab 1 content")

# Columns
cols = n.columns(3)
with cols.col(0):
    n.metric("A", "100")
with cols.col(1):
    n.metric("B", "200")
```

### Export

```python
path = n.save()                                          # Write .md to disk
markdown_string = n.to_markdown()                        # Get markdown as string
n.export_csv(df, "data.csv", name="Full dataset")       # Save CSV artifact
n.connection_status("Database", status="connected")      # Connection indicator
```

## Analysis Workflow

Follow this pattern for every data analysis task:

### Step 1: Load and Inspect

```python
from notebookmd import nb, NotebookConfig
import pandas as pd

cfg = NotebookConfig(max_table_rows=25)
n = nb("dist/analysis.md", title="<Descriptive Title>", cfg=cfg)

df = pd.read_csv("data.csv")

n.section("Data Overview")
n.kv({
    "File": "data.csv",
    "Records": f"{len(df):,}",
    "Columns": str(len(df.columns)),
    "Date Range": f"{df['date'].min()} to {df['date'].max()}",
}, title="Dataset Info")
n.summary(df, title="Statistical Summary")
```

### Step 2: Compute Key Metrics

```python
n.section("Key Metrics")
total = df["revenue"].sum()
avg = df["revenue"].mean()
top = df.groupby("product")["revenue"].sum().idxmax()

n.metric_row([
    {"label": "Total Revenue", "value": f"${total:,.0f}"},
    {"label": "Avg Order", "value": f"${avg:,.2f}"},
    {"label": "Top Product", "value": top},
])
```

### Step 3: Analyze Segments

```python
n.section("Segment Analysis")
by_segment = df.groupby("segment")["revenue"].agg(["sum", "mean", "count"])
by_segment = by_segment.sort_values("sum", ascending=False)
n.table(by_segment.reset_index(), name="Revenue by Segment")

for i, (seg, row) in enumerate(by_segment.iterrows(), 1):
    n.ranking(seg, value=f"${row['sum']:,.0f}", rank=i, total=len(by_segment))
```

### Step 4: Visualize Trends

```python
n.section("Trends")
daily = df.groupby("date")["revenue"].sum().reset_index()
n.line_chart(daily, x="date", y="revenue", title="Daily Revenue")

n.section("Distribution")
n.bar_chart(by_segment.reset_index(), x="segment", y="sum", title="Revenue by Segment")
```

### Step 5: Compare Periods

```python
n.section("Period Comparison")
current_month = df[df["date"] >= "2026-01-01"]["revenue"].sum()
previous_month = df[df["date"] < "2026-01-01"]["revenue"].sum()
n.change("Revenue", current=current_month, previous=previous_month, fmt=",.0f", pct=True)
```

### Step 6: Conclude and Export

```python
n.section("Conclusion")
n.success("Revenue grew 18% MoM — target exceeded!")
n.warning("Monitor churn in Enterprise segment")

n.export_csv(df, "processed_data.csv", name="Processed dataset")
out = n.save()
print(f"Report saved to: {out}")
```

## Design Principles

1. **Lead with metrics** — `metric_row()` at the top for at-a-glance KPIs
2. **Use sections** — `section()` for clear organization; readers scan headings first
3. **Show context** — `change()` for comparisons, `ranking()` for leaderboards
4. **Progressive disclosure** — `expander()` for methodology, raw data, edge cases
5. **Status badges** — `badge()` and `success()/warning()/error()` for actionable signals
6. **Export artifacts** — `export_csv()` for downstream consumption
7. **Keep tables concise** — Use `max_table_rows` to prevent overwhelming output

## Additional Resources

- [reference.md](reference.md) — Complete API reference with all method signatures
- [examples.md](examples.md) — Full working examples (SaaS dashboard, stock analysis, CSV exploration)
- [patterns.md](patterns.md) — Common analysis patterns and recipes
