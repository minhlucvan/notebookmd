# Analytics Dashboard for AI Agents — Design Proposal

**Code-first analytics platform. Markdown-output. Mirrors BI platform concepts.**

> Same data model as Metabase, Looker, PowerBI, Cube — but in Python, for agents,
> outputting Markdown. Import from them. Export to them. Or use standalone.

---

## The Core Idea

Every BI platform — Metabase, Looker, PowerBI, Cube — uses the same foundational concepts:

1. **Entities** (tables/views with semantic meaning)
2. **Dimensions** (attributes you group and filter by)
3. **Measures** (aggregations you compute)
4. **Relationships** (how entities join together)
5. **Queries** (select measures + dimensions → get results)
6. **Dashboards** (tiles bound to queries + global filters)

We mirror these concepts exactly in Python. The result is a data model that agents can
build programmatically, that maps 1:1 to existing BI platforms, and that renders to Markdown.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Metabase  ◄──────┐                                       │
│   Looker    ◄──────┤   notebookmd.analytics                │
│   PowerBI   ◄──────┤   (same concepts, Python API)         │
│   Cube      ◄──────┘                                       │
│                         │                                   │
│                         ▼                                   │
│                    Markdown report                          │
│                    (.md + assets/)                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## The Universal BI Data Model (in Python)

### Concept Mapping

| Concept | Looker | PowerBI | Cube | Metabase | **notebookmd** |
|---------|--------|---------|------|----------|:-:|
| Logical table | View | Table | Cube | Table | **Entity** |
| Attribute | dimension | Column | dimension | Column | **Dimension** |
| Aggregation | measure | DAX Measure | measure | Metric | **Measure** |
| Table link | explore + join | Relationship | joins | FK | **Relationship** |
| Query | Explore query | Visual query | /load API | Question | **Query** |
| Dashboard | Dashboard + tiles | Report + visuals | (frontend) | Dashboard + cards | **Dashboard + Tiles** |
| Filter | Dashboard filter | Slicer | filter member | Parameter | **Filter** |
| Time handling | dimension_group | Date table + DAX | time dimension | Temporal bins | **TimeDimension** |

### The Python API

```python
from notebookmd.analytics import Dashboard, Entity, Dimension, Measure

# === ENTITIES (like Looker views, PowerBI tables, Cube cubes) ===

orders = Entity(
    name="orders",
    source="data/orders.csv",                  # or "postgresql://...", table="orders"
    dimensions=[
        Dimension("order_id", type="number", primary_key=True),
        Dimension("status", type="string"),
        Dimension("order_date", type="time"),   # time dimension — auto-generates day/week/month/year
        Dimension("customer_id", type="number"),
        Dimension("product_id", type="number"),
    ],
    measures=[
        Measure("revenue", type="sum", sql="amount", format="$,.0f"),
        Measure("count", type="count"),
        Measure("aov", type="number", sql="revenue / count", format="$,.2f"),
        Measure("completed_count", type="count",
                filters=[("status", "equals", "completed")]),
    ],
)

customers = Entity(
    name="customers",
    source="data/customers.csv",
    dimensions=[
        Dimension("id", type="number", primary_key=True),
        Dimension("name", type="string"),
        Dimension("segment", type="string"),
        Dimension("region", type="string"),
        Dimension("signup_date", type="time"),
    ],
    measures=[
        Measure("count", type="count_distinct", sql="id"),
    ],
)

products = Entity(
    name="products",
    source="data/products.csv",
    dimensions=[
        Dimension("id", type="number", primary_key=True),
        Dimension("name", type="string"),
        Dimension("category", type="string"),
        Dimension("price", type="number"),
        Dimension("cost", type="number"),
    ],
)
```

This mirrors:
- **Looker**: `view: orders { dimension: status { type: string } measure: revenue { type: sum sql: ${amount} } }`
- **Cube**: `cube('Orders', { dimensions: { status: { type: 'string' } }, measures: { revenue: { type: 'sum', sql: 'amount' } } })`
- **PowerBI**: Table "Orders" with columns + DAX measure `Total Revenue = SUM(Orders[Amount])`

