# notebookmd — Working Examples

## Example 1: CSV Data Analysis

Analyze a CSV file with statistics, segmentation, trends, and export.

```python
from notebookmd import nb, NotebookConfig
import pandas as pd

cfg = NotebookConfig(max_table_rows=25)
st = nb("dist/csv_analysis.md", title="Sales Data Analysis", cfg=cfg)

df = pd.read_csv("sales.csv")

# ── Data Overview ──
st.section("Data Overview")
st.kv({
    "File": "sales.csv",
    "Records": f"{len(df):,}",
    "Columns": ", ".join(df.columns),
    "Date Range": f"{df['date'].min()} to {df['date'].max()}",
}, title="Dataset")
st.summary(df, title="Statistical Summary")

# ── Key Metrics ──
st.section("Key Metrics")
total_rev = df["revenue"].sum()
avg_order = df["revenue"].mean()
top_product = df.groupby("product")["revenue"].sum().idxmax()
st.metric_row([
    {"label": "Total Revenue", "value": f"${total_rev:,.0f}"},
    {"label": "Avg Order", "value": f"${avg_order:,.2f}"},
    {"label": "Top Product", "value": top_product},
])

# ── Revenue by Product ──
st.section("Revenue by Product")
by_product = (
    df.groupby("product")["revenue"]
    .agg(["sum", "mean", "count"])
    .sort_values("sum", ascending=False)
)
st.table(by_product.reset_index(), name="Product Performance")

# ── Trend ──
st.section("Trend")
st.line_chart(
    df.groupby("date")["revenue"].sum().reset_index(),
    x="date", y="revenue", title="Daily Revenue"
)

# ── Export ──
st.section("Export")
st.export_csv(df, "sales_processed.csv", name="Processed sales data")
st.success("Analysis complete!")
st.save()
```

---

## Example 2: SaaS Metrics Dashboard

Build a KPI dashboard with hero metrics, unit economics, rankings, and alerts.

```python
from notebookmd import nb

st = nb("dist/saas_dashboard.md", title="SaaS Metrics Dashboard — January 2026")

# ── Hero Metrics ──
st.section("Hero Metrics")
st.metric_row([
    {"label": "MRR", "value": "$350K", "delta": "+$28K"},
    {"label": "ARR", "value": "$4.2M", "delta": "+18%"},
    {"label": "Customers", "value": "1,234", "delta": "+89"},
    {"label": "Churn", "value": "1.8%", "delta": "-0.3%", "delta_color": "inverse"},
])
st.badge("ALL GREEN", style="success")

# ── Unit Economics ──
st.section("Unit Economics")
st.kv({
    "LTV": "$14,400",
    "CAC": "$2,100",
    "LTV/CAC": "6.9x",
    "Payback Period": "5.2 months",
    "Gross Margin": "82%",
}, title="Unit Economics")

# ── Growth ──
st.section("Growth")
st.change("MRR", current=350_000, previous=322_000, fmt=",.0f", pct=True)
st.change("Customers", current=1234, previous=1145, fmt=",d", pct=True)
st.change("ARPU", current=284, previous=281, fmt=",.0f", pct=True)

# ── Segment Rankings ──
st.section("Segment Performance")
st.ranking("Enterprise", value="$180K MRR", rank=1, total=3)
st.ranking("SMB", value="$120K MRR", rank=2, total=3)
st.ranking("Self-Serve", value="$50K MRR", rank=3, total=3)

# ── Alerts ──
st.section("Alerts")
st.success("MRR target of $340K exceeded")
st.warning("Enterprise churn increased 0.2pp — monitor closely")
st.info("New pricing tier launching Feb 15")

st.save()
```

---

## Example 3: Stock / Financial Analysis

Analyze stock price data with technical indicators, charts, and volume analysis.

