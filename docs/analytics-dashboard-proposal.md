# notebookmd Analytics Dashboard — Design Proposal

**The Markdown-native BI layer for AI agents.**

> Think Metabase meets Evidence.dev — but zero-server, agent-first, and outputs pure Markdown.

---

## The Opportunity

Today's BI tools (PowerBI, Metabase, Looker, Dash) solve the **human dashboard** problem:
connect to databases, build visualizations, share interactive dashboards. But they all assume
a human is clicking buttons in a browser.

AI agents don't click. They write code. They need:

1. **Declarative data source connections** — point at a database/CSV/API, get a DataFrame
2. **Auto-discovery** — "what tables exist? what columns? what's interesting?"
3. **Templated dashboards** — reusable report blueprints that agents can fill in
4. **Scheduled refresh** — re-run analysis on a cron, diff the output
5. **Markdown output** — readable by humans, parseable by other agents, committable to git

**notebookmd already has the best report generation layer for agents.** The missing piece is
the **data source → analysis → dashboard** pipeline that makes it a complete BI tool.

---

## Competitive Landscape

| Tool | Strengths | Gaps for AI Agents |
|------|-----------|-------------------|
| **Metabase** | Auto-discovers tables, SQL-native, beautiful UI | Requires server, no programmatic API, no Markdown output |
| **PowerBI** | Enterprise connectors, DAX expressions | Windows-centric, proprietary format, no agent API |
| **Dash (Plotly)** | Python-native, custom layouts | Requires running server, callback-based, no static output |
| **Streamlit** | Familiar API, Python-native | Requires running server, no static output, no data source layer |
| **Evidence.dev** | Markdown + SQL, git-friendly, static | Node.js ecosystem, not Python, no agent API, requires build step |
| **Julius AI** | AI-native analysis | Proprietary, cloud-only, no self-hosted option |
| **notebookmd** | Agent-first, zero-dep, Markdown output | **No data source layer, no auto-discovery, no dashboard templates** |

### The Gap

No tool exists that gives AI agents:
- **Python-native data source connectors** with zero config
- **Schema auto-discovery** that agents can reason about
- **Dashboard-as-code templates** in pure Markdown
- **Static output** that doesn't need a running server
- **Diff-friendly** reports for tracking changes over time

---

## Proposed Feature: `notebookmd.sources` + Dashboard Templates

### Architecture Overview

```
notebookmd/
├── sources/                  # NEW: Data source connectors
│   ├── __init__.py           # DataSource base, connect(), registry
│   ├── _base.py              # DataSource protocol + schema discovery
│   ├── csv_source.py         # CSV/Parquet file connector
│   ├── sql_source.py         # SQLite/PostgreSQL/MySQL connector
│   ├── api_source.py         # REST API connector (JSON endpoints)
│   └── dataframe_source.py   # In-memory DataFrame wrapper
├── discovery/                # NEW: Auto-discovery & profiling
│   ├── __init__.py
│   ├── profiler.py           # Column stats, distributions, anomalies
│   └── suggest.py            # AI-friendly schema summaries
├── dashboard/                # NEW: Dashboard templates
│   ├── __init__.py           # dashboard() factory
│   ├── templates.py          # Built-in templates (KPI, timeseries, comparison)
│   └── refresh.py            # Scheduled refresh / diff tracking
├── plugins/
│   ├── dashboard.py          # NEW: DashboardPlugin for Notebook
│   └── ...existing plugins
└── ...existing files
```

---

### 1. Data Sources (`notebookmd.sources`)

A thin, zero-dependency-core connector layer. Each source implements a simple protocol:

```python
from notebookmd.sources import connect

# CSV files
src = connect("data/sales.csv")
src = connect("s3://bucket/data.parquet")  # with [cloud] extra

# SQL databases
src = connect("sqlite:///app.db")
src = connect("postgresql://user:pass@host/db")  # with [sql] extra

# REST APIs
src = connect("https://api.example.com/v1/metrics", format="json")

# In-memory DataFrames
src = connect(df)  # wrap an existing pandas DataFrame
```