### Relationships (like Looker joins, PowerBI relationships, Cube joins)

```python
from notebookmd.analytics import Relationship

# Same concept as every BI platform: entity A links to entity B on a key
rels = [
    Relationship("orders", "customers",
                 on=("customer_id", "id"),
                 type="many_to_one"),

    Relationship("orders", "products",
                 on=("product_id", "id"),
                 type="many_to_one"),
]
```

Mirrors:
- **Looker**: `join: customers { relationship: many_to_one  sql_on: ${orders.customer_id} = ${customers.id} }`
- **Cube**: `joins: { Customers: { relationship: 'many_to_one', sql: '${CUBE}.customer_id = ${Customers}.id' } }`
- **PowerBI**: Relationship from Orders[CustomerID] to Customers[ID], many-to-one

### Queries (like Looker explore queries, Cube /load API, Metabase questions)

```python
from notebookmd.analytics import Query

# Composable query: select measures + dimensions → platform resolves joins + generates results
q = Query(
    measures=["orders.revenue", "orders.count"],
    dimensions=["customers.segment", "orders.order_date"],
    time_granularity="month",
    filters=[("orders.status", "equals", "completed")],
    sort=("orders.order_date", "asc"),
    limit=100,
)

# Execute against the model → returns DataFrame
result = dash.execute(q)
```

This is the same pattern as:
- **Cube REST API**: `{ "measures": ["Orders.revenue"], "dimensions": ["Orders.status"], "timeDimensions": [{"dimension": "Orders.created_at", "granularity": "month"}] }`
- **Looker**: User selects measures + dimensions in Explore → LookML generates SQL
- **Metabase**: "Question" with table, columns, aggregations, filters

The platform resolves joins automatically — if you ask for `orders.revenue` by
`customers.segment`, it knows to join orders → customers via customer_id.

### Dashboard (like Metabase dashboards, Looker dashboards, PowerBI reports)

```python
dash = Dashboard(
    title="Weekly Business Review",
    entities=[orders, customers, products],
    relationships=rels,
    output="output/weekly.md",
)

# Global filters (like Metabase parameters, Looker dashboard filters, PowerBI slicers)
dash.filter("date_range", dimension="orders.order_date", default="last_30_days")
dash.filter("region", dimension="customers.region")

# Tiles (like Metabase dashboard cards, Looker tiles, PowerBI visuals)
dash.section("Key Metrics")
dash.tile("orders.revenue", type="metric", compare="previous_period")
dash.tile("orders.count", type="metric", compare="previous_period")
dash.tile("orders.aov", type="metric", compare="previous_period")

dash.section("Revenue Trend")
dash.tile("orders.revenue", by="orders.order_date",
          type="line_chart", granularity="daily")

dash.section("Segment Analysis")
dash.tile("orders.revenue", by="customers.segment",
          type="bar_chart", sort="desc")

dash.section("Regional Breakdown")
dash.tile(["orders.revenue", "orders.count"],
          by="customers.region",
          type="table", sort="orders.revenue desc")

dash.section("Top Products")
dash.tile("orders.revenue", by="products.category",
          type="bar_chart", top=10)

# Render → resolves all queries, joins, and renders to Markdown
dash.save()
```

Each `tile()` is equivalent to:
- **Metabase**: A DashCard (card + position + parameter mappings)
- **Looker**: A dashboard element (explore + measures + dimensions + viz type)
- **PowerBI**: A visual on a report page (fields + chart type)

---

## Smart Defaults: Auto-Pick Visualization

Like Metabase's auto-chart selection, the platform picks the right visualization:

| Query Shape | Auto Visualization |
|-------------|-------------------|
| Single measure, no dimensions | Metric card |
| Measures + time dimension | Line chart |
| Measures + categorical dimension | Bar chart |
| Measures + categorical + time | Multi-line chart |
| Multiple measures + multiple dimensions | Table |
| Single measure + compare period | Metric card with delta |

