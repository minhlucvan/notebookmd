---
name: notebookmd-guide
description: Reference guide for the notebookmd library API. Use when you need to look up notebookmd widget methods, check API signatures, or understand how to use a specific notebookmd feature. This skill provides the complete API reference.
user-invocable: false
---

# notebookmd API Reference Guide

This is the complete API reference for the `notebookmd` library. Use this when you need
to generate Markdown reports, data analysis, dashboards, or structured documents.

## Installation

```bash
pip install notebookmd              # Core (zero deps)
pip install "notebookmd[pandas]"    # + tables, DataFrames, CSV
pip install "notebookmd[plotting]"  # + matplotlib charts
pip install "notebookmd[all]"       # Everything
```

## Factory

```python
from notebookmd import nb, NotebookConfig

cfg = NotebookConfig(
    max_table_rows=30,       # Default: 30
    float_format="{:.4f}",   # Default: "{:.4f}"
)
n = nb("output/report.md", title="Report Title", cfg=cfg)
```

## Text Elements

```python
n.title("Title")                           # # Title
n.header("Header", divider=False)          # ## Header (+ --- if divider=True)
n.subheader("Sub", divider=False)          # ### Sub
n.caption("Caption text")                  # _Caption text_
n.text("Preformatted text")                # ```text\nPreformatted text\n```
n.latex(r"\sum_{i=1}^{n} x_i")            # $$\sum_{i=1}^{n} x_i$$
n.md("**Bold** and _italic_")             # Raw markdown passthrough
n.code("print('hello')", lang="python")   # ```python\nprint('hello')\n```
n.divider()                                # ---
n.write("Any text or value")              # Auto-formatted
n.note("Important note")                  # > **Note:** Important note
```

## Data Display

```python
# Single metric with delta
n.metric("Revenue", "$1.2M", delta="+12%")
n.metric("Churn", "2.1%", delta="-0.3%", delta_color="inverse")

# Multiple metrics in a row
n.metric_row([
    {"label": "Revenue", "value": "$1.2M", "delta": "+12%"},
    {"label": "Profit", "value": "$340K", "delta": "+8%"},
    {"label": "Users", "value": "3,400", "delta": "+200"},
])

# DataFrames and tables
n.table(df, name="Table Title", max_rows=30)
n.dataframe(df, name="DataFrame Title")
n.summary(df, title="Auto Summary")  # shape, nulls, numeric stats

# Key-value dictionaries
n.kv({"Key1": "Value1", "Key2": "Value2"}, title="Metrics")

# JSON display
n.json({"key": "value", "nested": {"a": 1}}, expanded=True)
```

## Charts (requires matplotlib)

```python
# Convenience chart methods
n.line_chart(df, x="date", y="close", title="Price Trend")
n.bar_chart(df, x="category", y="count", title="Distribution")
n.area_chart(df, x="date", y="volume", title="Volume")

# Raw matplotlib figure
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(x, y)
n.figure(fig, "chart.png", caption="My Chart")

# Plotly (requires plotly)
import plotly.express as px
fig = px.line(df, x="date", y="close")
n.plotly_chart(fig, "interactive.html")

# Altair (requires altair)
import altair as alt
chart = alt.Chart(df).mark_line().encode(x="date", y="close")
n.altair_chart(chart, "vega_chart.png")
```

## Status Elements

```python
n.success("Operation successful!")         # > **Success:** ...
n.error("Something failed!")               # > **Error:** ...
n.warning("Be careful!")                   # > **Warning:** ...
n.info("For your information...")           # > **Info:** ...
n.exception(ValueError("Bad input"))       # > **Error:** ValueError: Bad input
n.progress(0.75, "Loading data...")        # [=============>    ] 75% Loading data...
n.toast("Notification message")            # > **Toast:** ...
n.balloons()                               # Celebration marker
n.snow()                                   # Snow marker
```

## Layout

```python
# Sections (primary organizational unit)
n.section("Section Title")
n.section("Section Title", "Optional description")

# Section as context manager (adds divider on exit)
with n.section("Section Title"):
    n.write("Content inside section")

# Collapsible content
with n.expander("Click to expand", expanded=False):
    n.write("Hidden content")

# Tabs
tabs = n.tabs(["Tab 1", "Tab 2", "Tab 3"])
with tabs.tab("Tab 1"):
    n.write("Tab 1 content")
with tabs.tab("Tab 2"):
    n.write("Tab 2 content")

# Columns
cols = n.columns(3)
with cols.col(0):
    n.metric("A", "100")
with cols.col(1):
    n.metric("B", "200")

# Container
with n.container(border=True):
    n.write("Contained content")
```

## Analytics Helpers

```python
# Single statistic
n.stat("Average Price", 95.4, fmt=".2f")
n.stat("Total", 1_234_567, description="All-time total", fmt=",.0f")

# Multiple inline stats
n.stats([
    {"label": "Mean", "value": 95.4, "fmt": ".2f"},
    {"label": "Std", "value": 3.2, "fmt": ".2f"},
    {"label": "N", "value": 1000, "fmt": ",d"},
])

# Inline badge/pill
n.badge("BULLISH", style="success")    # success, warning, error, info
n.badge("HOLD", style="warning")

# Period-over-period change
n.change("Revenue", current=1_200_000, previous=1_000_000, fmt=",.0f", pct=True)
# Output: **Revenue**: 1,200,000 (+200,000 / +20.0%)

# Ranking with context
n.ranking("Product A", value="$1.2M", rank=1, total=50)
n.ranking("Strategy X", value="12.3%", rank=3, total=20, percentile=85)
```

## Code Display

```python
# Echo: show code + output together
n.echo('df = pd.read_csv("data.csv")\nprint(len(df))', "1234")

# Code block with syntax highlighting
n.code("SELECT * FROM users WHERE active = 1", lang="sql")
```

## Export and Output

```python
# Save report to disk (returns Path)
path = n.save()

# Get markdown as string (no file written)
markdown_string = n.to_markdown()

# Export DataFrame as CSV artifact
n.export_csv(df, "data.csv", name="Full dataset")

# Connection status
n.connection_status("Database", status="connected", details="PostgreSQL 15")
```

## Complete Example

```python
from notebookmd import nb, NotebookConfig
import pandas as pd

cfg = NotebookConfig(max_table_rows=20)
n = nb("dist/report.md", title="Q4 Revenue Analysis", cfg=cfg)

n.section("Overview")
n.metric_row([
    {"label": "Revenue", "value": "$4.2M", "delta": "+18%"},
    {"label": "Customers", "value": "1,234", "delta": "+89"},
    {"label": "ARPU", "value": "$3,400", "delta": "+$200"},
])
n.badge("ON TRACK", style="success")

n.section("Revenue Trend")
n.line_chart(df, x="month", y="revenue", title="Monthly Revenue")

n.section("Top Segments")
n.table(segments_df, name="Revenue by Segment")
n.ranking("Enterprise", "$2.1M", rank=1, total=4)
n.ranking("SMB", "$1.4M", rank=2, total=4)

with n.expander("Methodology"):
    n.write("Revenue calculated as sum of all invoiced amounts...")

n.section("Conclusion")
n.change("Revenue", current=4_200_000, previous=3_560_000, fmt=",.0f", pct=True)
n.success("Q4 target exceeded by 12%!")

n.export_csv(df, "q4_revenue.csv", name="Q4 revenue data")
out = n.save()
```
