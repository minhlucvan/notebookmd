# notebookmd — Working Examples

## Example 1: CSV Data Analysis

Analyze a CSV file with statistics, segmentation, trends, and export.

```python
from notebookmd import nb, NotebookConfig
import pandas as pd

cfg = NotebookConfig(max_table_rows=25)
n = nb("dist/csv_analysis.md", title="Sales Data Analysis", cfg=cfg)

df = pd.read_csv("sales.csv")

# ── Data Overview ──
n.section("Data Overview")
n.kv({
    "File": "sales.csv",
    "Records": f"{len(df):,}",
    "Columns": ", ".join(df.columns),
    "Date Range": f"{df['date'].min()} to {df['date'].max()}",
}, title="Dataset")
n.summary(df, title="Statistical Summary")

# ── Key Metrics ──
n.section("Key Metrics")
total_rev = df["revenue"].sum()
avg_order = df["revenue"].mean()
top_product = df.groupby("product")["revenue"].sum().idxmax()
n.metric_row([
    {"label": "Total Revenue", "value": f"${total_rev:,.0f}"},
    {"label": "Avg Order", "value": f"${avg_order:,.2f}"},
    {"label": "Top Product", "value": top_product},
])

# ── Revenue by Product ──
n.section("Revenue by Product")
by_product = (
    df.groupby("product")["revenue"]
    .agg(["sum", "mean", "count"])
    .sort_values("sum", ascending=False)
)
n.table(by_product.reset_index(), name="Product Performance")

# ── Trend ──
n.section("Trend")
n.line_chart(
    df.groupby("date")["revenue"].sum().reset_index(),
    x="date", y="revenue", title="Daily Revenue"
)

# ── Export ──
n.section("Export")
n.export_csv(df, "sales_processed.csv", name="Processed sales data")
n.success("Analysis complete!")
n.save()
```

---

## Example 2: SaaS Metrics Dashboard

Build a KPI dashboard with hero metrics, unit economics, rankings, and alerts.

```python
from notebookmd import nb

n = nb("dist/saas_dashboard.md", title="SaaS Metrics Dashboard — January 2026")

# ── Hero Metrics ──
n.section("Hero Metrics")
n.metric_row([
    {"label": "MRR", "value": "$350K", "delta": "+$28K"},
    {"label": "ARR", "value": "$4.2M", "delta": "+18%"},
    {"label": "Customers", "value": "1,234", "delta": "+89"},
    {"label": "Churn", "value": "1.8%", "delta": "-0.3%", "delta_color": "inverse"},
])
n.badge("ALL GREEN", style="success")

# ── Unit Economics ──
n.section("Unit Economics")
n.kv({
    "LTV": "$14,400",
    "CAC": "$2,100",
    "LTV/CAC": "6.9x",
    "Payback Period": "5.2 months",
    "Gross Margin": "82%",
}, title="Unit Economics")

# ── Growth ──
n.section("Growth")
n.change("MRR", current=350_000, previous=322_000, fmt=",.0f", pct=True)
n.change("Customers", current=1234, previous=1145, fmt=",d", pct=True)
n.change("ARPU", current=284, previous=281, fmt=",.0f", pct=True)

# ── Segment Rankings ──
n.section("Segment Performance")
n.ranking("Enterprise", value="$180K MRR", rank=1, total=3)
n.ranking("SMB", value="$120K MRR", rank=2, total=3)
n.ranking("Self-Serve", value="$50K MRR", rank=3, total=3)

# ── Alerts ──
n.section("Alerts")
n.success("MRR target of $340K exceeded")
n.warning("Enterprise churn increased 0.2pp — monitor closely")
n.info("New pricing tier launching Feb 15")

n.save()
```

---

## Example 3: Stock / Financial Analysis

Analyze stock price data with technical indicators, charts, and volume analysis.