```python
# The platform auto-selects:
dash.tile("orders.revenue")                              # → metric card
dash.tile("orders.revenue", by="orders.order_date")      # → line chart
dash.tile("orders.revenue", by="customers.region")       # → bar chart
dash.tile("orders.revenue", by="customers.region",
          compare="previous_period")                     # → bar chart with deltas

# Or override explicitly:
dash.tile("orders.revenue", by="customers.region", type="table")
```

---

## Time Intelligence (Built-In)

Like PowerBI's DAX time intelligence or Looker's dimension_group:

```python
# Period comparison — automatic when time dimension is involved
dash.tile("orders.revenue", compare="previous_period")    # vs last 30 days
dash.tile("orders.revenue", compare="previous_year")      # vs same period last year
dash.tile("orders.revenue", compare="target", target=1_500_000)  # vs target

# Time granularity
dash.tile("orders.revenue", by="orders.order_date", granularity="daily")
dash.tile("orders.revenue", by="orders.order_date", granularity="weekly")
dash.tile("orders.revenue", by="orders.order_date", granularity="monthly")

# Automatic time dimension detection from Dimension(type="time")
```

---

## Interop: Import From / Export To BI Platforms

Because the data model maps 1:1, we can convert between platforms:

### Import from Metabase

```python
from notebookmd.analytics.interop import from_metabase

# Connect to Metabase API, import dashboard definition
dash = from_metabase(
    url="https://metabase.company.com",
    api_key="mb_xxxx",
    dashboard_id=42,
    output="output/imported_dashboard.md",
)

# Now you have the same dashboard as Python objects
# Entities, dimensions, measures, relationships, tiles — all mapped
dash.save()  # → Markdown version of the Metabase dashboard
```

### Import from Looker (LookML)

```python
from notebookmd.analytics.interop import from_lookml

dash = from_lookml(
    project_dir="path/to/lookml/",
    explore="orders",
    output="output/looker_dashboard.md",
)
```

### Import from Cube

```python
from notebookmd.analytics.interop import from_cube

dash = from_cube(
    url="https://cube.company.com",
    api_token="xxx",
    cubes=["Orders", "Customers"],
    output="output/cube_dashboard.md",
)
```

### Export to Metabase

```python
from notebookmd.analytics.interop import to_metabase

# Push the dashboard definition back to Metabase
to_metabase(dash, url="https://metabase.company.com", api_key="mb_xxxx")
# Creates questions and a dashboard in Metabase matching the definition
```

### Export as Cube Schema

```python
from notebookmd.analytics.interop import to_cube_schema

# Generate Cube YAML from the dashboard model
to_cube_schema(dash, output_dir="cube/schema/")
# Writes Orders.yaml, Customers.yaml, Products.yaml with dimensions, measures, joins
```

This means notebookmd analytics can be:
- A **Markdown preview** of an existing Metabase/Looker dashboard
- A **migration tool** between BI platforms (Metabase → Looker → PowerBI)
- A **code-first definition** that syncs to any BI platform
- A **standalone analytics platform** for agent workflows

---

## Detailed Platform Mappings

### Metabase Mapping (exact API correspondence)

Every notebookmd concept maps directly to Metabase's API objects:

| notebookmd | Metabase API | JSON path |
|------------|-------------|-----------|
| `Entity` | Table | `GET /api/table/:id` |
| `Dimension` | Field | `GET /api/field/:id` — `base_type`, `semantic_type` |
| `Dimension(type="time")` | Field with `base_type: "type/DateTime"` | temporal bucketing via `{"temporal-unit": "month"}` |
| `Dimension(type="string")` | Field with `base_type: "type/Text"` | `semantic_type: "type/Category"` |
| `Measure(type="sum")` | MBQL aggregation | `["sum", ["field", <id>, null]]` |
| `Measure(type="count")` | MBQL aggregation | `["count"]` |
| `Measure(type="avg")` | MBQL aggregation | `["avg", ["field", <id>, null]]` |
| `Measure(filters=[...])` | MBQL `count-where` / `sum-where` | `["count-where", ["=", ["field", <id>], "value"]]` |
| `Relationship` | Foreign key | `fk_target_field_id` on Field, MBQL `joins` |
| `Dashboard` | Dashboard | `POST /api/dashboard` |
| `tile()` | DashCard + Card | Card = question, DashCard = placement + size |
| `filter()` | Dashboard parameter | `parameters[]` with type like `"date/all-options"` |
| `tile(type="metric")` | Card with `display: "scalar"` or `"smartscalar"` | `visualization_settings.scalar.*` |
| `tile(type="line_chart")` | Card with `display: "line"` | breakout with `temporal-unit` |
| `tile(type="bar_chart")` | Card with `display: "bar"` | breakout on categorical field |
| `tile(type="table")` | Card with `display: "table"` | `visualization_settings.table.*` |
| `section()` | Text DashCard | `card_id: null`, `visualization_settings.text: "## Title"` |

**Import example — what actually happens:**

```python
dash = from_metabase(url="https://mb.company.com", api_key="mb_xxx", dashboard_id=42)
```

Under the hood:
1. `GET /api/dashboard/42` → get dashboard with dashcards
2. For each dashcard, `GET /api/card/:card_id` → get the question definition
3. Parse `dataset_query.query` → extract `source-table`, `aggregation`, `breakout`, `filter`, `joins`
4. `GET /api/database/:id/metadata` → get all tables and fields
5. Map MBQL `["sum", ["field", 10, null]]` → `Measure("total", type="sum", sql="amount")`
6. Map `breakout: [["field", 7, {"temporal-unit": "month"}]]` → `by="orders.date", granularity="monthly"`
7. Map `display: "line"` → `type="line_chart"`
8. Map `parameters[]` → `dash.filter()`
9. Map dashcard `size_x/size_y/col/row` → tile ordering in sections

**Export example — what actually happens:**

```python
to_metabase(dash, url="https://mb.company.com", api_key="mb_xxx")
```

Under the hood:
1. Match entities to Metabase tables via `GET /api/database/:id/metadata`
2. For each tile, `POST /api/card` → create a question with MBQL query
3. `POST /api/dashboard` → create dashboard with parameters
4. `PUT /api/dashboard/:id/cards` → place dashcards with layout positions

### Looker / LookML Mapping

| notebookmd | LookML |
|------------|--------|
| `Entity("orders", source=...)` | `view: orders { sql_table_name: public.orders ;; }` |
| `Dimension("status", type="string")` | `dimension: status { type: string  sql: ${TABLE}.status ;; }` |
| `Dimension("date", type="time")` | `dimension_group: date { type: time  timeframes: [date, week, month, year] }` |
| `Measure("revenue", type="sum", sql="amount")` | `measure: revenue { type: sum  sql: ${amount} ;; }` |
| `Measure("count", type="count")` | `measure: count { type: count }` |
| `Measure(..., filters=[("status","=","completed")])` | `measure: x { type: count  filters: [status: "completed"] }` |
| `Relationship("orders","customers", on=(...), type="many_to_one")` | `join: customers { relationship: many_to_one  sql_on: ${orders.customer_id} = ${customers.id} ;; }` |
| `Dashboard` + tiles | `dashboard: x { elements: [ { explore: orders  measures: [orders.revenue]  dimensions: [...] } ] }` |
| `filter("date_range", ...)` | `filters: [ { name: date_range  type: date_filter  field: orders.date } ]` |

### Cube Mapping

