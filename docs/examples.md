# Examples

End-to-end examples showing how to build different types of reports with notebookmd.

## Sales Report

A business report with KPIs, trends, and data tables.

```python
import pandas as pd
from notebookmd import nb, NotebookConfig

# Load data
df = pd.read_csv("data/monthly_sales.csv")

# Create notebook
cfg = NotebookConfig(max_table_rows=50)
n = nb("output/sales_report.md", title="Monthly Sales Report", cfg=cfg)

# Executive summary
n.section("Executive Summary")
n.metric_row([
    {"label": "Total Revenue", "value": f"${df['revenue'].sum():,.0f}", "delta": "+12%"},
    {"label": "Total Orders", "value": f"{df['orders'].sum():,}", "delta": "+8%"},
    {"label": "Avg Order Value", "value": f"${df['revenue'].sum() / df['orders'].sum():,.2f}"},
])

n.success("Revenue target exceeded by 12%")

# Trend analysis
n.section("Revenue Trend")
n.line_chart(df, x="month", y="revenue", title="Monthly Revenue")

# Regional breakdown
n.section("Regional Breakdown")
regional = df.groupby("region")["revenue"].sum().reset_index()
n.bar_chart(regional, x="region", y="revenue", title="Revenue by Region")
n.table(regional, name="Revenue by Region")

# Detailed data
n.section("Detailed Data")
with n.expander("Show all monthly data"):
    n.table(df, name="Full Dataset")

# Export
n.export_csv(df, "monthly_sales.csv", name="Monthly Sales Data")
n.save()
```

## Data Quality Report

An automated data validation report.

```python
import pandas as pd
from notebookmd import nb

df = pd.read_csv("data/raw_data.csv")
n = nb("output/data_quality.md", title="Data Quality Report")

# Overview
n.section("Dataset Overview")
n.summary(df, title="Dataset Summary")

# Completeness
n.section("Completeness")
total_cells = df.shape[0] * df.shape[1]
null_cells = df.isnull().sum().sum()
completeness = (total_cells - null_cells) / total_cells

n.metric("Completeness", f"{completeness:.1%}", delta=f"{completeness - 0.95:.1%}")

null_cols = df.isnull().sum()
null_cols = null_cols[null_cols > 0].sort_values(ascending=False)
if len(null_cols) > 0:
    n.warning(f"{len(null_cols)} columns have missing values")
    n.kv(
        {col: f"{count} ({count/len(df):.1%})" for col, count in null_cols.items()},
        title="Null Counts",
    )
else:
    n.success("No missing values found")

# Duplicates
n.section("Duplicates")
dup_count = df.duplicated().sum()
if dup_count > 0:
    n.error(f"Found {dup_count} duplicate rows ({dup_count/len(df):.1%})")
else:
    n.success("No duplicate rows")

# Numeric stats
n.section("Numeric Column Statistics")
numeric_cols = df.select_dtypes(include="number").columns
for col in numeric_cols[:5]:
    n.stat(f"{col} mean", df[col].mean(), fmt=".2f")
    n.stat(f"{col} std", df[col].std(), fmt=".2f")
    n.divider()

n.save()
```

## Model Evaluation Report

A machine learning model evaluation report.

```python
import pandas as pd
from notebookmd import nb

n = nb("output/model_eval.md", title="Model Evaluation Report")

# Model info
n.section("Model Configuration")
n.kv({
    "Algorithm": "XGBoost",
    "Training Samples": "50,000",
    "Features": "42",
    "Cross-Validation": "5-fold",
    "Random State": "42",
}, title="Model Parameters")

# Performance metrics
n.section("Performance Metrics")
n.metric_row([
    {"label": "Accuracy", "value": "94.2%", "delta": "+1.3%"},
    {"label": "Precision", "value": "92.8%", "delta": "+0.9%"},
    {"label": "Recall", "value": "91.5%", "delta": "+2.1%"},
    {"label": "F1 Score", "value": "92.1%", "delta": "+1.5%"},
])

n.badge("PRODUCTION READY", style="success")

# Comparison
n.section("Model Comparison")
n.change("Accuracy", 0.942, 0.929, fmt=".1%")
n.change("Training Loss", 0.15, 0.22, fmt=".3f", invert=True)
n.change("Inference Time", 12.5, 18.3, fmt=".1f", invert=True)

# Feature importance
n.section("Feature Importance")
importance_df = pd.DataFrame({
    "Feature": ["age", "income", "tenure", "usage", "complaints"],
    "Importance": [0.25, 0.22, 0.18, 0.15, 0.12],
})
n.bar_chart(importance_df, x="Feature", y="Importance", title="Top 5 Features")
n.table(importance_df, name="Feature Importance Scores")

# Results by segment
n.section("Results by Segment")
tabs = n.tabs(["High Value", "Medium Value", "Low Value"])

with tabs.tab("High Value"):
    n.metric("Accuracy", "96.1%")
    n.metric("Sample Size", "5,200")

with tabs.tab("Medium Value"):
    n.metric("Accuracy", "93.8%")
    n.metric("Sample Size", "28,000")

with tabs.tab("Low Value"):
    n.metric("Accuracy", "91.2%")
    n.metric("Sample Size", "16,800")

n.save()
```