```python
from notebookmd import nb
import pandas as pd

n = nb("dist/stock_analysis.md", title="AAPL Stock Analysis")

df = pd.read_csv("aapl_prices.csv", parse_dates=["date"])

# ── Price Overview ──
n.section("Price Overview")
latest = df.iloc[-1]
prev = df.iloc[-2]
n.metric("Close", f"{latest['close']:,.0f}", delta=f"{latest['close'] - prev['close']:+,.0f}")
n.change("Price", current=latest["close"], previous=df.iloc[0]["close"], fmt=",.0f", pct=True)

# ── Technical Indicators ──
n.section("Technical Indicators")
df["sma_20"] = df["close"].rolling(20).mean()
n.kv({
    "SMA 20": f"{df['sma_20'].iloc[-1]:,.0f}",
    "52-Week High": f"{df['close'].max():,.0f}",
    "52-Week Low": f"{df['close'].min():,.0f}",
    "Avg Volume": f"{df['volume'].mean():,.0f}",
}, title="Indicators")
n.badge("BULLISH", style="success")

# ── Charts ──
n.section("Price Chart")
n.line_chart(df, x="date", y="close", title="AAPL Daily Close")

n.section("Volume Analysis")
n.bar_chart(df.tail(20), x="date", y="volume", title="Recent Volume")

n.save()
```

---

## Example 4: Portfolio Dashboard

Investment portfolio overview with allocation, risk metrics, and top holdings.

```python
from notebookmd import nb

n = nb("dist/portfolio.md", title="Investment Portfolio Dashboard")

# ── Portfolio Summary ──
n.section("Portfolio Summary")
n.metric_row([
    {"label": "Total Value", "value": "$2.4M", "delta": "+$180K"},
    {"label": "Day P&L", "value": "+$12,340", "delta": "+0.52%"},
    {"label": "YTD Return", "value": "+14.2%", "delta": "+14.2%"},
    {"label": "Sharpe", "value": "1.84"},
])

# ── Asset Allocation ──
n.section("Asset Allocation")
n.kv({
    "Equities": "62% ($1.49M)",
    "Fixed Income": "25% ($600K)",
    "Alternatives": "8% ($192K)",
    "Cash": "5% ($120K)",
}, title="Allocation")

# ── Top Holdings ──
n.section("Top Holdings")
n.ranking("AAPL", value="$340K", rank=1, total=25, percentile=96)
n.ranking("MSFT", value="$280K", rank=2, total=25, percentile=92)
n.ranking("GOOGL", value="$210K", rank=3, total=25, percentile=88)

# ── Risk Metrics ──
n.section("Risk Metrics")
n.stats([
    {"label": "VaR (95%)", "value": -45_000, "fmt": ",.0f"},
    {"label": "Max Drawdown", "value": -0.082, "fmt": ".1%"},
    {"label": "Beta", "value": 0.95, "fmt": ".2f"},
])

n.save()
```

---

## Example 5: Quick DataFrame Exploration

Rapid inspection of any dataset — shape, types, distributions, samples.

```python
from notebookmd import nb
import pandas as pd

n = nb("dist/explore.md", title="Data Exploration")

df = pd.read_csv("dataset.csv")

# ── Shape & Types ──
n.section("Shape & Types")
n.kv({
    "Rows": f"{len(df):,}",
    "Columns": str(len(df.columns)),
    "Memory": f"{df.memory_usage(deep=True).sum() / 1e6:.1f} MB",
}, title="Dataset Shape")

# ── Summary Statistics ──
n.section("Summary Statistics")
n.summary(df, title="Auto Summary")

# ── Sample Data ──
n.section("Sample Data")
n.dataframe(df.head(20), name="First 20 Rows")
n.dataframe(df.tail(10), name="Last 10 Rows")

# ── Value Counts ──
n.section("Value Counts")
for col in df.select_dtypes(include="object").columns[:5]:
    n.kv(df[col].value_counts().head(10).to_dict(), title=f"{col} Distribution")

# ── Export ──
n.export_csv(df.describe(), "summary_stats.csv", name="Summary statistics")
n.save()
```

