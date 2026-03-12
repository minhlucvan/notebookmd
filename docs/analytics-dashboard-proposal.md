# notebookmd Analytics Dashboard — Design Proposal

**The last-mile rendering layer for AI agent analytics.**

> Where notebookmd fits: Data Warehouse → Semantic Layer → AI Agent → **notebookmd** → Stakeholder

---

## Where We Stand in the Analytics Value Chain

The modern analytics stack has clear layers. Every tool occupies a specific position.
notebookmd's opportunity is the **last-mile rendering gap** — the missing piece between
AI agent reasoning and stakeholder-readable output.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    THE ANALYTICS VALUE CHAIN                           │
│                                                                        │
│  Data Sources     Data Platform      AI / Query        Delivery        │
│  ───────────      ─────────────      ─────────         ────────        │
│                                                                        │
│  PostgreSQL ─┐                                                         │
│  MySQL      ─┤    Snowflake         Cortex Analyst                     │
│  CSV/Parquet ┤    Databricks        Genie Agent        Dashboards?     │
│  S3/GCS     ─┤    BigQuery          Looker + Gemini    PDF exports?    │
│  REST APIs  ─┤    DuckDB ◄──────    ThoughtSpot        Slack bots?     │
│  MongoDB    ─┘                      Hex Agent          Email?          │
│                        │            Cortex Agents                      │
│                        │                 │              ┌────────────┐  │
│                   Semantic Layer         │              │            │  │
│                   (Cube, dbt,           ▼              │ notebookmd │  │
│                    LookML,         AI Agent reasons     │ ◄── HERE  │  │
│                    Unity Catalog)  about data           │            │  │
│                                                        └────────────┘  │
│                                                              │         │
│                                                              ▼         │
│                                                     Markdown report    │
│                                                     (.md + assets/)    │
│                                                     git-committable    │
│                                                     LLM-readable       │
└─────────────────────────────────────────────────────────────────────────┘
```

### The Key Insight

Every major analytics platform is adding AI agents:
- **Databricks** has Genie (Research Agent, agentic dashboards)
- **Snowflake** has Cortex Analyst + Cortex Agents
- **Google** has Looker + Gemini Conversational Analytics
- **Microsoft** has Fabric Copilot + MCP Server Endpoints
- **ThoughtSpot** has Spotter (agentic semantic layer)
- **Hex** has Notebook Agent (Claude-powered)

These agents are great at **querying and reasoning**. But their output is trapped:
- Databricks → lives in Databricks UI
- Snowflake → lives in Streamlit apps or Snowsight
- Hex → lives in Hex notebooks
- ThoughtSpot → lives in Liveboards

**No tool produces portable, static, agent-readable Markdown reports.** That's notebookmd's position.

---

## The Last-Mile Problem

Research shows this is a real, named problem in the industry:

> "Organizations are insight-rich but action-poor." — Analytics industry consensus
>
> "95% of AI pilots fail in production — not because of model quality, but organizational
> integration." — HBR, March 2026

The frictions in the "last mile":

| Problem | Current State | notebookmd Solution |
|---------|--------------|-------------------|
| **Format lock-in** | Insights trapped in proprietary dashboards | Plain Markdown renders everywhere |
| **Agent output is ephemeral** | Julius AI, Code Interpreter results live in chat sessions | Persistent `.md` files, git-versioned |
| **No Markdown export** | Metabase: PDF only. PowerBI: proprietary. Looker: HTML. | Native Markdown output |
| **Token overhead** | HTML dashboards cost 4-5x more tokens for LLMs to parse | Markdown is LLM-native |
| **No diff tracking** | Can't `git diff` a Metabase dashboard | `git diff report.md` shows exactly what changed |
| **Narrative gap** | Dashboards show "what" but not "why" | Agent writes narrative + data together |

---

## Competitive Landscape (Deep Research)

### Tools That Touch Our Space

| Tool | Layer | What It Does | Markdown Export? | Agent API? |
|------|-------|-------------|:---:|:---:|
| **Metabase** | BI / Visualization | Self-serve dashboards, SQL + visual query builder | No (PDF/CSV/XLSX only) | Limited REST API |
| **PowerBI** | BI / Visualization | Enterprise dashboards, DAX, semantic models | No (proprietary) | Power Automate |
| **Evidence.dev** | BI-as-Code | SQL + Markdown → static website | Markdown input, HTML output | No |
| **Streamlit** | App Framework | Python → live web app | No (requires server) | No |
| **Dash (Plotly)** | App Framework | Python callbacks → live web app | No (requires server) | No |
| **DuckDB** | Query Engine | In-process OLAP, reads CSV/Parquet/S3/Postgres | N/A (engine only) | Python API |
| **MindsDB** | AI Data Hub | SQL interface to 200+ sources + AI models | No | MCP server |
| **Hex** | Notebook + BI | Notebooks + AI agent + published apps | No (requires Hex) | Internal agent |
| **Cube** | Semantic Layer | Headless BI, metric definitions, REST/GraphQL APIs | No | MCP server |
| **notebookmd** | **Report Renderer** | Python API → static Markdown + assets | **Yes (native)** | **Yes (native)** |

### Key Findings

**Metabase has zero Markdown export.** Exports: PDF (UI-only screenshots), CSV/XLSX/JSON (raw data via API), PNG (UI-only, API endpoint broken per GitHub #41879). Dashboard subscriptions deliver via email/Slack only. 134-upvote issue for Markdown in table cells (#7188) still open.

**DuckDB is the ideal embedded query engine.** Zero-config, reads everything (CSV, Parquet, JSON, S3, Postgres, MySQL), 40x faster than pandas on large datasets, zero-copy DataFrame integration. MotherDuck has an MCP server. Evidence.dev uses DuckDB as both build-time and browser-time engine.

**MindsDB is a universal data adapter.** 200+ source connectors, SQL interface to AI models ("AI Tables"), MCP server for agent integration. Positions as "AI's Query Engine" — middleware between data sources and AI agents.

**MCP is the emerging standard.** 340% adoption growth in 2025, 500+ servers in public registries. Database MCP servers from Google Cloud, Snowflake, Microsoft Fabric, MindsDB, MotherDuck. Donated to Linux Foundation's Agentic AI Foundation.

**The semantic layer is non-negotiable for AI.** Gartner: "60% of agentic analytics projects without a consistent semantic layer will fail by 2028." Google: semantic layer reduces NL query errors by 50-66%. Every major platform (Databricks Unity Catalog, Looker LookML, ThoughtSpot Spotter Semantics, Snowflake semantic models) treats this as critical infrastructure.

---

## Where notebookmd Sits: The Rendering Layer

notebookmd does NOT compete with Metabase, DuckDB, or MindsDB. It **complements** them.

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│   DATA ACCESS              INTELLIGENCE         RENDERING        │
│   (not our job)            (not our job)         (OUR JOB)       │
│                                                                  │
│   ┌──────────┐            ┌──────────┐         ┌──────────────┐  │
│   │ DuckDB   │            │ AI Agent │         │ notebookmd   │  │
│   │ MindsDB  │──query──►  │ (Claude, │──render─►│              │  │
│   │ MCP      │            │  GPT,    │         │ .md + assets/ │  │
│   │ Postgres │◄─schema──  │  local)  │         │ git-friendly  │  │
│   │ CSV/S3   │            │          │         │ LLM-readable  │  │
│   └──────────┘            └──────────┘         └──────────────┘  │
│                                                       │          │
│   Also:                   Also:                       ▼          │
│   Cube, dbt (semantic)    Hex, Spotter,        GitHub, Slack,    │
│   Snowflake, BigQuery     Genie, Cortex        email, CI/CD,    │
│                                                PDF, web          │
└──────────────────────────────────────────────────────────────────┘
```

