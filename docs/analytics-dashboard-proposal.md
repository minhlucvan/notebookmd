# notebookmd Analytics Dashboard — Design Proposal

**Code-first representation layer for agent-driven analytics.**

> Agent writes Python → notebookmd renders Markdown → Analytics happens.

---

## The Core Idea

notebookmd is a **representation layer**. Not a BI tool. Not a query engine. Not a
dashboard server.

It's the thing that turns an AI agent's analysis into a structured, readable, portable
document — instantly, with zero configuration, using pure Python.

```
Agent analyzes data ──► n.metric(), n.table(), n.chart() ──► report.md
```

That's it. That's the product.

### Why This Matters Now

Every AI agent — Claude, GPT, Gemini, open-source models — can already:
- Read CSVs, query databases, call APIs
- Do statistical analysis, find patterns, draw conclusions
- Write Python code fluently

What they **cannot** do is produce structured, presentation-ready output. They `print()`.
They dump raw text. They generate one-off Markdown by hand, inconsistently, every time.

notebookmd gives agents a **standard representation vocabulary**:

```python
n.metric("Revenue", "$4.2M", delta="+18%")    # KPI card
n.table(df, name="Top Products")               # formatted table
n.line_chart(df, x="date", y="value")           # chart image
n.bar_chart(df, x="region", y="sales")          # bar chart
n.badge("HEALTHY", style="success")             # status pill
n.stat("P/E Ratio", "24.5x")                    # inline stat
```

One `pip install`, one `n = nb("report.md")`, and the agent has a full analytics
rendering toolkit. No server. No config. No build step.

---

## What "Code-First Representation Layer" Means

### Code-First

The report is defined entirely in Python. Not YAML. Not SQL. Not drag-and-drop.
An agent writes code; the code produces the report. This is how agents naturally work —
sequentially, imperatively, one function call at a time.

```python
# This IS the dashboard. No config file. No template language. Just Python.
n = nb("output/weekly.md", title="Weekly Dashboard")

n.section("Revenue")
n.metric_row([
    {"label": "This Week", "value": "$142K", "delta": "+12%"},
    {"label": "MTD", "value": "$580K", "delta": "+8%"},
    {"label": "Pipeline", "value": "$1.2M"},
])

n.section("Trend")
n.line_chart(df, x="date", y="revenue", title="Daily Revenue")

n.section("Breakdown")
n.table(by_region, name="Revenue by Region")
n.bar_chart(by_region, x="region", y="revenue")

n.save()
```

### Representation Layer

notebookmd doesn't query data. It doesn't store data. It **represents** data.

The agent is responsible for getting the data (from a database, CSV, API, wherever).
notebookmd is responsible for turning that data into a clean, structured document.

This separation is intentional:
- Agents are already good at getting and analyzing data
- What they lack is a consistent way to **present** it
- notebookmd provides that presentation vocabulary

### Instantly Enables Agent Analytics

No setup required. An agent can go from "zero" to "full analytics dashboard" in one script:

```python
from notebookmd import nb
import pandas as pd

df = pd.read_csv("sales.csv")

n = nb("dashboard.md", title="Sales Dashboard")
n.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
n.metric("Orders", f"{len(df):,}")
n.line_chart(df, x="date", y="revenue", title="Revenue Trend")
n.table(df.head(10), name="Recent Orders")
n.save()
```

That's a complete dashboard. 8 lines. Works immediately. The agent didn't need to learn
a framework, configure a server, or understand a template language.

---

## The Agent → Markdown → Analytics Pipeline

### How It Works Today

```
┌──────────┐         ┌──────────┐         ┌──────────────────┐
│ AI Agent │──code──► │notebookmd│──write──►│ report.md        │
│          │         │          │         │ + assets/         │
│ (Claude, │         │ n.metric │         │   chart_1.png    │
│  GPT,    │         │ n.table  │         │   data.csv       │
│  local)  │         │ n.chart  │         │                  │
└──────────┘         └──────────┘         └──────────────────┘
                                                   │
                                          ┌────────┴────────┐
                                          │                 │
                                     Humans read it    Agents read it
                                     (GitHub, email,   (downstream
                                      Slack, web)       analysis)
```

