# notebookmd — Analysis Patterns & Recipes

Reusable patterns for common data analysis tasks. Copy and adapt these recipes.

---

## Pattern 1: CSV File Analysis

When given a CSV file, follow this structure:

```python
from notebookmd import nb, NotebookConfig
import pandas as pd

cfg = NotebookConfig(max_table_rows=25)
st = nb("dist/analysis.md", title="<Descriptive Title>", cfg=cfg)

df = pd.read_csv("data.csv")

# 1. Data Overview
st.section("Data Overview")
st.kv({
    "File": "data.csv",
    "Records": f"{len(df):,}",
    "Columns": str(len(df.columns)),
}, title="Dataset Info")
st.summary(df, title="Statistical Summary")

# 2. Key Metrics
st.section("Key Metrics")
st.metric_row([...])

# 3. Segmentation
st.section("Segmentation")
grouped = df.groupby("category")[target].agg(["sum", "mean", "count"])
st.table(grouped.reset_index(), name="By Category")

# 4. Trends
st.section("Trends")
st.line_chart(df, x="date", y=target, title="Trend")

# 5. Conclusion
st.section("Conclusion")
st.success("Key finding")
st.export_csv(df, "processed.csv", name="Processed data")
st.save()
```

---

## Pattern 2: Comparison Report

Compare two groups, periods, or variants:

```python
st.section("Comparison")
st.change("Metric A", current=current_a, previous=previous_a, fmt=",.0f", pct=True)
st.change("Metric B", current=current_b, previous=previous_b, fmt=",.0f", pct=True)
st.change("Metric C", current=current_c, previous=previous_c, fmt=".1%", pct=True)

# Side-by-side table
comparison = pd.DataFrame({
    "Metric": ["Revenue", "Users", "ARPU"],
    "Period A": [100_000, 500, 200],
    "Period B": [120_000, 600, 200],
    "Change": ["+20%", "+20%", "0%"],
})
st.table(comparison, name="Period Comparison")
```

---

## Pattern 3: KPI Dashboard

Lead with hero metrics, follow with detail sections:

```python
# Hero row — the 3-5 most important numbers
st.section("KPIs")
st.metric_row([
    {"label": "Primary KPI", "value": "...", "delta": "..."},
    {"label": "Secondary KPI", "value": "...", "delta": "..."},
    {"label": "Guard Rail", "value": "...", "delta": "...", "delta_color": "inverse"},
])
st.badge("STATUS", style="success")

# Detail sections
st.section("Breakdown")
st.kv({...}, title="Sub-metrics")

st.section("Rankings")
for i, (name, val) in enumerate(top_items, 1):
    st.ranking(name, value=val, rank=i, total=len(all_items))

st.section("Alerts")
st.success("...")
st.warning("...")
```

---

## Pattern 4: Exploratory Data Analysis (EDA)

Quick exploration of an unknown dataset:

```python
st.section("Shape")
st.kv({
    "Rows": f"{len(df):,}",
    "Columns": str(len(df.columns)),
    "Memory": f"{df.memory_usage(deep=True).sum() / 1e6:.1f} MB",
    "Duplicates": f"{df.duplicated().sum():,}",
    "Null %": f"{df.isnull().mean().mean():.1%}",
}, title="Dataset Shape")

st.section("Types")
type_counts = df.dtypes.value_counts().to_dict()
st.kv({str(k): str(v) for k, v in type_counts.items()}, title="Column Types")

st.section("Numeric Summary")
st.summary(df, title="Auto Summary")

st.section("Sample")
st.dataframe(df.head(20), name="First 20 Rows")

st.section("Distributions")
for col in df.select_dtypes(include="object").columns[:5]:
    st.kv(
        df[col].value_counts().head(10).to_dict(),
        title=f"{col} Distribution"
    )

st.section("Correlations")
numeric_cols = df.select_dtypes(include="number")
if len(numeric_cols.columns) > 1:
    corr = numeric_cols.corr()
    st.table(corr.round(3), name="Correlation Matrix")
```

---

## Pattern 5: Financial / Stock Analysis

```python
# Price metrics
st.section("Price Overview")
latest = df.iloc[-1]
st.metric("Close", f"{latest['close']:,.2f}", delta=f"{latest['close'] - df.iloc[-2]['close']:+,.2f}")
st.change("Price", current=latest["close"], previous=df.iloc[0]["close"], fmt=",.2f", pct=True)

# Technical indicators
st.section("Technical Indicators")
df["sma_20"] = df["close"].rolling(20).mean()
df["sma_50"] = df["close"].rolling(50).mean()
df["daily_return"] = df["close"].pct_change()
st.kv({
    "SMA 20": f"{df['sma_20'].iloc[-1]:,.2f}",
    "SMA 50": f"{df['sma_50'].iloc[-1]:,.2f}",
    "52W High": f"{df['close'].max():,.2f}",
    "52W Low": f"{df['close'].min():,.2f}",
    "Avg Daily Vol": f"{df['volume'].mean():,.0f}",
    "Volatility (ann.)": f"{df['daily_return'].std() * (252**0.5):.1%}",
}, title="Indicators")

# Signal
if df["sma_20"].iloc[-1] > df["sma_50"].iloc[-1]:
    st.badge("BULLISH", style="success")
else:
    st.badge("BEARISH", style="error")

# Charts
st.section("Charts")
st.line_chart(df, x="date", y="close", title="Price History")
st.bar_chart(df.tail(30), x="date", y="volume", title="Recent Volume")
```