### The Integration Story

notebookmd doesn't need to build a query engine or 200 connectors. Instead:

1. **DuckDB as the query engine** — optional `[duckdb]` extra, gives universal data access
2. **MCP as the protocol** — agents already have MCP access to databases; notebookmd is where they write results
3. **Semantic layers are upstream** — Cube/dbt/LookML define metrics; agents consume them; notebookmd renders them

### What notebookmd SHOULD Build

| Build | Don't Build | Why |
|-------|-------------|-----|
| DuckDB integration plugin | Full SQL engine | DuckDB already does this perfectly |
| `connect()` convenience wrapper | 200 database connectors | Use DuckDB/MCP for access |
| Lightweight metric definitions | Full semantic layer | Cube/dbt own this; we need just enough for report metadata |
| Schema-aware report templates | Query optimization | Agents handle query logic |
| MCP-compatible output format | MCP server | Agents write to notebookmd, not the reverse |
| Refresh + diff tracking | Real-time streaming | We're batch/static by design |

---

## Proposed Architecture (Revised)

```
notebookmd/
├── sources/                  # Thin data source wrappers
│   ├── __init__.py           # connect() factory, DataSource protocol
│   ├── _base.py              # DataSource protocol + schema types
│   ├── csv_source.py         # CSV files (zero-dep, stdlib csv module)
│   ├── dataframe_source.py   # pandas DataFrame wrapper
│   ├── duckdb_source.py      # DuckDB: the universal connector [duckdb]
│   └── sql_source.py         # SQLite (stdlib) + SQLAlchemy [sql]
├── discovery/                # Data profiling for agents
│   ├── __init__.py
│   ├── profiler.py           # Column stats, distributions, anomalies
│   └── suggest.py            # AI-friendly hints (KPI candidates, chart suggestions)
├── dashboard/                # Dashboard templates + operations
│   ├── __init__.py           # dashboard() factory
│   ├── templates.py          # Built-in templates (KPI, timeseries, comparison)
│   ├── refresh.py            # Re-run + metric diff tracking
│   └── index.py              # ReportIndex: cross-report catalog
├── plugins/
│   ├── dashboard.py          # DashboardPlugin: n.connect(), n.source_status(), etc.
│   └── ...existing plugins
└── ...existing files
```

