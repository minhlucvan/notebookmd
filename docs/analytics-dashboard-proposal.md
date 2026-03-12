# Analytics Dashboard for AI Agents — Design Proposal

**Code-first analytics platform. Powered by Markdown.**

> Connect data sources → Define metrics → Join & transform → Visualize as Markdown.
> Like Metabase or PowerBI, but code-first, agent-native, and Markdown-output.

---

## The Vision

A **full analytics platform** where AI agents (or humans) define data sources, metrics,
relationships, and transformations in Python — and the output is clean, portable Markdown.

notebookmd (the rendering library) is just one piece underneath. The dashboard layer sits
**above** it and thinks about the real analytics problems:

- Where does the data live?
- What are the key metrics and how are they calculated?
- How do tables relate to each other?
- What dimensions can you slice by?
- How has a metric changed over time?

Visualization is the **last step**, not the first.

```
┌─────────────────────────────────────────────────────┐
│            Analytics Dashboard (NEW)                 │
│                                                     │
│  Sources → Metrics → Joins → Transforms → Insights  │
│                                                     │
│         ┌───────────────────────────┐               │
│         │  notebookmd (rendering)   │  ◄── existing │
│         │  n.metric, n.table, etc.  │               │
│         └───────────────────────────┘               │
│                      │                              │
│                      ▼                              │
│               report.md + assets/                   │
└─────────────────────────────────────────────────────┘
```

---

## What the Platform Does

### 1. Data Sources — "Where does the data live?"

Connect to anything. The platform knows about your data, not just individual DataFrames.

```python
from notebookmd.analytics import Dashboard

dash = Dashboard("output/weekly.md", title="Weekly Business Review")

# Register data sources — the dashboard knows about all of them
dash.source("orders", "data/orders.csv")
dash.source("customers", "postgresql://host/db", table="customers")
dash.source("products", "data/products.parquet")
dash.source("web", "https://api.analytics.com/v1/events", format="json")
```

Sources are **first-class objects**. The dashboard tracks them, profiles them, and
understands their schemas. An agent can ask: "what sources do I have? what columns?
what types? how fresh is the data?"

```python
# Agent discovers what's available
for src in dash.sources:
    print(src.name, src.columns, src.row_count, src.freshness)

# Output:
# orders    [date, customer_id, product_id, quantity, revenue]  145,230  2026-03-12
# customers [id, name, segment, region, signup_date]             12,891  2026-03-12
# products  [id, name, category, price, cost]                      487  2026-03-01
# web       [timestamp, event, user_id, page, duration]       1.2M     2026-03-12
```

### 2. Metrics — "What are we measuring?"

Metrics are defined once, reused everywhere. Not just formatted values — actual
calculations with formulas, formats, and business context.

```python
# Define metrics as first-class objects
dash.metric("revenue",
    expr="SUM(orders.revenue)",
    format="$,.0f",
    description="Total gross revenue from all orders")

dash.metric("aov",
    expr="SUM(orders.revenue) / COUNT(orders.*)",
    format="$,.2f",
    description="Average order value")

dash.metric("customers",
    expr="COUNT(DISTINCT orders.customer_id)",
    format=",d",
    description="Unique paying customers")

dash.metric("conversion_rate",
    expr="COUNT(DISTINCT orders.customer_id) / COUNT(DISTINCT web.user_id)",
    format=".1%",
    description="Visitor to customer conversion rate",
    sources=["orders", "web"])  # cross-source metric
```

Metrics know:
- **How to compute themselves** (expression tied to source columns)
- **How to format** (currency, percentage, integer, etc.)
- **What they mean** (description for agents and humans)
- **Which sources they need** (dependency tracking)
- **How to compare** (period-over-period, vs target, vs benchmark)

### 3. Relationships & Joins — "How does the data connect?"

The dashboard understands how tables relate. Agents don't manually write JOIN clauses.

```python
# Define relationships between sources
dash.join("orders", "customers", on="customer_id")
dash.join("orders", "products", on="product_id")
```

Now the platform can automatically:
- Slice revenue by customer segment (orders → customers)
- Slice revenue by product category (orders → products)
- Compute cross-source metrics without manual SQL

```python
# Agent asks for revenue by segment — the platform handles the join
by_segment = dash.slice("revenue", by="customers.segment")
# Returns DataFrame with segment, revenue — join handled automatically

# Multi-dimensional slice
by_segment_category = dash.slice("revenue", by=["customers.segment", "products.category"])
```

### 4. Dimensions & Slicing — "How do we break it down?"

Dimensions are the axes you slice metrics along. The platform auto-discovers them
and lets agents explore freely.

```python
# Auto-discovered dimensions
dash.dimensions()
# → ["orders.date", "customers.segment", "customers.region",
#    "products.category", "products.name"]

# Slice any metric by any dimension
revenue_by_date = dash.slice("revenue", by="orders.date", period="weekly")
revenue_by_region = dash.slice("revenue", by="customers.region")
revenue_trend = dash.trend("revenue", over="orders.date", period="daily", last=30)

# Compare periods
dash.compare("revenue", current="2026-03", previous="2026-02")
# → {current: $1.2M, previous: $1.05M, change: +$150K, pct: +14.3%}
```