## Financial Dashboard

An analytics-focused report using the analytics widgets.

```python
from notebookmd import nb

n = nb("output/financial.md", title="Financial Dashboard")

# Market overview
n.section("Market Overview")
n.stats([
    {"label": "S&P 500", "value": 5021.84, "fmt": ",.2f"},
    {"label": "Nasdaq", "value": 15990.66, "fmt": ",.2f"},
    {"label": "VIX", "value": 14.2, "fmt": ".1f"},
])

# Stock analysis
n.section("AAPL Analysis")
n.badge("BUY", style="success")

n.metric_row([
    {"label": "Price", "value": "$185.42", "delta": "+2.3%"},
    {"label": "Volume", "value": "52.3M"},
    {"label": "Market Cap", "value": "$2.87T"},
])

n.stats([
    {"label": "P/E", "value": 30.2, "fmt": ".1f"},
    {"label": "P/B", "value": 47.8, "fmt": ".1f"},
    {"label": "Dividend Yield", "value": 0.0054, "fmt": ".2%"},
])

n.change("Revenue (TTM)", 383_285_000, 365_817_000, fmt=",.0f")
n.change("Net Income", 96_995_000, 94_680_000, fmt=",.0f")

n.ranking("Market Cap", "$2.87T", rank=1, total=500)
n.ranking("Revenue Growth", 0.048, percentile=72, fmt=".1%")

# Risk assessment
n.section("Risk Assessment")
n.connection_status("Market Data Feed", status="connected", details="real-time")
n.connection_status("Historical DB", status="connected", details="5yr daily")

with n.expander("Risk Factors"):
    n.warning("Concentration risk: >50% revenue from iPhone")
    n.info("Regulatory: EU DMA compliance ongoing")
    n.info("Geopolitical: China supply chain exposure")

n.save()
```

## Report with Custom Plugin

Building a report with a domain-specific plugin.

```python
from notebookmd import nb
from notebookmd.plugins import PluginSpec

# Define a custom plugin
class WeatherPlugin(PluginSpec):
    name = "weather"

    def forecast(self, city: str, conditions: list[dict]) -> None:
        """Display a weather forecast table."""
        self._w(f"### {city} Forecast\n\n")
        self._w("| Day | Temp | Conditions | Precip |\n")
        self._w("|-----|------|------------|--------|\n")
        for day in conditions:
            self._w(f"| {day['day']} | {day['temp']} | {day['conditions']} | {day['precip']} |\n")
        self._w("\n")

    def alert(self, severity: str, message: str) -> None:
        """Display a weather alert."""
        icons = {"watch": "🟡", "warning": "🟠", "emergency": "🔴"}
        icon = icons.get(severity, "⚪")
        self._w(f"> {icon} **Weather {severity.title()}:** {message}\n\n")


# Use it
n = nb("output/weather.md", title="Weather Report")
n.use(WeatherPlugin)

n.section("Bay Area")
n.forecast("San Francisco", [
    {"day": "Mon", "temp": "62°F", "conditions": "Partly Cloudy", "precip": "10%"},
    {"day": "Tue", "temp": "58°F", "conditions": "Fog", "precip": "20%"},
    {"day": "Wed", "temp": "65°F", "conditions": "Sunny", "precip": "0%"},
])

n.alert("watch", "Dense fog advisory in effect until 10 AM Tuesday")

n.section("Summary")
n.info("Next update in 6 hours")

n.save()
```

## Report to String (No File)

Generate Markdown in memory without writing to disk.