### The DuckDB-First Strategy

Instead of building connectors for every database, make DuckDB the universal adapter:

```python
from notebookmd import nb
from notebookmd.sources import connect

# DuckDB reads EVERYTHING — CSV, Parquet, JSON, S3, Postgres, MySQL
src = connect("duckdb://")  # in-memory DuckDB

# Query local files directly
df = src.query("SELECT * FROM 'data/sales.csv' WHERE revenue > 1000")

# Query remote files
df = src.query("SELECT * FROM 's3://bucket/data.parquet'")

# Attach a Postgres database and query it
src.execute("ATTACH 'postgresql://user:pass@host/db' AS warehouse")
df = src.query("SELECT * FROM warehouse.orders LIMIT 100")

# Cross-source join (the DuckDB superpower)
df = src.query("""
    SELECT o.*, c.segment
    FROM 'data/orders.csv' o
    JOIN warehouse.customers c ON o.customer_id = c.id
""")

# Render with notebookmd
n = nb("output/report.md", title="Cross-Source Analysis")
n.table(df, name="Orders with Customer Segments")
n.save()
```

This gives notebookmd access to **every data source DuckDB supports** (CSV, Parquet, JSON,
S3, GCS, Azure, PostgreSQL, MySQL, SQLite, HTTP endpoints) with a single optional dependency.

### Zero-Dep Fallback

For environments where DuckDB isn't available:

```python
# CSV source works with zero dependencies (stdlib csv module)
src = connect("data/sales.csv")  # Uses CSVSource

# SQLite works with zero dependencies (stdlib sqlite3)
src = connect("sqlite:///app.db")  # Uses SQLSource

# pandas DataFrame if pandas is available
src = connect(df)  # Uses DataFrameSource
```

---

## Data Profiling & Discovery

Auto-generate data profiles that agents can reason about:

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

This is the **Metabase auto-discovery experience** as a Python API. An agent goes from
"here's a CSV" to "here's a full dashboard" with zero human input.

---

## Lightweight Semantic Layer

Every successful BI tool has a semantic layer — PowerBI's semantic models, dbt's metrics
layer, Looker's LookML, ThoughtSpot's Spotter Semantics. Gartner says 60% of agentic
analytics projects without one will fail.

notebookmd doesn't need a full semantic layer. But it needs **just enough** for:
- Report metadata (what data backs this report?)
- Reusable metric definitions (consistent calculations across reports)
- Agent-to-agent communication (downstream agents can parse report context)

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

### Reusable Metric Definitions

```python
from notebookmd.sources import MetricDef

revenue = MetricDef("Total Revenue", expr="SUM(total)", format="$,.0f")
aov = MetricDef("Avg Order Value", expr="AVG(total)", format="$,.2f")

# Use in any dashboard — consistent calculation & formatting
n.metric_from(revenue, src, filter="date >= '2026-03-01'")
```

Intentionally simpler than dbt's MetricFlow or Cube. No build step, no config server.
Just Python dataclasses that agents can define and reuse.

---

## Dashboard Templates

Pre-built, composable dashboard blueprints:

```python
from notebookmd import nb
from notebookmd.sources import connect
from notebookmd.dashboard import KPIDashboard

src = connect("data/sales.csv")

n = nb("output/sales_dashboard.md", title="Sales Dashboard")
KPIDashboard(
    source=src,
    metrics=["revenue", "orders", "avg_order_value"],
    time_column="order_date",
    group_by="region",
).render(n)
n.save()
```

