---
name: dashboard
description: Generate a metrics dashboard using notebookmd with KPIs, charts, and data tables. Use when the user wants a dashboard, scorecard, or metrics overview saved as Markdown.
argument-hint: "[metrics source or description]"
allowed-tools: ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]
---

# Metrics Dashboard Generator

Generate a KPI dashboard as a structured Markdown report using `notebookmd`.

## Input

Dashboard: $ARGUMENTS

## Instructions

### 1. Setup

```python
from notebookmd import nb, NotebookConfig

cfg = NotebookConfig(max_table_rows=20)
st = nb("dist/dashboard.md", title="<Dashboard Title>", cfg=cfg)
```

### 2. Dashboard Layout

```python
# Hero Metrics Row
st.section("Key Performance Indicators")
st.metric_row([
    {"label": "Revenue", "value": "$4.2M", "delta": "+18%"},
    {"label": "Users", "value": "34.5K", "delta": "+2,100"},
    {"label": "Conversion", "value": "3.2%", "delta": "+0.4%"},
    {"label": "Churn", "value": "1.8%", "delta": "-0.3%", "delta_color": "inverse"},
])

# Status Badges
st.badge("ON TRACK", style="success")
st.badge("Q4 2026", style="info")

# Trend Charts
st.section("Trends")
st.line_chart(df, x="date", y="revenue", title="Revenue Trend")
st.area_chart(df, x="date", y="users", title="User Growth")
st.bar_chart(df, x="category", y="count", title="Distribution")

# Detailed Metrics
st.section("Detailed Metrics")
st.kv({
    "MRR": "$350K",
    "ARR": "$4.2M",
    "LTV": "$1,200",
    "CAC": "$180",
    "LTV/CAC": "6.7x",
}, title="Unit Economics")

# Period Comparison
st.section("Period Comparison")
st.change("Revenue", current=4_200_000, previous=3_560_000, fmt=",.0f", pct=True)
st.change("Users", current=34_521, previous=32_421, fmt=",d", pct=True)
st.change("Churn", current=0.018, previous=0.021, fmt=".1%", pct=True)

# Rankings
st.section("Top Performers")
st.ranking("Product A", value="$1.2M", rank=1, total=15)
st.ranking("Product B", value="$890K", rank=2, total=15)
st.ranking("Product C", value="$650K", rank=3, total=15)

# Data Tables
st.section("Data Tables")
st.dataframe(summary_df, name="Summary by Segment")

# Alerts
st.section("Alerts & Actions")
st.success("Revenue target exceeded by 12%")
st.warning("Churn rate increasing in Enterprise segment")
st.info("New pricing tier launching next quarter")

# Export
st.export_csv(df, "dashboard_data.csv", name="Dashboard data export")
st.save()
```

### 3. Design Principles

- Lead with the most important metrics at the top (metric_row)
- Use `st.change()` for period-over-period comparisons
- Use `st.ranking()` for leaderboards and rankings
- Use `st.badge()` for status indicators
- Use `st.kv()` for grouped metrics (unit economics, configuration)
- Charts go in a dedicated "Trends" section
- End with alerts, actions, and data exports
- Keep tables concise — use `max_table_rows` to truncate
