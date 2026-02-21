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
st = nb("output/report.md", title="Report Title", cfg=cfg)
```

## Text Elements

```python
st.title("Title")                           # # Title
st.header("Header", divider=False)          # ## Header (+ --- if divider=True)
st.subheader("Sub", divider=False)          # ### Sub
st.caption("Caption text")                  # _Caption text_
st.text("Preformatted text")                # ```text\nPreformatted text\n```
st.latex(r"\sum_{i=1}^{n} x_i")            # $$\sum_{i=1}^{n} x_i$$
st.md("**Bold** and _italic_")             # Raw markdown passthrough
st.code("print('hello')", lang="python")   # ```python\nprint('hello')\n```
st.divider()                                # ---
st.write("Any text or value")              # Auto-formatted
st.note("Important note")                  # > **Note:** Important note
```

## Data Display

```python
# Single metric with delta
st.metric("Revenue", "$1.2M", delta="+12%")
st.metric("Churn", "2.1%", delta="-0.3%", delta_color="inverse")

# Multiple metrics in a row
st.metric_row([
    {"label": "Revenue", "value": "$1.2M", "delta": "+12%"},
    {"label": "Profit", "value": "$340K", "delta": "+8%"},
    {"label": "Users", "value": "3,400", "delta": "+200"},
])

# DataFrames and tables
st.table(df, name="Table Title", max_rows=30)
st.dataframe(df, name="DataFrame Title")
st.summary(df, title="Auto Summary")  # shape, nulls, numeric stats

# Key-value dictionaries
st.kv({"Key1": "Value1", "Key2": "Value2"}, title="Metrics")

# JSON display
st.json({"key": "value", "nested": {"a": 1}}, expanded=True)
```

## Charts (requires matplotlib)

```python
# Convenience chart methods
st.line_chart(df, x="date", y="close", title="Price Trend")
st.bar_chart(df, x="category", y="count", title="Distribution")
st.area_chart(df, x="date", y="volume", title="Volume")

# Raw matplotlib figure
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(x, y)
st.figure(fig, "chart.png", caption="My Chart")

# Plotly (requires plotly)
import plotly.express as px
fig = px.line(df, x="date", y="close")
st.plotly_chart(fig, "interactive.html")

# Altair (requires altair)
import altair as alt
chart = alt.Chart(df).mark_line().encode(x="date", y="close")
st.altair_chart(chart, "vega_chart.png")
```

## Status Elements

```python
st.success("Operation successful!")         # > **Success:** ...
st.error("Something failed!")               # > **Error:** ...
st.warning("Be careful!")                   # > **Warning:** ...
st.info("For your information...")           # > **Info:** ...
st.exception(ValueError("Bad input"))       # > **Error:** ValueError: Bad input
st.progress(0.75, "Loading data...")        # [=============>    ] 75% Loading data...
st.toast("Notification message")            # > **Toast:** ...
st.balloons()                               # Celebration marker
st.snow()                                   # Snow marker
```

## Layout

```python
# Sections (primary organizational unit)
st.section("Section Title")
st.section("Section Title", "Optional description")

# Section as context manager (adds divider on exit)
with st.section("Section Title"):
    st.write("Content inside section")

# Collapsible content
with st.expander("Click to expand", expanded=False):
    st.write("Hidden content")

# Tabs
tabs = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
with tabs.tab("Tab 1"):
    st.write("Tab 1 content")
with tabs.tab("Tab 2"):
    st.write("Tab 2 content")

# Columns
cols = st.columns(3)
with cols.col(0):
    st.metric("A", "100")
with cols.col(1):
    st.metric("B", "200")

# Container
with st.container(border=True):
    st.write("Contained content")
```

## Analytics Helpers

```python
# Single statistic
st.stat("Average Price", 95.4, fmt=".2f")
st.stat("Total", 1_234_567, description="All-time total", fmt=",.0f")

# Multiple inline stats
st.stats([
    {"label": "Mean", "value": 95.4, "fmt": ".2f"},
    {"label": "Std", "value": 3.2, "fmt": ".2f"},
    {"label": "N", "value": 1000, "fmt": ",d"},
])

# Inline badge/pill
st.badge("BULLISH", style="success")    # success, warning, error, info
st.badge("HOLD", style="warning")

# Period-over-period change
st.change("Revenue", current=1_200_000, previous=1_000_000, fmt=",.0f", pct=True)
# Output: **Revenue**: 1,200,000 (+200,000 / +20.0%)

# Ranking with context
st.ranking("Product A", value="$1.2M", rank=1, total=50)
st.ranking("Strategy X", value="12.3%", rank=3, total=20, percentile=85)
```

## Code Display

```python
# Echo: show code + output together
st.echo('df = pd.read_csv("data.csv")\nprint(len(df))', "1234")

# Code block with syntax highlighting
st.code("SELECT * FROM users WHERE active = 1", lang="sql")
```

## Export and Output

```python
# Save report to disk (returns Path)
path = st.save()

# Get markdown as string (no file written)
markdown_string = st.to_markdown()

# Export DataFrame as CSV artifact
st.export_csv(df, "data.csv", name="Full dataset")

# Connection status
st.connection_status("Database", status="connected", details="PostgreSQL 15")
```

## Complete Example

```python
from notebookmd import nb, NotebookConfig
import pandas as pd

cfg = NotebookConfig(max_table_rows=20)
st = nb("dist/report.md", title="Q4 Revenue Analysis", cfg=cfg)

st.section("Overview")
st.metric_row([
    {"label": "Revenue", "value": "$4.2M", "delta": "+18%"},
    {"label": "Customers", "value": "1,234", "delta": "+89"},
    {"label": "ARPU", "value": "$3,400", "delta": "+$200"},
])
st.badge("ON TRACK", style="success")

st.section("Revenue Trend")
st.line_chart(df, x="month", y="revenue", title="Monthly Revenue")

st.section("Top Segments")
st.table(segments_df, name="Revenue by Segment")
st.ranking("Enterprise", "$2.1M", rank=1, total=4)
st.ranking("SMB", "$1.4M", rank=2, total=4)

with st.expander("Methodology"):
    st.write("Revenue calculated as sum of all invoiced amounts...")

st.section("Conclusion")
st.change("Revenue", current=4_200_000, previous=3_560_000, fmt=",.0f", pct=True)
st.success("Q4 target exceeded by 12%!")

st.export_csv(df, "q4_revenue.csv", name="Q4 revenue data")
out = st.save()
```
