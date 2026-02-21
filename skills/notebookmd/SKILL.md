# notebookmd — AI Agent Data Analysis Skill

> **Markup-to-Markdown toolkit for AI agents.** Use `notebookmd` to produce
> structured Markdown reports with metrics, charts, tables, and analytics —
> the same way a human analyst uses Jupyter, Streamlit, or Excel.

## Quick Start

```python
from notebookmd import nb

st = nb("dist/report.md", title="My Analysis")

st.section("Key Metrics")
st.metric_row([
    {"label": "Revenue", "value": "$4.2M", "delta": "+18%"},
    {"label": "Users", "value": "34.5K", "delta": "+2,100"},
    {"label": "Churn", "value": "1.8%", "delta": "-0.3%", "delta_color": "inverse"},
])

st.section("Revenue Trend")
st.line_chart(df, x="date", y="revenue", title="Monthly Revenue")

st.section("Details")
st.table(df.head(20), name="Top 20 Records")
st.kv({"LTV": "$14,400", "CAC": "$2,100", "LTV/CAC": "6.9x"}, title="Unit Economics")

st.success("Analysis complete!")
st.save()
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
st = nb("dist/report.md", title="Report Title", cfg=cfg)
```

- `out_md` — Path to the output `.md` file (directories created automatically)
- `title` — Report title rendered as `# Title`
- `assets_dir` — Directory for figures/CSVs (default: `<out_dir>/assets/`)
- `cfg` — Optional `NotebookConfig` for rendering settings

### Report Lifecycle

1. **Create** — `st = nb("dist/report.md", title="...")`
2. **Build** — Call `st.*` methods sequentially (no cells, no execution context)
3. **Save** — `st.save()` writes the `.md` file and returns its `Path`

### Optional Dependencies

notebookmd gracefully degrades when optional packages are missing:

| Feature | Requires |
|---------|----------|
| `st.table()`, `st.dataframe()`, `st.summary()` | `pandas` |
| `st.line_chart()`, `st.bar_chart()`, `st.area_chart()` | `pandas`, `matplotlib` |
| `st.plotly_chart()` | `plotly` |
| `st.altair_chart()` | `altair` |
| `st.export_csv()` | `pandas` |

Missing deps produce a clear fallback message in output — they never crash.

## API Overview

### Text Elements

```python
st.title("Title")                           # # Title
st.header("Header")                         # ## Header
st.subheader("Sub")                         # ### Sub
st.caption("Caption text")                  # _Caption text_
st.text("Preformatted text")                # Monospace code block
st.md("**Bold** and _italic_")             # Raw markdown passthrough
st.code("print('hello')", lang="python")   # Syntax-highlighted code block
st.latex(r"\sum_{i=1}^{n} x_i")           # LaTeX math block
st.note("Important note")                  # Blockquote with Note label
st.write("Any text or value")              # Auto-formatted output
st.divider()                                # Horizontal rule ---
```

### Metrics & KPIs

```python
# Single metric with delta indicator
st.metric("Revenue", "$1.2M", delta="+12%")
st.metric("Churn", "2.1%", delta="-0.3%", delta_color="inverse")

# Row of metrics (dashboard-style)
st.metric_row([
    {"label": "Revenue", "value": "$1.2M", "delta": "+12%"},
    {"label": "Profit", "value": "$340K", "delta": "+8%"},
    {"label": "Users", "value": "3,400", "delta": "+200"},
])

# Key-value dictionary display
st.kv({"LTV": "$14,400", "CAC": "$2,100", "Ratio": "6.9x"}, title="Unit Economics")
```

### Data Display

```python
# DataFrames and tables (requires pandas)
st.table(df, name="Table Title", max_rows=30)
st.dataframe(df, name="DataFrame Title")
st.summary(df, title="Auto Summary")           # Shape, nulls, numeric stats

# JSON display
st.json({"key": "value", "nested": {"a": 1}}, expanded=True)
```

### Charts (requires matplotlib)

```python
st.line_chart(df, x="date", y="close", title="Price Trend")
st.bar_chart(df, x="category", y="count", title="Distribution")
st.area_chart(df, x="date", y="volume", title="Volume Over Time")

# Raw matplotlib figure
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(x, y)
st.figure(fig, "chart.png", caption="My Chart")
```

### Analytics Helpers