---

## Pattern 6: Ranking / Leaderboard

```python
st.section("Top Performers")
ranked = df.sort_values("score", ascending=False).head(10)
for i, row in enumerate(ranked.itertuples(), 1):
    st.ranking(
        row.name,
        value=f"{row.score:,.0f}",
        rank=i,
        total=len(df),
        percentile=round((1 - i / len(df)) * 100),
    )
```

---

## Pattern 7: Status Report

```python
st.section("Status Overview")
st.metric_row([
    {"label": "Complete", "value": "73%", "delta": "+5%"},
    {"label": "On Track", "value": "12/15"},
    {"label": "Blocked", "value": "2"},
])
st.progress(0.73, "Overall completion")

st.section("Completed")
st.write("- Feature A: user auth\n- Feature B: payments\n- Feature C: dashboard")

st.section("In Progress")
st.write("- Feature D: reporting (80%)\n- Feature E: notifications (40%)")

st.section("Risks")
st.warning("Third-party API rate limits may delay Feature D")
st.error("Database migration blocked by schema review")
```

---

## Pattern 8: Multi-Source Analysis

Combine data from multiple files:

```python
st.section("Data Sources")
sources = {
    "sales.csv": pd.read_csv("sales.csv"),
    "customers.csv": pd.read_csv("customers.csv"),
    "products.csv": pd.read_csv("products.csv"),
}
for name, df in sources.items():
    st.kv({"Records": f"{len(df):,}", "Columns": str(len(df.columns))}, title=name)

# Join and analyze
merged = (
    sources["sales.csv"]
    .merge(sources["customers.csv"], on="customer_id")
    .merge(sources["products.csv"], on="product_id")
)

st.section("Combined Analysis")
st.kv({"Merged Records": f"{len(merged):,}"}, title="Join Result")
st.summary(merged, title="Merged Summary")
```

---

## Pattern 9: Progressive Disclosure

Use expanders and tabs to keep the report scannable:

```python
# Executive summary at top
st.section("Executive Summary")
st.metric_row([...])
st.write("One-paragraph summary of key findings...")

# Details hidden in expanders
st.section("Methodology")
with st.expander("Data Collection"):
    st.write("Detailed methodology...")
    st.code("SELECT * FROM events WHERE ...", lang="sql")

with st.expander("Statistical Tests"):
    st.write("Chi-squared test, p < 0.001...")
    st.table(test_results, name="Test Results")

# Raw data in tabs
st.section("Data")
tabs = st.tabs(["Summary", "Full Data", "Export"])
with tabs.tab("Summary"):
    st.summary(df)
with tabs.tab("Full Data"):
    st.dataframe(df, name="All Records")
with tabs.tab("Export"):
    st.export_csv(df, "full_data.csv", name="Complete dataset")
```

---

## Pattern 10: Error Handling for Missing Data

Graceful handling when data might be incomplete:

```python
# Check for required columns
required = ["date", "revenue", "product"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Missing columns: {', '.join(missing)}")
    st.save()
    raise SystemExit(1)

# Report nulls
null_pct = df.isnull().mean()
high_null = null_pct[null_pct > 0.1]
if len(high_null) > 0:
    st.warning(f"Columns with >10% nulls: {', '.join(high_null.index)}")
    st.kv(
        {col: f"{pct:.1%}" for col, pct in high_null.items()},
        title="Null Percentages"
    )

# Safe computation with fallbacks
try:
    trend = df.groupby("date")["revenue"].sum()
    st.line_chart(trend.reset_index(), x="date", y="revenue", title="Revenue Trend")
except Exception as e:
    st.exception(e)
    st.warning("Could not generate trend chart — check data quality")
```

---

## Formatting Cheat Sheet

Common `fmt` strings for `st.stat()`, `st.stats()`, `st.change()`, `st.ranking()`:

| Format | Example Input | Example Output | Use Case |
|--------|--------------|----------------|----------|
| `".2f"` | `3.14159` | `3.14` | Prices, ratios |
| `",.0f"` | `1234567` | `1,234,567` | Revenue, counts |
| `",d"` | `1234567` | `1,234,567` | Integer counts |
| `".1%"` | `0.1234` | `12.3%` | Percentages |
| `".2%"` | `0.1234` | `12.34%` | Precise percentages |
| `"+.1f"` | `3.14` | `+3.1` | Signed values |
| `",.2f"` | `1234.5` | `1,234.50` | Currency amounts |

## Section Organization Best Practices

1. **Data Overview** — Dataset shape, source info, date range
2. **Key Metrics** — 3-5 hero numbers in `metric_row()`
3. **Analysis** — Charts, tables, segmentation
4. **Comparison** — `change()` for period-over-period
5. **Rankings** — `ranking()` for leaderboards
6. **Conclusion** — `success()`/`warning()`/`info()` for takeaways
7. **Export** — `export_csv()` for artifacts