---

## Example 6: A/B Test Results Report

Structured report for experiment results with statistical outcomes.

```python
from notebookmd import nb
import pandas as pd

n = nb("dist/ab_ten.md", title="A/B Test Results — Checkout Flow Redesign")

# ── Experiment Summary ──
n.section("Experiment Summary")
n.kv({
    "Hypothesis": "New checkout reduces cart abandonment",
    "Duration": "14 days (Jan 5–19, 2026)",
    "Traffic Split": "50/50",
    "Sample Size": "24,500 users per variant",
}, title="Experiment Config")

# ── Key Results ──
n.section("Key Results")
n.metric_row([
    {"label": "Control CR", "value": "3.2%"},
    {"label": "Variant CR", "value": "4.1%", "delta": "+0.9pp"},
    {"label": "Lift", "value": "+28.1%", "delta": "+28.1%"},
    {"label": "p-value", "value": "0.003"},
])
n.badge("STATISTICALLY SIGNIFICANT", style="success")

# ── Segment Breakdown ──
n.section("Segment Breakdown")
segments = pd.DataFrame({
    "Segment": ["Mobile", "Desktop", "New Users", "Returning"],
    "Control": ["2.8%", "3.9%", "2.1%", "4.5%"],
    "Variant": ["3.9%", "4.4%", "3.2%", "5.0%"],
    "Lift": ["+39%", "+13%", "+52%", "+11%"],
    "Significant": ["Yes", "No", "Yes", "No"],
})
n.table(segments, name="Conversion by Segment")

# ── Recommendation ──
n.section("Recommendation")
n.success("Roll out new checkout flow to 100% of traffic")
n.warning("Desktop segment shows marginal lift — monitor post-launch")
n.info("Follow-up test planned for payment page optimization")

n.save()
```

---

## Example 7: Multi-Tab Technical Report

Using tabs and expanders for progressive disclosure.

```python
from notebookmd import nb
import pandas as pd

n = nb("dist/technical_report.md", title="System Performance Report")

# ── Overview ──
n.section("Overview")
n.metric_row([
    {"label": "Uptime", "value": "99.97%", "delta": "+0.02%"},
    {"label": "Avg Latency", "value": "45ms", "delta": "-8ms"},
    {"label": "Error Rate", "value": "0.03%", "delta": "-0.01%", "delta_color": "inverse"},
    {"label": "RPS", "value": "12.4K", "delta": "+2.1K"},
])

# ── Service Health ──
n.section("Service Health")
tabs = n.tabs(["API Gateway", "Database", "Cache"])

with tabs.tab("API Gateway"):
    n.stats([
        {"label": "p50", "value": 12, "fmt": "d"},
        {"label": "p95", "value": 45, "fmt": "d"},
        {"label": "p99", "value": 180, "fmt": "d"},
    ])
    n.badge("HEALTHY", style="success")

with tabs.tab("Database"):
    n.stats([
        {"label": "Connections", "value": 145, "fmt": "d"},
        {"label": "QPS", "value": 3200, "fmt": ",d"},
        {"label": "Slow Queries", "value": 3, "fmt": "d"},
    ])
    n.badge("WARNING", style="warning")

with tabs.tab("Cache"):
    n.stats([
        {"label": "Hit Rate", "value": 0.94, "fmt": ".0%"},
        {"label": "Memory", "value": 0.72, "fmt": ".0%"},
        {"label": "Evictions/s", "value": 12, "fmt": "d"},
    ])
    n.badge("HEALTHY", style="success")

# ── Methodology ──
with n.expander("Methodology"):
    n.write("Metrics collected from Prometheus over 7-day rolling window.")
    n.write("Latency percentiles computed at 1-minute granularity.")
    n.code("SELECT percentile_disc(0.99) WITHIN GROUP (ORDER BY latency) FROM requests", lang="sql")

n.save()
```