| notebookmd | Cube schema |
|------------|-------------|
| `Entity("orders", source=...)` | `cube('Orders', { sql_table: 'public.orders' })` |
| `Dimension("status", type="string")` | `dimensions: { status: { sql: 'status', type: 'string' } }` |
| `Dimension("date", type="time")` | `dimensions: { date: { sql: 'date', type: 'time' } }` |
| `Measure("revenue", type="sum", sql="amount")` | `measures: { revenue: { sql: 'amount', type: 'sum' } }` |
| `Relationship(...)` | `joins: { Customers: { relationship: 'many_to_one', sql: '...' } }` |
| `dash.query(measures=[...], dimensions=[...])` | `POST /cubejs-api/v1/load { "measures": [...], "dimensions": [...] }` |

### PowerBI Mapping

| notebookmd | PowerBI semantic model |
|------------|----------------------|
| `Entity("orders", source=...)` | Table "Orders" in `model.bim` |
| `Dimension("status", type="string")` | Column `Orders[Status]` |
| `Dimension("date", type="time")` | Date table relationship + `Orders[Date]` |
| `Measure("revenue", type="sum", sql="amount")` | DAX: `Total Revenue = SUM(Orders[Amount])` |
| `Measure("aov", sql="revenue / count")` | DAX: `AOV = DIVIDE([Total Revenue], [Order Count])` |
| `Relationship(type="many_to_one")` | Relationship with `crossFilteringBehavior: "oneDirection"` |
| `filter()` | Slicer visual on report page |
| `tile(compare="previous_period")` | DAX: `CALCULATE([Revenue], SAMEPERIODLASTYEAR('Date'[Date]))` |

---

## End-to-End Example

```python
from notebookmd.analytics import Dashboard, Entity, Dimension, Measure, Relationship

# --- Define the model (once, reuse across dashboards) ---

orders = Entity("orders", source="data/orders.csv", dimensions=[
    Dimension("id", type="number", primary_key=True),
    Dimension("date", type="time"),
    Dimension("customer_id", type="number"),
    Dimension("product_id", type="number"),
    Dimension("status", type="string"),
], measures=[
    Measure("revenue", type="sum", sql="amount", format="$,.0f"),
    Measure("count", type="count"),
    Measure("aov", type="number", sql="revenue / count", format="$,.2f"),
])

customers = Entity("customers", source="data/customers.csv", dimensions=[
    Dimension("id", type="number", primary_key=True),
    Dimension("name", type="string"),
    Dimension("segment", type="string"),
    Dimension("region", type="string"),
])

products = Entity("products", source="data/products.csv", dimensions=[
    Dimension("id", type="number", primary_key=True),
    Dimension("category", type="string"),
    Dimension("price", type="number"),
    Dimension("cost", type="number"),
])

rels = [
    Relationship("orders", "customers", on=("customer_id", "id"), type="many_to_one"),
    Relationship("orders", "products", on=("product_id", "id"), type="many_to_one"),
]

# --- Build the dashboard ---

dash = Dashboard(
    title="Weekly Business Review",
    entities=[orders, customers, products],
    relationships=rels,
    output="output/weekly.md",
)

dash.filter("date_range", dimension="orders.date", default="last_30_days")

dash.section("Key Metrics")
dash.tile("orders.revenue", compare="previous_period")
dash.tile("orders.count", compare="previous_period")
dash.tile("orders.aov", compare="previous_period")

dash.section("Revenue Trend")
dash.tile("orders.revenue", by="orders.date", granularity="weekly")

dash.section("By Segment")
dash.tile("orders.revenue", by="customers.segment", type="bar_chart")
dash.tile(["orders.revenue", "orders.count"], by="customers.segment", type="table")

dash.section("By Product Category")
dash.tile("orders.revenue", by="products.category", top=10)

dash.section("Regional Performance")
dash.tile("orders.revenue", by="customers.region", compare="previous_period")

dash.save()
```

**What happens under the hood:**
1. Dashboard loads all sources (CSV → DataFrames)
2. For each tile, resolves the required joins (orders → customers → products)
3. Computes the measures with the right aggregations and groupings
4. Applies global filters (date range)
5. Auto-selects visualization type per tile
6. Renders everything through notebookmd (metric cards, tables, charts)
7. Saves `output/weekly.md` + `output/assets/`

---

## Agent Workflow

