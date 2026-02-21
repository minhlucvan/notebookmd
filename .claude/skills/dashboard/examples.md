# Dashboard Skill — Examples

## Example 1: SaaS Metrics Dashboard

```python
from notebookmd import nb

st = nb("dist/saas_dashboard.md", title="SaaS Metrics Dashboard — January 2026")

st.section("Hero Metrics")
st.metric_row([
    {"label": "MRR", "value": "$350K", "delta": "+$28K"},
    {"label": "ARR", "value": "$4.2M", "delta": "+18%"},
    {"label": "Customers", "value": "1,234", "delta": "+89"},
    {"label": "Churn", "value": "1.8%", "delta": "-0.3%", "delta_color": "inverse"},
])
st.badge("ALL GREEN", style="success")

st.section("Unit Economics")
st.kv({
    "LTV": "$14,400",
    "CAC": "$2,100",
    "LTV/CAC": "6.9x",
    "Payback Period": "5.2 months",
    "Gross Margin": "82%",
}, title="Unit Economics")

st.section("Growth")
st.change("MRR", current=350_000, previous=322_000, fmt=",.0f", pct=True)
st.change("Customers", current=1234, previous=1145, fmt=",d", pct=True)
st.change("ARPU", current=284, previous=281, fmt=",.0f", pct=True)

st.section("Segment Performance")
st.ranking("Enterprise", value="$180K MRR", rank=1, total=3)
st.ranking("SMB", value="$120K MRR", rank=2, total=3)
st.ranking("Self-Serve", value="$50K MRR", rank=3, total=3)

st.section("Alerts")
st.success("MRR target of $340K exceeded")
st.warning("Enterprise churn increased 0.2pp — monitor closely")
st.info("New pricing tier launching Feb 15")

st.save()
```

## Example 2: Portfolio Dashboard

```python
from notebookmd import nb
import pandas as pd

st = nb("dist/portfolio.md", title="Investment Portfolio Dashboard")

st.section("Portfolio Summary")
st.metric_row([
    {"label": "Total Value", "value": "$2.4M", "delta": "+$180K"},
    {"label": "Day P&L", "value": "+$12,340", "delta": "+0.52%"},
    {"label": "YTD Return", "value": "+14.2%", "delta": "+14.2%"},
    {"label": "Sharpe", "value": "1.84"},
])

st.section("Asset Allocation")
st.kv({
    "Equities": "62% ($1.49M)",
    "Fixed Income": "25% ($600K)",
    "Alternatives": "8% ($192K)",
    "Cash": "5% ($120K)",
}, title="Allocation")

st.section("Top Holdings")
st.ranking("AAPL", value="$340K", rank=1, total=25, percentile=96)
st.ranking("MSFT", value="$280K", rank=2, total=25, percentile=92)
st.ranking("GOOGL", value="$210K", rank=3, total=25, percentile=88)

st.section("Risk Metrics")
st.stats([
    {"label": "VaR (95%)", "value": -45_000, "fmt": ",.0f"},
    {"label": "Max Drawdown", "value": -0.082, "fmt": ".1%"},
    {"label": "Beta", "value": 0.95, "fmt": ".2f"},
])

st.save()
```