### Built-in Templates

| Template | Use Case | What It Generates |
|----------|----------|-------------------|
| `KPIDashboard` | Executive summary | Metric cards, sparklines, period-over-period change |
| `TimeSeriesDashboard` | Trend analysis | Line charts, moving averages, seasonality detection |
| `ComparisonDashboard` | A/B or segment comparison | Side-by-side metrics, statistical significance |
| `DataQualityDashboard` | Data health monitoring | Null rates, type mismatches, freshness, anomalies |
| `FunnelDashboard` | Conversion/pipeline analysis | Stage metrics, drop-off rates, conversion charts |

---

## Refresh & Diff Tracking

The operational dashboard feature: re-run and track changes over time.

```python
from notebookmd.dashboard import refresh

result = refresh("scripts/daily_kpis.py", output="output/daily_kpis.md")
# result.changed == True if metrics shifted
# result.diff == markdown-formatted diff of key metrics
# result.alerts == ["Revenue dropped 15% vs yesterday"]
```

**Git-native diffs** — since output is Markdown, `git diff` shows exactly what changed:

```diff
- | **Revenue** | **$1.2M** | ▲ +12% |
+ | **Revenue** | **$1.05M** | ▼ -5% |
```

**CLI integration:**

```bash
notebookmd run scripts/daily_kpis.py --refresh
0 9 * * * notebookmd run scripts/daily_kpis.py --refresh --alert-webhook $SLACK_URL
```

---

## Cross-Report Indexing

When agents generate many reports, navigation becomes critical:

```python
from notebookmd.dashboard import ReportIndex

idx = ReportIndex("output/")
idx.scan()  # Discovers all .md files with notebookmd metadata

n = nb("output/index.md", title="Dashboard Index")
n.table(idx.to_dataframe(), name="All Reports")
# Columns: title, sources, last_refreshed, metrics_count, status
n.save()
```

---

## Competitive Positioning (Corrected)

### notebookmd is NOT a BI tool. It's the rendering layer that BI tools are missing.

```
┌────────────────────────────────────────────────────────────────┐
│  TRADITIONAL BI                    AGENT-NATIVE ANALYTICS      │
│                                                                │
│  Human clicks UI ──► Dashboard     Agent writes code ──► ???   │
│                                                                │
│  Metabase, PowerBI,                notebookmd fills             │
│  Looker, Tableau                   this gap ──► .md report     │
└────────────────────────────────────────────────────────────────┘
```

### Detailed Comparison

| Dimension | Evidence.dev | Metabase | DuckDB | MindsDB | notebookmd |
|-----------|:-:|:-:|:-:|:-:|:-:|
| **Layer** | BI-as-Code | BI Tool | Query Engine | Data Hub | Report Renderer |
| **Language** | SQL + MD | SQL + UI | SQL | SQL | Python |
| **Output** | Static website | Live server | DataFrames | Query results | Static Markdown |
| **Dependencies** | Node.js, DuckDB | JVM, database | C++ lib | Python, server | Zero (core) |
| **Markdown export** | No (HTML) | No (PDF only) | N/A | No | **Yes (native)** |
| **Agent-native** | Evidence Agent | Metabot (basic) | MCP server | MCP server | **Built for agents** |
| **Git-friendly** | Yes (source) | No | N/A | No | **Yes (output)** |
| **Self-contained** | Needs build | Needs server | Needs app | Needs server | **Yes** |

### The Positioning Statement

> **Evidence.dev** is BI-as-code for analysts writing SQL.
> **Metabase** is self-serve BI for business users clicking a UI.
> **DuckDB** is the universal query engine that reads any data source.
> **MindsDB** is the universal adapter that connects AI to databases.
> **notebookmd** is the **rendering layer** where AI agents write their findings as
> structured, portable, version-controlled Markdown reports.

### Complementary, Not Competitive

The dream stack for AI agent analytics:

```python
# DuckDB provides universal data access
# MindsDB/MCP provides the agent-to-database bridge
# Cube/dbt provides semantic metric definitions
# The AI agent provides reasoning and analysis
# notebookmd provides the last-mile rendering

from notebookmd import nb
from notebookmd.sources import connect

src = connect("duckdb://")
src.execute("ATTACH 'postgresql://host/warehouse' AS wh")

n = nb("output/weekly.md", title="Weekly Analytics")
df = src.query("SELECT ... FROM wh.orders")
n.metric("Revenue", f"${df['revenue'].sum():,.0f}")
n.line_chart(df, x="date", y="revenue")
n.save()  # → portable .md + assets/, readable by humans AND agents
```