### 5. Transforms & Computed Fields — "Derive new data"

Add computed columns, filters, and aggregations without touching the raw data.

```python
# Computed fields
dash.compute("orders", "profit", expr="revenue - (products.cost * quantity)")
dash.compute("orders", "margin", expr="profit / revenue", format=".1%")

# Filters
enterprise = dash.filter("customers.segment == 'Enterprise'")
recent = dash.filter("orders.date >= '2026-03-01'")

# Filtered metrics
enterprise_revenue = dash.slice("revenue", by="orders.date", where=enterprise)
```

### 6. Render — "Show me the dashboard"

After all the analytical thinking, visualization is the final step.
The platform uses notebookmd underneath but the agent thinks in metrics and dimensions,
not in widget calls.

```python
# High-level rendering — the platform decides the best visualization
dash.show("revenue")                          # → metric card with delta
dash.show("revenue", by="orders.date")        # → line chart (time series)
dash.show("revenue", by="customers.region")   # → bar chart (categorical)
dash.show("revenue", by=["region", "date"])   # → multi-line chart

# Or explicit control
dash.card("revenue", "aov", "customers")      # → metric row
dash.timeseries("revenue", period="daily")    # → trend chart + table
dash.breakdown("revenue", by="segment")       # → bar chart + table
dash.comparison("revenue", "2026-03", "2026-02")  # → delta table

# Save the full dashboard
dash.save()
```

The `.show()` method is smart — it picks the right visualization based on the metric
type and dimension. Time dimension → line chart. Categorical → bar chart. Single value → metric card.

---

## End-to-End Example

```python
from notebookmd.analytics import Dashboard

# === SETUP: Define the analytical model ===

dash = Dashboard("output/weekly.md", title="Weekly Business Review")

# Sources
dash.source("orders", "data/orders.csv")
dash.source("customers", "data/customers.csv")
dash.source("products", "data/products.csv")

# Relationships
dash.join("orders", "customers", on="customer_id")
dash.join("orders", "products", on="product_id")

# Metrics
dash.metric("revenue", expr="SUM(orders.revenue)", format="$,.0f")
dash.metric("orders", expr="COUNT(orders.*)", format=",d")
dash.metric("aov", expr="revenue / orders", format="$,.2f")
dash.metric("margin", expr="SUM(orders.revenue - products.cost * orders.quantity) / SUM(orders.revenue)", format=".1%")

# === RENDER: Build the dashboard ===

dash.section("Key Metrics")
dash.card("revenue", "orders", "aov", "margin", compare="previous_week")

dash.section("Revenue Trend")
dash.timeseries("revenue", period="daily", last=30)

dash.section("Segment Analysis")
dash.breakdown("revenue", by="customers.segment")
dash.breakdown("revenue", by="products.category", top=10)

dash.section("Regional Performance")
dash.breakdown("revenue", by="customers.region", compare="previous_week")

dash.section("Data Health")
dash.freshness()   # Shows last-updated for each source
dash.coverage()    # Shows null rates, data completeness

dash.save()
```

**Output**: A complete `weekly.md` with KPI cards, trend charts, breakdowns, comparisons —
all from a single analytical model definition. No manual pandas. No manual SQL. No manual
chart configuration.

---

## How This Differs from "Just Using notebookmd"

| Concern | Raw notebookmd | Analytics Dashboard |
|---------|:---:|:---:|
| Data sources | Agent does `pd.read_csv()` manually | `dash.source()` — registered, tracked, profiled |
| Metrics | Agent computes `df['revenue'].sum()` and formats manually | `dash.metric("revenue", expr=...)` — defined once, computed automatically |
| Joins | Agent writes `pd.merge()` or SQL joins manually | `dash.join()` — relationships declared, joins automatic |
| Slicing | Agent does `df.groupby()` manually | `dash.slice("revenue", by="segment")` — one call |
| Period comparison | Agent computes current vs previous manually | `dash.compare("revenue", current, previous)` — built in |
| Visualization | Agent calls `n.metric()`, `n.table()`, `n.chart()` directly | `dash.show("revenue", by="date")` — auto-picks the right chart |
| Freshness | Not tracked | `dash.freshness()` — automatic |
| Reusability | Copy-paste between reports | Metrics and sources defined once, reused across dashboards |

The key difference: **raw notebookmd is a rendering library. The Analytics Dashboard is an
analytical thinking framework** that happens to render to Markdown.

---

## The Analytical Model

At the core is a declarative analytical model:

```python
# The model — WHAT we're analyzing
Sources:     orders, customers, products, web_events
Joins:       orders ↔ customers (customer_id), orders ↔ products (product_id)
Metrics:     revenue, aov, margin, customers, conversion_rate
Dimensions:  date, segment, region, category
Filters:     enterprise_only, recent_30d, high_value

# The dashboard — HOW we're presenting it
Sections:    Key Metrics, Trends, Breakdowns, Comparisons, Data Health
```

This model is:
- **Reusable** — same model, different dashboards (weekly summary vs deep dive)
- **Composable** — mix sources and metrics freely
- **Discoverable** — agents can introspect the model to decide what to analyze
- **Portable** — the model definition is Python code, versionable in git

### Agent Workflow

An agent working with the Analytics Dashboard thinks at a higher level:

```
1. "What data sources are available?"     → dash.sources
2. "What can I measure?"                  → dash.metrics
3. "What dimensions can I slice by?"      → dash.dimensions()
4. "How has revenue changed?"             → dash.trend("revenue")
5. "What's driving the change?"           → dash.breakdown("revenue", by="segment")
6. "Show me the dashboard."               → dash.save()
```

Compare this to raw notebookmd where the agent must manually:
1. Load each CSV/database
2. Write pandas code for every aggregation
3. Format every number
4. Choose every chart type
5. Handle every join

---

## Architecture

```
notebookmd/
├── analytics/                    # NEW: The analytics platform
│   ├── __init__.py               # Dashboard class, public API
│   ├── dashboard.py              # Dashboard: sources, metrics, joins, rendering
│   ├── source.py                 # DataSource: connect, schema, query, profile
│   ├── metric.py                 # MetricDef: expression, format, dependencies
│   ├── join.py                   # JoinSpec: relationships between sources
│   ├── slice.py                  # Slicer: groupby, filter, period comparison
│   ├── suggest.py                # Auto-discovery: suggest metrics, charts, dimensions
│   └── refresh.py                # Re-run + diff tracking
├── core.py                       # Notebook class (existing — used by Dashboard internally)
├── plugins/                      # Widget plugins (existing — used by Dashboard internally)
│   ├── text.py, data.py, charts.py, analytics.py, ...
└── ...
```

The `Dashboard` class owns a `Notebook` internally. It translates analytical operations
(slice, trend, breakdown, compare) into notebookmd widget calls (metric, table, chart).
The agent never touches `n.metric()` directly — it works at the analytics level.

---

## Implementation Plan

### Phase 1: Core Model
- `Dashboard` class with `source()`, `metric()`, `join()`
- `DataSource` with schema discovery, profiling, query
- `MetricDef` with expression parsing and formatting
- `JoinSpec` with automatic join resolution
- Basic `show()` → delegates to notebookmd rendering

### Phase 2: Slicing & Comparison
- `slice()` — groupby any dimension with automatic joins
- `trend()` — time series with configurable period
- `compare()` — period-over-period, segment-vs-segment
- `breakdown()` — top-N categorical analysis
- Smart chart selection based on metric + dimension type

### Phase 3: Auto-Discovery
- `suggest()` — auto-detect metrics, time columns, categories
- `dash.auto()` — generate a complete dashboard from sources alone
- `dimensions()` — enumerate all available slicing axes
- `anomalies()` — flag statistical outliers

### Phase 4: Templates & Operations
- Pre-built dashboard templates (KPI, TimeSeries, Comparison, Funnel)
- `refresh()` — re-run with metric diff tracking
- `freshness()` / `coverage()` — data health widgets
- CLI: `notebookmd run --refresh --alert-webhook`

### Phase 5: Advanced
- Computed fields and derived metrics
- Cross-source metrics (metrics spanning multiple sources)
- Parameterized dashboards (date range, region, segment as parameters)
- Report index and cross-dashboard navigation

---

## Dependency Strategy

| Feature | Zero deps | Optional |
|---------|:-:|:-:|
| Dashboard API, metric definitions, join specs | yes | — |
| CSV source | yes (stdlib) | — |
| SQLite source | yes (stdlib) | — |
| Pandas source + transforms | — | `[pandas]` |
| SQL databases | — | `[sql]` → `sqlalchemy` |
| DuckDB (universal query) | — | `[duckdb]` |
| Chart rendering | — | `[plotting]` |
| Everything | — | `[all]` |

---

## The Positioning

This is not a rendering library. This is an **analytics platform**.

```
Metabase:    GUI → click to explore → dashboard (browser-only)
PowerBI:     GUI → drag and drop → dashboard (proprietary)
Evidence:    SQL + Markdown → build step → static website
Streamlit:   Python → live server → interactive app

notebookmd:  Python → analytical model → Markdown report (portable, everywhere)
```

What they all have in common: **data sources, metrics, joins, dimensions, slicing**.
That's what analytics IS. The visualization is just the delivery format.

notebookmd's analytics layer speaks the same language as Metabase and PowerBI —
sources, metrics, relationships, dimensions — but in Python code, for agents,
outputting Markdown.

**Code-first. Agent-native. Markdown-output. Full analytics.**