```python
from notebookmd import nb

n = nb("/dev/null", title="In-Memory Report")

n.section("Results")
n.metric("Score", "42")
n.success("All checks passed")

# Get as string instead of saving
md = n.to_markdown()
print(md)

# Or send to an API, embed in an email, etc.
# send_email(subject="Report", body=md)
```

## Report with matplotlib Figures

Full control over chart rendering using matplotlib directly.

```python
import matplotlib.pyplot as plt
import pandas as pd
from notebookmd import nb

df = pd.read_csv("data/timeseries.csv")
n = nb("output/charts.md", title="Custom Charts Report")

# Simple auto-generated chart
n.section("Auto Charts")
n.line_chart(df, x="date", y="value", title="Auto Line Chart")
n.bar_chart(df, x="category", y="count", title="Auto Bar Chart")

# Custom matplotlib figure
n.section("Custom Figures")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].scatter(df["x"], df["y"], alpha=0.5, c=df["category_id"], cmap="viridis")
axes[0].set_title("Scatter Plot")
axes[0].set_xlabel("X")
axes[0].set_ylabel("Y")

axes[1].hist(df["value"], bins=30, edgecolor="black")
axes[1].set_title("Distribution")
axes[1].set_xlabel("Value")
axes[1].set_ylabel("Frequency")

fig.tight_layout()
n.figure(fig, "custom_analysis.png", caption="Scatter plot and distribution")
plt.close(fig)

# Subplot grid
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
for i, col in enumerate(["revenue", "profit", "users", "churn"]):
    ax = axes[i // 2][i % 2]
    ax.plot(df["month"], df[col])
    ax.set_title(col.title())
    ax.grid(True, alpha=0.3)

fig.suptitle("Key Metrics Over Time", fontsize=14)
fig.tight_layout()
n.figure(fig, "metrics_grid.png", caption="Four key metrics", dpi=200)
plt.close(fig)

n.save()
```

## Multi-Section Report with Layout

Using tabs, columns, and expanders for complex layouts.

```python
import pandas as pd
from notebookmd import nb

n = nb("output/layout_demo.md", title="Layout Demo")

# Header metrics in columns
n.section("Dashboard")
cols = n.columns(4)
with cols.col(0):
    n.metric("Users", "10.2K", delta="+5%")
with cols.col(1):
    n.metric("Revenue", "$1.2M", delta="+12%")
with cols.col(2):
    n.metric("NPS", "72", delta="+4")
with cols.col(3):
    n.metric("Churn", "2.1%", delta="-0.3%", delta_color="inverse")

# Tabbed analysis
n.section("Analysis")
tabs = n.tabs(["By Region", "By Product", "By Channel"])

with tabs.tab("By Region"):
    n.bar_chart(region_df, x="region", y="revenue")
    n.table(region_df, name="Regional Revenue")

with tabs.tab("By Product"):
    n.bar_chart(product_df, x="product", y="units_sold")
    n.table(product_df, name="Product Sales")

with tabs.tab("By Channel"):
    n.kv({
        "Online": "$650K (54%)",
        "Retail": "$380K (32%)",
        "Wholesale": "$170K (14%)",
    }, title="Channel Revenue")

# Collapsible details
n.section("Appendix")
with n.expander("Methodology"):
    n.md("""
    Data was collected from the internal analytics platform.
    Revenue figures include all product lines.
    Growth percentages are year-over-year.
    """)

with n.expander("Data Sources"):
    n.connection_status("Analytics DB", status="connected")
    n.connection_status("CRM API", status="connected")
    n.connection_status("Legacy System", status="disconnected", details="deprecated Q3")

with n.expander("Raw Data", expanded=False):
    n.table(full_df, name="Complete Dataset", max_rows=100)

n.save()
```

## Capturing Code Execution

Using `capture_streams` to capture and display code output.

```python
from notebookmd import nb
from notebookmd.capture import capture_streams

n = nb("output/execution.md", title="Code Execution Report")

n.section("Data Processing")

# Show code and its output
code = "df.describe()"
with capture_streams() as out:
    print(df.describe())

n.echo(code, out.stdout)

# Capture errors gracefully
n.section("Error Handling")
with capture_streams(echo=False) as out:
    try:
        result = process_data(invalid_input)
    except Exception:
        pass

if out.has_error:
    n.exception(out.exception)
    n.error("Processing failed -- see exception above")
else:
    n.success("Processing completed")

n.save()
```