---

## MCP Integration Strategy

MCP (Model Context Protocol) is the standard for agent-to-tool communication. 340% adoption
growth in 2025, 500+ servers, adopted by OpenAI and donated to Linux Foundation.

notebookmd doesn't need an MCP **server** (it's a rendering library, not a data source).
But it benefits from the MCP ecosystem:

1. **Agents use MCP to access data** (MotherDuck MCP, BigQuery MCP, Snowflake MCP, MindsDB MCP)
2. **Agents use notebookmd to render results** (Python API)
3. **notebookmd output is MCP-friendly** (Markdown is the lingua franca of agent communication)

Future opportunity: a notebookmd MCP **tool** that lets agents say "render this data as a
dashboard" through MCP, producing `.md` output.

---

## Dependency Strategy

Stays true to the zero-dep core philosophy:

| Feature | Core (zero deps) | Optional Extra |
|---------|:-:|:-:|
| CSV source | yes (stdlib `csv`) | — |
| SQLite source | yes (stdlib `sqlite3`) | — |
| REST API source | yes (stdlib `urllib`) | — |
| DataFrame source | — | `[pandas]` |
| Parquet files | — | `[pandas]` or `[arrow]` |
| PostgreSQL/MySQL | — | `[sql]` → `sqlalchemy` |
| **DuckDB (universal)** | — | **`[duckdb]`** |
| Cloud storage | — | `[cloud]` → `boto3`/`gcsfs` |
| Data profiling | yes (basic) | `[pandas]` for full stats |

**Recommended install for full analytics:**

```bash
pip install "notebookmd[duckdb,plotting]"
```

This gives: universal data access (DuckDB), chart generation (matplotlib), and the full
notebookmd rendering API.

---

## Implementation Plan

### Phase 1: Data Sources + DuckDB (Core)
- `DataSource` protocol and base class
- `CSVSource` (zero-dep), `SQLSource` (sqlite3 stdlib), `DataFrameSource`
- `DuckDBSource` — the universal connector via optional `[duckdb]`
- `connect()` factory with URL-scheme detection
- `DashboardPlugin` with `n.connect()`, `n.source()`, `n.source_status()`

### Phase 2: Discovery + Profiling
- `profiler.py` — column statistics, type inference, distribution summaries
- `suggest.py` — AI-friendly hints (KPI candidates, chart suggestions)
- `n.source_profile()` integration
- Report metadata header generation

### Phase 3: Dashboard Templates
- `DashboardTemplate` base class
- `KPIDashboard`, `TimeSeriesDashboard`, `ComparisonDashboard`
- `n.auto_dashboard()` one-liner
- Metric definitions (`MetricDef`) and `n.metric_from()`

### Phase 4: Refresh & Operations
- `refresh()` function with metric diff tracking
- `--refresh` CLI flag
- `ReportIndex` for cross-report catalog
- Alert webhooks (Slack, email, generic HTTP)

### Phase 5: Ecosystem Integration
- MCP tool wrapper (optional)
- DuckDB extension ecosystem integration
- Community dashboard templates via entry points
- Evidence.dev-style parameterized reports

---

## What Makes This Unique

1. **Right layer** — Rendering, not querying. Complements DuckDB/MindsDB/MCP instead of competing
2. **Agent-first** — Every feature is a Python function call, not a UI click
3. **Markdown-native** — The only analytics tool with native Markdown output
4. **Zero-server** — No running process; generate once, read anywhere
5. **Git-friendly** — Dashboards are diffable, reviewable, versionable
6. **LLM-readable** — 4-5x more token-efficient than HTML; both input and output are LLM-native
7. **Progressive complexity** — From `connect("file.csv")` to cross-source DuckDB analytics
8. **Composable** — Works with any data access layer (DuckDB, MCP, pandas, raw SQL)

---

## Tagline

**"The last-mile rendering layer for AI agent analytics."**

Or more concretely:

**"AI agents query data. notebookmd turns it into reports."**

---

*notebookmd doesn't try to be Metabase, DuckDB, or MindsDB. It's the missing piece that
connects them all to the stakeholder — the rendering layer that turns agent analysis into
portable, versioned, readable Markdown reports.*
