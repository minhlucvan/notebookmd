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
n = nb("dist/dashboard.md", title="<Dashboard Title>", cfg=cfg)
```

### 2. Dashboard Layout

```python
# Hero Metrics Row
n.section("Key Performance Indicators")
n.metric_row([
    {"label": "Revenue", "value": "$4.2M", "delta": "+18%"},
    {"label": "Users", "value": "34.5K", "delta": "+2,100"},
    {"label": "Conversion", "value": "3.2%", "delta": "+0.4%"},
    {"label": "Churn", "value": "1.8%", "delta": "-0.3%", "delta_color": "inverse"},
])

# Status Badges
n.badge("ON TRACK", style="success")
n.badge("Q4 2026", style="info")

# Trend Charts
n.section("Trends")
n.line_chart(df, x="date", y="revenue", title="Revenue Trend")
n.area_chart(df, x="date", y="users", title="User Growth")
n.bar_chart(df, x="category", y="count", title="Distribution")

# Detailed Metrics
n.section("Detailed Metrics")
n.kv({
    "MRR": "$350K",
    "ARR": "$4.2M",
    "LTV": "$1,200",
    "CAC": "$180",
    "LTV/CAC": "6.7x",
}, title="Unit Economics")

# Period Comparison
n.section("Period Comparison")
n.change("Revenue", current=4_200_000, previous=3_560_000, fmt=",.0f", pct=True)
n.change("Users", current=34_521, previous=32_421, fmt=",d", pct=True)
n.change("Churn", current=0.018, previous=0.021, fmt=".1%", pct=True)

# Rankings
n.section("Top Performers")
n.ranking("Product A", value="$1.2M", rank=1, total=15)
n.ranking("Product B", value="$890K", rank=2, total=15)
n.ranking("Product C", value="$650K", rank=3, total=15)

# Data Tables
n.section("Data Tables")
n.dataframe(summary_df, name="Summary by Segment")

# Alerts
n.section("Alerts & Actions")
n.success("Revenue target exceeded by 12%")
n.warning("Churn rate increasing in Enterprise segment")
n.info("New pricing tier launching next quarter")

# Export
n.export_csv(df, "dashboard_data.csv", name="Dashboard data export")
n.save()
```

### 3. Design Principles

- Lead with the most important metrics at the top (metric_row)
- Use `n.change()` for period-over-period comparisons
- Use `n.ranking()` for leaderboards and rankings
- Use `n.badge()` for status indicators
- Use `n.kv()` for grouped metrics (unit economics, configuration)
- Charts go in a dedicated "Trends" section
- End with alerts, actions, and data exports
- Keep tables concise — use `max_table_rows` to truncate