```python
from notebookmd import nb
import pandas as pd

st = nb("dist/stock_analysis.md", title="VCB Stock Analysis")

df = pd.read_csv("vcb_prices.csv", parse_dates=["date"])

# ── Price Overview ──
st.section("Price Overview")
latest = df.iloc[-1]
prev = df.iloc[-2]
st.metric("Close", f"{latest['close']:,.0f}", delta=f"{latest['close'] - prev['close']:+,.0f}")
st.change("Price", current=latest["close"], previous=df.iloc[0]["close"], fmt=",.0f", pct=True)

# ── Technical Indicators ──
st.section("Technical Indicators")
df["sma_20"] = df["close"].rolling(20).mean()
st.kv({
    "SMA 20": f"{df['sma_20'].iloc[-1]:,.0f}",
    "52-Week High": f"{df['close'].max():,.0f}",
    "52-Week Low": f"{df['close'].min():,.0f}",
    "Avg Volume": f"{df['volume'].mean():,.0f}",
}, title="Indicators")
st.badge("BULLISH", style="success")

# ── Charts ──
st.section("Price Chart")
st.line_chart(df, x="date", y="close", title="VCB Daily Close")

st.section("Volume Analysis")
st.bar_chart(df.tail(20), x="date", y="volume", title="Recent Volume")

st.save()
```

---

## Example 4: Portfolio Dashboard

Investment portfolio overview with allocation, risk metrics, and top holdings.

```python
from notebookmd import nb

st = nb("dist/portfolio.md", title="Investment Portfolio Dashboard")

# ── Portfolio Summary ──
st.section("Portfolio Summary")
st.metric_row([
    {"label": "Total Value", "value": "$2.4M", "delta": "+$180K"},
    {"label": "Day P&L", "value": "+$12,340", "delta": "+0.52%"},
    {"label": "YTD Return", "value": "+14.2%", "delta": "+14.2%"},
    {"label": "Sharpe", "value": "1.84"},
])

# ── Asset Allocation ──
st.section("Asset Allocation")
st.kv({
    "Equities": "62% ($1.49M)",
    "Fixed Income": "25% ($600K)",
    "Alternatives": "8% ($192K)",
    "Cash": "5% ($120K)",
}, title="Allocation")

# ── Top Holdings ──
st.section("Top Holdings")
st.ranking("AAPL", value="$340K", rank=1, total=25, percentile=96)
st.ranking("MSFT", value="$280K", rank=2, total=25, percentile=92)
st.ranking("GOOGL", value="$210K", rank=3, total=25, percentile=88)

# ── Risk Metrics ──
st.section("Risk Metrics")
st.stats([
    {"label": "VaR (95%)", "value": -45_000, "fmt": ",.0f"},
    {"label": "Max Drawdown", "value": -0.082, "fmt": ".1%"},
    {"label": "Beta", "value": 0.95, "fmt": ".2f"},
])

st.save()
```

---

## Example 5: Quick DataFrame Exploration

Rapid inspection of any dataset — shape, types, distributions, samples.

```python
from notebookmd import nb
import pandas as pd

st = nb("dist/explore.md", title="Data Exploration")

df = pd.read_csv("dataset.csv")

# ── Shape & Types ──
st.section("Shape & Types")
st.kv({
    "Rows": f"{len(df):,}",
    "Columns": str(len(df.columns)),
    "Memory": f"{df.memory_usage(deep=True).sum() / 1e6:.1f} MB",
}, title="Dataset Shape")

# ── Summary Statistics ──
st.section("Summary Statistics")
st.summary(df, title="Auto Summary")

# ── Sample Data ──
st.section("Sample Data")
st.dataframe(df.head(20), name="First 20 Rows")
st.dataframe(df.tail(10), name="Last 10 Rows")

# ── Value Counts ──
st.section("Value Counts")
for col in df.select_dtypes(include="object").columns[:5]:
    st.kv(df[col].value_counts().head(10).to_dict(), title=f"{col} Distribution")

# ── Export ──
st.export_csv(df.describe(), "summary_stats.csv", name="Summary statistics")
st.save()
```