#### DataSource Protocol

```python
from dataclasses import dataclass
from typing import Protocol

@dataclass
class ColumnInfo:
    name: str
    dtype: str                  # "int64", "float64", "object", "datetime64", etc.
    nullable: bool
    sample_values: list         # 3-5 example values
    stats: dict | None = None   # min, max, mean, unique_count, null_pct

@dataclass
class TableInfo:
    name: str
    columns: list[ColumnInfo]
    row_count: int
    description: str = ""

class DataSource(Protocol):
    """What every data source must implement."""

    def tables(self) -> list[str]:
        """List available tables/datasets."""
        ...

    def schema(self, table: str = None) -> list[TableInfo]:
        """Get schema info — the key method for AI agent discovery."""
        ...

    def query(self, sql_or_filter: str) -> "DataFrame":
        """Fetch data. SQL for databases, filter expressions for files."""
        ...

    def profile(self, table: str = None, sample_size: int = 1000) -> dict:
        """Quick statistical profile of the data."""
        ...

    def describe(self) -> str:
        """Human/agent-readable summary of this data source."""
        ...
```

#### Why This Matters for Agents

An agent can now do:

```python
src = connect("sqlite:///sales.db")

# Agent reads this to understand what data is available
print(src.describe())
# Output:
# Database: sales.db (SQLite)
# Tables: orders (145,230 rows), customers (12,891 rows), products (487 rows)
# Key columns: orders.total (float, $12-$4,500), orders.date (2023-01 to 2026-03)

# Agent decides what to query
df = src.query("SELECT date, SUM(total) as revenue FROM orders GROUP BY date")
```

This is the **Metabase auto-discovery experience**, but as a Python API that agents can call.

---

### 2. Data Profiling & Discovery (`notebookmd.discovery`)

Auto-generate data profiles that agents (and humans) can reason about:

```python
from notebookmd.sources import connect
from notebookmd.discovery import profile, suggest

src = connect("data/sales.csv")

# Full statistical profile
prof = profile(src)
# Returns: column types, distributions, correlations, outliers, missing data patterns

# AI-friendly suggestions (the killer feature)
suggestions = suggest(src)
# Returns structured hints like:
# {
#   "kpi_candidates": ["revenue", "order_count", "avg_order_value"],
#   "time_column": "order_date",
#   "category_columns": ["region", "product_type"],
#   "suggested_charts": [
#     {"type": "line_chart", "x": "order_date", "y": "revenue", "reason": "time series trend"},
#     {"type": "bar_chart", "x": "region", "y": "revenue", "reason": "categorical comparison"},
#   ],
#   "suggested_metrics": [
#     {"label": "Total Revenue", "expr": "revenue.sum()", "format": "$,.0f"},
#     {"label": "Avg Order", "expr": "order_value.mean()", "format": "$,.2f"},
#   ],
#   "anomalies": ["revenue has 3 outliers > 3σ on 2026-01-15, 2026-02-03, 2026-02-28"],
# }
```

This lets an agent go from "here's a CSV" to "here's a full dashboard" with **zero human input**.

---

### 3. Dashboard Templates (`notebookmd.dashboard`)

Pre-built, composable dashboard blueprints that agents can invoke:

```python
from notebookmd import nb
from notebookmd.sources import connect
from notebookmd.dashboard import KPIDashboard, TimeSeriesDashboard, ComparisonDashboard

src = connect("data/sales.csv")

# One-liner: auto-generate a KPI dashboard
n = nb("output/sales_dashboard.md", title="Sales Dashboard")
KPIDashboard(
    source=src,
    metrics=["revenue", "orders", "avg_order_value"],
    time_column="order_date",
    group_by="region",
).render(n)
n.save()
```

#### Built-in Templates