An AI agent works at this level:

```python
# 1. Agent discovers data sources
sources = discover("data/")  # auto-detect CSV/Parquet files

# 2. Agent inspects schemas
for entity in sources:
    print(entity.name, entity.dimensions, entity.suggest_measures())

# 3. Agent builds the model
dash = Dashboard.from_entities(sources, auto_join=True)
# auto_join detects foreign keys and creates relationships

# 4. Agent adds tiles (or uses auto_dashboard)
dash.auto_dashboard()  # auto-generates sections + tiles from the model

# 5. Save
dash.save()
```

Or for a specific analysis:

```python
# Agent uses the Cube-style query API
result = dash.query(
    measures=["orders.revenue"],
    dimensions=["customers.segment"],
    filters=[("orders.date", "gte", "2026-01-01")],
)
# result is a DataFrame — agent can reason about it, then decide what to render
```

---

## Architecture

```
notebookmd/
├── analytics/                  # NEW: The analytics platform
│   ├── __init__.py             # Public API: Dashboard, Entity, Dimension, Measure, etc.
│   ├── model.py                # Entity, Dimension, Measure, Relationship
│   ├── dashboard.py            # Dashboard: tiles, filters, sections, save()
│   ├── query.py                # Query builder: resolve joins, generate SQL/pandas
│   ├── engine.py               # Execution engine: run queries against sources
│   ├── time.py                 # Time intelligence: granularity, period comparison
│   ├── suggest.py              # Auto-discovery: detect dimensions, suggest measures
│   ├── refresh.py              # Re-run + metric diff tracking
│   └── interop/                # Platform connectors
│       ├── __init__.py
│       ├── metabase.py         # from_metabase() / to_metabase()
│       ├── lookml.py           # from_lookml() / to_lookml()
│       ├── cube.py             # from_cube() / to_cube_schema()
│       └── powerbi.py          # from_powerbi() / to_powerbi()
├── core.py                     # Notebook (existing rendering engine)
├── plugins/                    # Widget plugins (existing)
└── ...
```

---

## Implementation Plan

### Phase 1: Core Model
- `Entity`, `Dimension`, `Measure`, `Relationship` dataclasses
- `Dashboard` class with `section()`, `tile()`, `filter()`
- Basic query engine: resolve joins, compute measures on CSV/DataFrames
- Render tiles through notebookmd (metric → `n.metric()`, bar → `n.bar_chart()`, etc.)
- `dash.save()` → Markdown output

### Phase 2: Query Engine
- Composable `Query` object (measures + dimensions + filters + time)
- Automatic join resolution from relationship graph
- Time granularity and period comparison
- Smart chart type selection

### Phase 3: Auto-Discovery
- `discover()` — scan directory for data files, infer entities
- `suggest_measures()` — detect numeric columns → SUM/AVG/COUNT
- `auto_join=True` — detect foreign keys
- `auto_dashboard()` — generate full dashboard from model

### Phase 4: Interop
- `from_metabase()` / `to_metabase()` — API-based import/export
- `from_lookml()` — parse LookML files into Entity/Measure/Relationship
- `to_cube_schema()` — generate Cube YAML from model
- `from_cube()` — import from Cube REST API

### Phase 5: Operations
- `refresh()` with metric diff tracking
- `--refresh` CLI flag
- Parameterized dashboards (date range, filters as CLI args)
- Report index across multiple dashboards

---

## The Positioning

```
Same analytical model as:    Metabase, Looker, PowerBI, Cube
Same data modeling:          Entities + Dimensions + Measures + Joins
Same query pattern:          Select measures + dimensions → results

Different delivery:          Python-defined, Markdown-output, agent-native
Different audience:          AI agents and code-first teams
Different philosophy:        Code, not clicks. Files, not servers.
```

Import a Metabase dashboard → get a Markdown version.
Define a model in Python → export to Looker or Cube.
Let an agent build a dashboard → renders to `.md` automatically.

**One data model. Every BI platform. Markdown output.**