---

## Example 6: A/B Test Results Report

Structured report for experiment results with statistical outcomes.

```python
from notebookmd import nb
import pandas as pd

st = nb("dist/ab_test.md", title="A/B Test Results — Checkout Flow Redesign")

# ── Experiment Summary ──
st.section("Experiment Summary")
st.kv({
    "Hypothesis": "New checkout reduces cart abandonment",
    "Duration": "14 days (Jan 5–19, 2026)",
    "Traffic Split": "50/50",
    "Sample Size": "24,500 users per variant",
}, title="Experiment Config")

# ── Key Results ──
st.section("Key Results")
st.metric_row([
    {"label": "Control CR", "value": "3.2%"},
    {"label": "Variant CR", "value": "4.1%", "delta": "+0.9pp"},
    {"label": "Lift", "value": "+28.1%", "delta": "+28.1%"},
    {"label": "p-value", "value": "0.003"},
])
st.badge("STATISTICALLY SIGNIFICANT", style="success")

# ── Segment Breakdown ──
st.section("Segment Breakdown")
segments = pd.DataFrame({
    "Segment": ["Mobile", "Desktop", "New Users", "Returning"],
    "Control": ["2.8%", "3.9%", "2.1%", "4.5%"],
    "Variant": ["3.9%", "4.4%", "3.2%", "5.0%"],
    "Lift": ["+39%", "+13%", "+52%", "+11%"],
    "Significant": ["Yes", "No", "Yes", "No"],
})
st.table(segments, name="Conversion by Segment")

# ── Recommendation ──
st.section("Recommendation")
st.success("Roll out new checkout flow to 100% of traffic")
st.warning("Desktop segment shows marginal lift — monitor post-launch")
st.info("Follow-up test planned for payment page optimization")

st.save()
```

---

## Example 7: Multi-Tab Technical Report

Using tabs and expanders for progressive disclosure.

```python
from notebookmd import nb
import pandas as pd

st = nb("dist/technical_report.md", title="System Performance Report")

# ── Overview ──
st.section("Overview")
st.metric_row([
    {"label": "Uptime", "value": "99.97%", "delta": "+0.02%"},
    {"label": "Avg Latency", "value": "45ms", "delta": "-8ms"},
    {"label": "Error Rate", "value": "0.03%", "delta": "-0.01%", "delta_color": "inverse"},
    {"label": "RPS", "value": "12.4K", "delta": "+2.1K"},
])

# ── Service Health ──
st.section("Service Health")
tabs = st.tabs(["API Gateway", "Database", "Cache"])

with tabs.tab("API Gateway"):
    st.stats([
        {"label": "p50", "value": 12, "fmt": "d"},
        {"label": "p95", "value": 45, "fmt": "d"},
        {"label": "p99", "value": 180, "fmt": "d"},
    ])
    st.badge("HEALTHY", style="success")

with tabs.tab("Database"):
    st.stats([
        {"label": "Connections", "value": 145, "fmt": "d"},
        {"label": "QPS", "value": 3200, "fmt": ",d"},
        {"label": "Slow Queries", "value": 3, "fmt": "d"},
    ])
    st.badge("WARNING", style="warning")

with tabs.tab("Cache"):
    st.stats([
        {"label": "Hit Rate", "value": 0.94, "fmt": ".0%"},
        {"label": "Memory", "value": 0.72, "fmt": ".0%"},
        {"label": "Evictions/s", "value": 12, "fmt": "d"},
    ])
    st.badge("HEALTHY", style="success")

# ── Methodology ──
with st.expander("Methodology"):
    st.write("Metrics collected from Prometheus over 7-day rolling window.")
    st.write("Latency percentiles computed at 1-minute granularity.")
    st.code("SELECT percentile_disc(0.99) WITHIN GROUP (ORDER BY latency) FROM requests", lang="sql")

st.save()
```
