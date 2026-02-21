# Analyze Skill — Examples

## Example 1: CSV File Analysis

```python
from notebookmd import nb, NotebookConfig
import pandas as pd

cfg = NotebookConfig(max_table_rows=25)
n = nb("dist/csv_analysis.md", title="Sales Data Analysis", cfg=cfg)

df = pd.read_csv("sales.csv")

n.section("Data Overview")
n.kv({
    "File": "sales.csv",
    "Records": f"{len(df):,}",
    "Columns": ", ".join(df.columns),
    "Date Range": f"{df['date'].min()} to {df['date'].max()}",
}, title="Dataset")
n.summary(df, title="Statistical Summary")

n.section("Key Metrics")
total_rev = df["revenue"].sum()
avg_order = df["revenue"].mean()
top_product = df.groupby("product")["revenue"].sum().idxmax()
n.metric_row([
    {"label": "Total Revenue", "value": f"${total_rev:,.0f}"},
    {"label": "Avg Order", "value": f"${avg_order:,.2f}"},
    {"label": "Top Product", "value": top_product},
])

n.section("Revenue by Product")
by_product = df.groupby("product")["revenue"].agg(["sum", "mean", "count"]).sort_values("sum", ascending=False)
n.table(by_product.reset_index(), name="Product Performance")

n.section("Trend")
n.line_chart(df.groupby("date")["revenue"].sum().reset_index(), x="date", y="revenue", title="Daily Revenue")

n.section("Export")
n.export_csv(df, "sales_processed.csv", name="Processed sales data")
n.success("Analysis complete!")
n.save()
```

## Example 2: Financial Stock Analysis

```python
from notebookmd import nb
import pandas as pd

n = nb("dist/stock_analysis.md", title="AAPL Stock Analysis")

df = pd.read_csv("aapl_prices.csv", parse_dates=["date"])

n.section("Price Overview")
latest = df.iloc[-1]
prev = df.iloc[-2]
n.metric("Close", f"{latest['close']:,.0f}", delta=f"{latest['close'] - prev['close']:+,.0f}")
n.change("Price", current=latest["close"], previous=df.iloc[0]["close"], fmt=",.0f", pct=True)

n.section("Technical Indicators")
df["sma_20"] = df["close"].rolling(20).mean()
df["rsi"] = 50  # simplified
n.kv({
    "SMA 20": f"{df['sma_20'].iloc[-1]:,.0f}",
    "52-Week High": f"{df['close'].max():,.0f}",
    "52-Week Low": f"{df['close'].min():,.0f}",
    "Avg Volume": f"{df['volume'].mean():,.0f}",
}, title="Indicators")
n.badge("BULLISH", style="success")

n.section("Price Chart")
n.line_chart(df, x="date", y="close", title="AAPL Daily Close")

n.section("Volume Analysis")
n.bar_chart(df.tail(20), x="date", y="volume", title="Recent Volume")

n.save()
```

## Example 3: Quick DataFrame Exploration

```python
from notebookmd import nb
import pandas as pd

n = nb("dist/explore.md", title="Data Exploration")

df = pd.read_csv("dataset.csv")

n.section("Shape & Types")
n.kv({
    "Rows": f"{len(df):,}",
    "Columns": str(len(df.columns)),
    "Memory": f"{df.memory_usage(deep=True).sum() / 1e6:.1f} MB",
}, title="Dataset Shape")

n.section("Summary Statistics")
n.summary(df, title="Auto Summary")

n.section("Sample Data")
n.dataframe(df.head(20), name="First 20 Rows")
n.dataframe(df.tail(10), name="Last 10 Rows")

n.section("Value Counts")
for col in df.select_dtypes(include="object").columns[:5]:
    n.kv(df[col].value_counts().head(10).to_dict(), title=f"{col} Distribution")

n.export_csv(df.describe(), "summary_stats.csv", name="Summary statistics")
n.save()
```
