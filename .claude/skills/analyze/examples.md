# Analyze Skill — Examples

## Example 1: CSV File Analysis

```python
from notebookmd import nb, NotebookConfig
import pandas as pd

cfg = NotebookConfig(max_table_rows=25)
st = nb("dist/csv_analysis.md", title="Sales Data Analysis", cfg=cfg)

df = pd.read_csv("sales.csv")

st.section("Data Overview")
st.kv({
    "File": "sales.csv",
    "Records": f"{len(df):,}",
    "Columns": ", ".join(df.columns),
    "Date Range": f"{df['date'].min()} to {df['date'].max()}",
}, title="Dataset")
st.summary(df, title="Statistical Summary")

st.section("Key Metrics")
total_rev = df["revenue"].sum()
avg_order = df["revenue"].mean()
top_product = df.groupby("product")["revenue"].sum().idxmax()
st.metric_row([
    {"label": "Total Revenue", "value": f"${total_rev:,.0f}"},
    {"label": "Avg Order", "value": f"${avg_order:,.2f}"},
    {"label": "Top Product", "value": top_product},
])

st.section("Revenue by Product")
by_product = df.groupby("product")["revenue"].agg(["sum", "mean", "count"]).sort_values("sum", ascending=False)
st.table(by_product.reset_index(), name="Product Performance")

st.section("Trend")
st.line_chart(df.groupby("date")["revenue"].sum().reset_index(), x="date", y="revenue", title="Daily Revenue")

st.section("Export")
st.export_csv(df, "sales_processed.csv", name="Processed sales data")
st.success("Analysis complete!")
st.save()
```

## Example 2: Financial Stock Analysis

```python
from notebookmd import nb
import pandas as pd

st = nb("dist/stock_analysis.md", title="VCB Stock Analysis")

df = pd.read_csv("vcb_prices.csv", parse_dates=["date"])

st.section("Price Overview")
latest = df.iloc[-1]
prev = df.iloc[-2]
st.metric("Close", f"{latest['close']:,.0f}", delta=f"{latest['close'] - prev['close']:+,.0f}")
st.change("Price", current=latest["close"], previous=df.iloc[0]["close"], fmt=",.0f", pct=True)

st.section("Technical Indicators")
df["sma_20"] = df["close"].rolling(20).mean()
df["rsi"] = 50  # simplified
st.kv({
    "SMA 20": f"{df['sma_20'].iloc[-1]:,.0f}",
    "52-Week High": f"{df['close'].max():,.0f}",
    "52-Week Low": f"{df['close'].min():,.0f}",
    "Avg Volume": f"{df['volume'].mean():,.0f}",
}, title="Indicators")
st.badge("BULLISH", style="success")

st.section("Price Chart")
st.line_chart(df, x="date", y="close", title="VCB Daily Close")

st.section("Volume Analysis")
st.bar_chart(df.tail(20), x="date", y="volume", title="Recent Volume")

st.save()
```

## Example 3: Quick DataFrame Exploration

```python
from notebookmd import nb
import pandas as pd

st = nb("dist/explore.md", title="Data Exploration")

df = pd.read_csv("dataset.csv")

st.section("Shape & Types")
st.kv({
    "Rows": f"{len(df):,}",
    "Columns": str(len(df.columns)),
    "Memory": f"{df.memory_usage(deep=True).sum() / 1e6:.1f} MB",
}, title="Dataset Shape")

st.section("Summary Statistics")
st.summary(df, title="Auto Summary")

st.section("Sample Data")
st.dataframe(df.head(20), name="First 20 Rows")
st.dataframe(df.tail(10), name="Last 10 Rows")

st.section("Value Counts")
for col in df.select_dtypes(include="object").columns[:5]:
    st.kv(df[col].value_counts().head(10).to_dict(), title=f"{col} Distribution")

st.export_csv(df.describe(), "summary_stats.csv", name="Summary statistics")
st.save()
```