```python
# Single statistic with formatting
st.stat("Average Price", 95.4, fmt=".2f")
st.stat("Total", 1_234_567, description="All-time total", fmt=",.0f")

# Multiple inline stats
st.stats([
    {"label": "Mean", "value": 95.4, "fmt": ".2f"},
    {"label": "Std", "value": 3.2, "fmt": ".2f"},
    {"label": "N", "value": 1000, "fmt": ",d"},
])

# Period-over-period change
st.change("Revenue", current=1_200_000, previous=1_000_000, fmt=",.0f", pct=True)
# Output: **Revenue**: 1,200,000 (+200,000 / +20.0%)

# Ranking with context
st.ranking("Product A", value="$1.2M", rank=1, total=50)
st.ranking("Strategy X", value="12.3%", rank=3, total=20, percentile=85)

# Status badge
st.badge("BULLISH", style="success")   # success | warning | error | info
```

### Status Messages

```python
st.success("Operation successful!")
st.error("Something failed!")
st.warning("Be careful!")
st.info("For your information...")
st.exception(ValueError("Bad input"))
st.progress(0.75, "Loading data...")
```

### Layout

```python
# Sections (primary organizational unit)
st.section("Section Title")
st.section("Section Title", "Optional description")

# Section as context manager
with st.section("Analysis"):
    st.write("Content inside section")

# Collapsible content
with st.expander("Click to expand", expanded=False):
    st.write("Hidden content")

# Tabs
tabs = st.tabs(["Tab 1", "Tab 2"])
with tabs.tab("Tab 1"):
    st.write("Tab 1 content")

# Columns
cols = st.columns(3)
with cols.col(0):
    st.metric("A", "100")
with cols.col(1):
    st.metric("B", "200")
```

### Export

```python
path = st.save()                                          # Write .md to disk
markdown_string = st.to_markdown()                        # Get markdown as string
st.export_csv(df, "data.csv", name="Full dataset")       # Save CSV artifact
st.connection_status("Database", status="connected")      # Connection indicator
```

## Analysis Workflow

Follow this pattern for every data analysis task:

### Step 1: Load and Inspect

```python
from notebookmd import nb, NotebookConfig
import pandas as pd

cfg = NotebookConfig(max_table_rows=25)
st = nb("dist/analysis.md", title="<Descriptive Title>", cfg=cfg)

df = pd.read_csv("data.csv")

st.section("Data Overview")
st.kv({
    "File": "data.csv",
    "Records": f"{len(df):,}",
    "Columns": str(len(df.columns)),
    "Date Range": f"{df['date'].min()} to {df['date'].max()}",
}, title="Dataset Info")
st.summary(df, title="Statistical Summary")
```

### Step 2: Compute Key Metrics

```python
st.section("Key Metrics")
total = df["revenue"].sum()
avg = df["revenue"].mean()
top = df.groupby("product")["revenue"].sum().idxmax()

st.metric_row([
    {"label": "Total Revenue", "value": f"${total:,.0f}"},
    {"label": "Avg Order", "value": f"${avg:,.2f}"},
    {"label": "Top Product", "value": top},
])
```

### Step 3: Analyze Segments

```python
st.section("Segment Analysis")
by_segment = df.groupby("segment")["revenue"].agg(["sum", "mean", "count"])
by_segment = by_segment.sort_values("sum", ascending=False)
st.table(by_segment.reset_index(), name="Revenue by Segment")

for i, (seg, row) in enumerate(by_segment.iterrows(), 1):
    st.ranking(seg, value=f"${row['sum']:,.0f}", rank=i, total=len(by_segment))
```

### Step 4: Visualize Trends

```python
st.section("Trends")
daily = df.groupby("date")["revenue"].sum().reset_index()
st.line_chart(daily, x="date", y="revenue", title="Daily Revenue")

st.section("Distribution")
st.bar_chart(by_segment.reset_index(), x="segment", y="sum", title="Revenue by Segment")
```

### Step 5: Compare Periods

```python
st.section("Period Comparison")
current_month = df[df["date"] >= "2026-01-01"]["revenue"].sum()
previous_month = df[df["date"] < "2026-01-01"]["revenue"].sum()
st.change("Revenue", current=current_month, previous=previous_month, fmt=",.0f", pct=True)
```

### Step 6: Conclude and Export

```python
st.section("Conclusion")
st.success("Revenue grew 18% MoM — target exceeded!")
st.warning("Monitor churn in Enterprise segment")

st.export_csv(df, "processed_data.csv", name="Processed dataset")
out = st.save()
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