| Template | Use Case | What It Generates |
|----------|----------|-------------------|
| `KPIDashboard` | Executive summary | Metric cards, sparklines, period-over-period change |
| `TimeSeriesDashboard` | Trend analysis | Line charts, moving averages, seasonality detection |
| `ComparisonDashboard` | A/B or segment comparison | Side-by-side metrics, statistical significance |
| `DataQualityDashboard` | Data health monitoring | Null rates, type mismatches, freshness, anomalies |
| `FunnelDashboard` | Conversion/pipeline analysis | Stage metrics, drop-off rates, conversion charts |
| `FinancialDashboard` | Revenue/P&L reporting | Revenue breakdown, margin analysis, forecasts |

#### Custom Templates

```python
from notebookmd.dashboard import DashboardTemplate

class ChurnDashboard(DashboardTemplate):
    """Custom template for churn analysis."""

    name = "churn"
    required_columns = ["customer_id", "signup_date", "last_active", "plan"]

    def render(self, n):
        df = self.source.query("SELECT * FROM customers")

        n.section("Churn Overview")
        n.metric_row([
            {"label": "Total Customers", "value": f"{len(df):,}"},
            {"label": "Churn Rate", "value": f"{self.calc_churn(df):.1%}"},
            {"label": "At Risk", "value": f"{self.at_risk_count(df):,}"},
        ])

        n.section("Churn by Cohort")
        n.bar_chart(self.cohort_analysis(df), x="cohort", y="churn_rate")
        # ...
```

---

### 4. Dashboard Plugin for Notebook (`plugins/dashboard.py`)

Integrate dashboard features directly into the Notebook API:

```python
n = nb("output/report.md", title="Weekly Report")

# Connect data sources inline
n.connect("sales", "sqlite:///sales.db")
n.connect("web", "data/web_analytics.csv")

# Source status indicator (uses existing connection_status widget)
n.source_status()  # Shows: 🟢 sales (SQLite, 3 tables) · 🟢 web (CSV, 145K rows)

# Auto-profile a source
n.source_profile("sales")  # Generates schema + stats section

# Quick dashboard from source
n.auto_dashboard("sales", template="kpi", metrics=["revenue", "orders"])

# Query and display
df = n.source("sales").query("SELECT * FROM orders WHERE date > '2026-01-01'")
n.table(df, name="Recent Orders")
```

---

### 5. Refresh & Diff Tracking (`notebookmd.dashboard.refresh`)

The killer feature for **operational dashboards**: re-run and track changes.

```python
from notebookmd.dashboard import refresh

# Re-run a dashboard script and generate a diff
result = refresh("scripts/daily_kpis.py", output="output/daily_kpis.md")

# result.changed == True if metrics shifted
# result.diff == markdown-formatted diff of key metrics
# result.alerts == ["Revenue dropped 15% vs yesterday"]
```

**CLI integration:**

```bash
# Run dashboard with refresh tracking
notebookmd run scripts/daily_kpis.py --refresh

# Schedule with cron
0 9 * * * notebookmd run scripts/daily_kpis.py --refresh --alert-webhook $SLACK_URL
```

**Git-friendly diffs:**

Since output is Markdown, `git diff` shows exactly what changed:

```diff
- | **Revenue** | **$1.2M** | ▲ +12% |
+ | **Revenue** | **$1.05M** | ▼ -5% |
```

---

## End-to-End Example: Agent Workflow

Here's what the complete experience looks like for an AI agent:

```python
from notebookmd import nb
from notebookmd.sources import connect
from notebookmd.discovery import suggest

# 1. Connect to data
src = connect("postgresql://analytics:pass@host/warehouse")

# 2. Discover what's available (agent reads this)
schema = src.describe()
hints = suggest(src, table="orders")

# 3. Build the dashboard
n = nb("output/weekly_dashboard.md", title="Weekly Business Dashboard")

n.section("Data Sources")
n.connection_status("warehouse", "connected", f"{src.tables().__len__()} tables")

n.section("Key Metrics")
df_kpis = src.query("""
    SELECT
        SUM(revenue) as total_revenue,
        COUNT(*) as order_count,
        AVG(revenue) as avg_order
    FROM orders
    WHERE date >= CURRENT_DATE - INTERVAL '7 days'
""")
n.metric_row([
    {"label": "Revenue", "value": f"${df_kpis['total_revenue'][0]:,.0f}",
     "delta": "+12%"},
    {"label": "Orders", "value": f"{df_kpis['order_count'][0]:,}"},
    {"label": "AOV", "value": f"${df_kpis['avg_order'][0]:,.2f}"},
])

n.section("Revenue Trend")
df_trend = src.query("""
    SELECT date, SUM(revenue) as daily_revenue
    FROM orders GROUP BY date ORDER BY date
""")
n.line_chart(df_trend, x="date", y="daily_revenue", title="Daily Revenue (Last 30 Days)")

n.section("Top Products")
df_products = src.query("""
    SELECT product_name, SUM(revenue) as revenue, COUNT(*) as orders
    FROM orders JOIN products USING(product_id)
    GROUP BY product_name ORDER BY revenue DESC LIMIT 10
""")
n.table(df_products, name="Top 10 Products by Revenue")
n.bar_chart(df_products, x="product_name", y="revenue", title="Revenue by Product")

n.section("Data Quality")
n.badge("HEALTHY", style="success")
n.stat("Freshness", "2 hours ago", description="Last data update")
n.stat("Completeness", "99.7%", description="Non-null rate across key columns")

n.save()
```

**Output:** A clean, self-contained `weekly_dashboard.md` with tables, charts, KPIs — no
server required, git-committable, readable by any LLM.

---

## Implementation Plan

### Phase 1: Data Sources (Core)
- `DataSource` protocol and base class
- `CSVSource` — CSV/TSV/Parquet file connector (zero-dep for CSV, optional for Parquet)
- `DataFrameSource` — wrap existing pandas DataFrames
- `connect()` factory with URL-scheme detection
- `DashboardPlugin` with `n.connect()`, `n.source()`, `n.source_status()`

### Phase 2: SQL & Discovery
- `SQLSource` — SQLite (stdlib), PostgreSQL/MySQL with optional deps
- `profiler.py` — column statistics, type inference, distribution summaries
- `suggest.py` — AI-friendly hints (KPI candidates, chart suggestions)
- `n.source_profile()` integration

### Phase 3: Dashboard Templates
- `DashboardTemplate` base class
- `KPIDashboard`, `TimeSeriesDashboard`, `ComparisonDashboard`
- `n.auto_dashboard()` one-liner
- Template gallery in docs

### Phase 4: Refresh & Operations
- `refresh()` function with metric diff tracking
- `--refresh` CLI flag
- Alert webhooks (Slack, email, generic HTTP)
- Cron-friendly execution mode

### Phase 5: Advanced Sources
- `APISource` — REST API connector with pagination
- Cloud storage (S3, GCS) with `[cloud]` extra
- DuckDB integration for fast local analytics
- Community source plugins via entry points

---

## Dependency Strategy

Stays true to notebookmd's zero-dep core philosophy:

| Feature | Core (zero deps) | Optional Extra |
|---------|:-:|:-:|
| CSV source | yes | — |
| DataFrame source | — | `[pandas]` |
| SQLite source | yes (stdlib) | — |
| PostgreSQL/MySQL | — | `[sql]` → `sqlalchemy` |
| Parquet files | — | `[pandas]` or `[arrow]` |
| REST API source | yes (urllib) | — |
| Cloud storage | — | `[cloud]` → `boto3`/`gcsfs` |
| DuckDB | — | `[duckdb]` |
| Data profiling | yes (basic) | `[pandas]` for full stats |

---

## Lightweight Semantic Layer

Research shows that **every successful BI tool has a semantic layer** — PowerBI's semantic
models, dbt's metrics layer, Metabase's metadata sync. It's what prevents LLMs from
hallucinating when they query data. notebookmd doesn't need a full-blown semantic layer,
but a lightweight version would be the differentiator.

