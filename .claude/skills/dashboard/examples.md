# Dashboard Skill — Examples

## Example 1: SaaS Metrics Dashboard

```python
from notebookmd import nb

n = nb("dist/saas_dashboard.md", title="SaaS Metrics Dashboard — January 2026")

n.section("Hero Metrics")
n.metric_row([
    {"label": "MRR", "value": "$350K", "delta": "+$28K"},
    {"label": "ARR", "value": "$4.2M", "delta": "+18%"},
    {"label": "Customers", "value": "1,234", "delta": "+89"},
    {"label": "Churn", "value": "1.8%", "delta": "-0.3%", "delta_color": "inverse"},
])
n.badge("ALL GREEN", style="success")

n.section("Unit Economics")
n.kv({
    "LTV": "$14,400",
    "CAC": "$2,100",
    "LTV/CAC": "6.9x",
    "Payback Period": "5.2 months",
    "Gross Margin": "82%",
}, title="Unit Economics")

n.section("Growth")
n.change("MRR", current=350_000, previous=322_000, fmt=",.0f", pct=True)
n.change("Customers", current=1234, previous=1145, fmt=",d", pct=True)
n.change("ARPU", current=284, previous=281, fmt=",.0f", pct=True)

n.section("Segment Performance")
n.ranking("Enterprise", value="$180K MRR", rank=1, total=3)
n.ranking("SMB", value="$120K MRR", rank=2, total=3)
n.ranking("Self-Serve", value="$50K MRR", rank=3, total=3)

n.section("Alerts")
n.success("MRR target of $340K exceeded")
n.warning("Enterprise churn increased 0.2pp — monitor closely")
n.info("New pricing tier launching Feb 15")

n.save()
```

## Example 2: Portfolio Dashboard

```python
from notebookmd import nb
import pandas as pd

n = nb("dist/portfolio.md", title="Investment Portfolio Dashboard")

n.section("Portfolio Summary")
n.metric_row([
    {"label": "Total Value", "value": "$2.4M", "delta": "+$180K"},
    {"label": "Day P&L", "value": "+$12,340", "delta": "+0.52%"},
    {"label": "YTD Return", "value": "+14.2%", "delta": "+14.2%"},
    {"label": "Sharpe", "value": "1.84"},
])

n.section("Asset Allocation")
n.kv({
    "Equities": "62% ($1.49M)",
    "Fixed Income": "25% ($600K)",
    "Alternatives": "8% ($192K)",
    "Cash": "5% ($120K)",
}, title="Allocation")

n.section("Top Holdings")
n.ranking("AAPL", value="$340K", rank=1, total=25, percentile=96)
n.ranking("MSFT", value="$280K", rank=2, total=25, percentile=92)
n.ranking("GOOGL", value="$210K", rank=3, total=25, percentile=88)

n.section("Risk Metrics")
n.stats([
    {"label": "VaR (95%)", "value": -45_000, "fmt": ",.0f"},
    {"label": "Max Drawdown", "value": -0.082, "fmt": ".1%"},
    {"label": "Beta", "value": 0.95, "fmt": ".2f"},
])

n.save()
```