### What Makes Markdown the Right Output

- **Universal**: renders on GitHub, VS Code, Slack, email, web, PDF
- **Git-friendly**: `git diff` shows exactly what changed between runs
- **LLM-native**: 4-5x more token-efficient than HTML for agent consumption
- **Portable**: no server, no viewer app, no proprietary format
- **Composable**: sections, tables, images, code blocks — all plain text

### The Dual-Audience Advantage

The same `.md` file serves two audiences:

1. **Humans** read the rendered Markdown (tables, charts, metrics)
2. **Agents** parse the raw Markdown (structured, predictable format)

No other format does both well. HTML is verbose for agents. JSON is unreadable for humans.
PDF is opaque to both. Markdown is the sweet spot.

---

## What We Build Next: The Dashboard Layer

notebookmd already has the widget library (40+ methods). The next step is making it trivially
easy for agents to produce **recurring, data-connected dashboards**.

### 1. Data Source Wrappers

Thin convenience layer — not a query engine, just a consistent interface:

```python
from notebookmd.sources import connect

src = connect("data/sales.csv")        # CSV (zero deps)
src = connect("sqlite:///app.db")       # SQLite (zero deps)
src = connect(df)                       # pandas DataFrame

# Schema discovery — agents read this to understand the data
print(src.describe())
# → "sales.csv: 145,230 rows, 8 columns [date, product, region, revenue, ...]"

df = src.query("SELECT region, SUM(revenue) FROM data GROUP BY region")
```

The key insight: agents don't need 200 database connectors. They need a **describe → query → render** loop. The `connect()` wrapper standardizes that loop.

### 2. Data Profiling for Agents

Auto-generate structured hints that agents can use to decide what to visualize:

```python
from notebookmd.discovery import suggest

hints = suggest(src)
# {
#   "kpi_candidates": ["revenue", "order_count"],
#   "time_column": "order_date",
#   "category_columns": ["region", "product_type"],
#   "suggested_charts": [
#     {"type": "line_chart", "x": "order_date", "y": "revenue"},
#     {"type": "bar_chart", "x": "region", "y": "revenue"},
#   ],
# }
```

This turns any dataset into dashboard-ready guidance. The agent reads the hints,
writes the rendering code, notebookmd produces the report.

### 3. Dashboard Templates

Pre-built blueprints for common dashboard patterns:

```python
from notebookmd.dashboard import KPIDashboard

KPIDashboard(
    source=src,
    metrics=["revenue", "orders", "avg_order_value"],
    time_column="order_date",
    group_by="region",
).render(n)
```

| Template | What It Renders |
|----------|----------------|
| `KPIDashboard` | Metric cards + sparklines + period-over-period change |
| `TimeSeriesDashboard` | Line charts + moving averages + seasonality |
| `ComparisonDashboard` | Side-by-side metrics + statistical significance |
| `DataQualityDashboard` | Null rates + type checks + freshness + anomalies |
| `FunnelDashboard` | Stage metrics + drop-off rates + conversion charts |

Templates are just Python classes that call `n.metric()`, `n.table()`, `n.chart()`.
Agents can use them as-is or as starting points for custom dashboards.

### 4. Refresh & Diff

Re-run a dashboard script, track what changed:

```python
from notebookmd.dashboard import refresh

result = refresh("scripts/daily_kpis.py", output="output/daily_kpis.md")
# result.changed → True
# result.alerts → ["Revenue dropped 15% vs yesterday"]
```

```bash
# CLI
notebookmd run scripts/daily_kpis.py --refresh

# Cron
0 9 * * * notebookmd run scripts/daily_kpis.py --refresh --alert-webhook $SLACK_URL
```