### Report Metadata Header

Every generated report embeds machine-readable context:

```markdown
<!--
notebookmd:dashboard
sources:
  - name: sales_db
    type: postgresql
    tables: [orders, customers, products]
    freshness: 2026-03-12T09:00:00Z
metrics:
  - name: total_revenue
    expr: "SUM(orders.total)"
    format: "$,.0f"
  - name: avg_order_value
    expr: "AVG(orders.total)"
    format: "$,.2f"
parameters:
  date_range: "2026-03-01..2026-03-12"
  region: "all"
-->
```

This means:
- **Other agents** can parse the report and understand what data backs it
- **Refresh scripts** know what to re-query and can diff metrics
- **Report indexes** can auto-catalog dashboards by source, metrics, and freshness
- **Downstream agents** can chain analyses without re-discovering the schema

### Metric Definitions (Reusable)

```python
from notebookmd.sources import MetricDef

revenue = MetricDef("Total Revenue", expr="SUM(total)", format="$,.0f")
aov = MetricDef("Avg Order Value", expr="AVG(total)", format="$,.2f")

# Use in any dashboard
n.metric_from(revenue, src, filter="date >= '2026-03-01'")
```

This is intentionally simpler than dbt's MetricFlow or Cube — just enough structure for
agents to work with, without requiring a build step or config server.

---

## Cross-Report Linking & Indexing

When agents generate 50+ reports, navigation becomes critical:

```python
from notebookmd.dashboard import ReportIndex

idx = ReportIndex("output/")
idx.scan()  # Discovers all .md files with notebookmd metadata

# Generate an index page
n = nb("output/index.md", title="Dashboard Index")
n.table(idx.to_dataframe(), name="All Reports")
# Columns: title, sources, last_refreshed, metrics_count, status
n.save()
```

---

## Competitive Positioning

> **Evidence.dev is BI-as-code for humans writing SQL.**
> **notebookmd is BI-as-code for AI agents writing Python.**

| Dimension | Evidence.dev | Streamlit | Metabase | notebookmd (proposed) |
|-----------|:-:|:-:|:-:|:-:|
| Language | SQL + Markdown | Python | SQL + UI | Python |
| Output | Static website | Live server | Live server | Static Markdown |
| Dependencies | Node.js, DuckDB | Python, server | JVM, database | Zero (core) |
| AI-native | Evidence Agent | Community | Metabot | Built for agents |
| Git-friendly | yes | no | no | yes |
| Token efficiency | N/A | N/A | N/A | 4-5x vs HTML |
| Artifact persistence | Built site | Ephemeral | Ephemeral | `.md` + `assets/` |

Key insight from research: Markdown is **4-5x more token-efficient than HTML** for LLM
consumption (2 tokens for `## Heading` vs 9 for `<h2>Heading</h2>`). This makes notebookmd
reports inherently cheaper and faster for downstream agent processing.

---

## What Makes This Unique

1. **Agent-first** — Every feature is designed for programmatic use, not clicking a UI
2. **Markdown-native** — Output is plain Markdown, not a proprietary dashboard format
3. **Zero-server** — No running process needed; generate once, read anywhere
4. **Git-friendly** — Dashboards are diffable, reviewable, and versionable
5. **Composable** — Mix data sources, templates, and custom widgets freely
6. **Progressive complexity** — From `connect("file.csv")` to full SQL warehouse dashboards
7. **LLM-readable** — Both input (API) and output (Markdown) are native to language models

---

## Tagline Options

- **"The Markdown BI layer for AI agents"**
- **"Metabase, but Markdown. Built for agents."**
- **"From database to dashboard in one Python script"**
- **"BI without the browser"**

---

*This proposal extends notebookmd from a report generation library into a lightweight,
agent-native analytics platform — filling the gap between heavyweight BI tools and raw
`print()` statements.*