Since output is Markdown, `git diff` is the natural change tracker:

```diff
- | **Revenue** | **$1.2M** | ▲ +12% |
+ | **Revenue** | **$1.05M** | ▼ -5% |
```

### 5. Report Metadata

Embed machine-readable context in every report:

```markdown
<!--
notebookmd:dashboard
source: sales.csv
generated: 2026-03-12T09:00:00Z
metrics: [total_revenue, avg_order_value, order_count]
parameters:
  date_range: "2026-03-01..2026-03-12"
-->
```

This enables:
- **Downstream agents** parse the metadata to understand what the report covers
- **Refresh scripts** know what to re-query
- **Report indexes** auto-catalog dashboards across a project

---

## End-to-End: What an Agent Actually Does

```python
from notebookmd import nb
import pandas as pd

# 1. Agent gets data (however it wants — pandas, SQL, API, whatever)
df = pd.read_csv("data/sales.csv")

# 2. Agent analyzes
total = df["revenue"].sum()
by_region = df.groupby("region")["revenue"].sum().reset_index()
trend = df.groupby("date")["revenue"].sum().reset_index()

# 3. Agent renders with notebookmd
n = nb("output/sales_dashboard.md", title="Sales Dashboard")

n.section("Key Metrics")
n.metric("Total Revenue", f"${total:,.0f}", delta="+12%")
n.metric("Orders", f"{len(df):,}", delta="+5%")
n.metric("AOV", f"${total/len(df):,.2f}")

n.section("Revenue Trend")
n.line_chart(trend, x="date", y="revenue", title="Daily Revenue")

n.section("By Region")
n.table(by_region, name="Revenue by Region")
n.bar_chart(by_region, x="region", y="revenue")

n.save()
# → output/sales_dashboard.md (readable by humans and agents)
# → output/assets/chart_1.png, chart_2.png
```

The agent doesn't learn a new paradigm. It writes Python. notebookmd handles the rest.

---

## Implementation Plan

### Phase 1: Data Sources
- `DataSource` protocol (describe → query → render loop)
- `CSVSource` (zero-dep), `SQLSource` (sqlite3 stdlib), `DataFrameSource`
- `connect()` factory with auto-detection
- `DashboardPlugin` with `n.connect()`, `n.source_status()`

### Phase 2: Discovery
- `profiler.py` — column stats, type inference, distributions
- `suggest.py` — AI-friendly chart/metric hints
- `n.source_profile()` integration

### Phase 3: Templates
- `DashboardTemplate` base class
- `KPIDashboard`, `TimeSeriesDashboard`, `ComparisonDashboard`
- `n.auto_dashboard()` one-liner

### Phase 4: Operations
- `refresh()` with metric diff tracking
- `--refresh` CLI flag
- `ReportIndex` for cross-report catalog
- Alert webhooks

---

## Dependency Strategy

Zero-dep core philosophy stays:

| Feature | Core (zero deps) | Optional Extra |
|---------|:-:|:-:|
| CSV source | yes | — |
| SQLite source | yes | — |
| DataFrame source | — | `[pandas]` |
| Charts | — | `[plotting]` |
| Full analytics | — | `[all]` |

---

## The Positioning

notebookmd is not a BI tool. It's not a query engine. It's not a dashboard server.

It's the **code-first representation layer** that instantly gives any AI agent the ability
to produce structured analytics output.

```
Traditional BI:     Human → clicks UI → dashboard (locked in a browser)
Agent analytics:    Agent → writes Python → notebookmd → .md report (portable, everywhere)
```

Every agent framework (LangChain, CrewAI, Claude Code, custom agents) can use notebookmd
today. No integration needed. Just `pip install notebookmd` and start calling `n.metric()`.

**The agent already knows how to analyze data. notebookmd gives it a voice.**
