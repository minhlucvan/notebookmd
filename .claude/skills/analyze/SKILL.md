---
name: analyze
description: Generate a structured data analysis report using notebookmd. Use when the user asks to analyze data, a CSV file, a DataFrame, financial data, or any dataset and wants a readable Markdown report with tables, charts, metrics, and insights.
argument-hint: "[data-source or description]"
allowed-tools: ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]
---

# Data Analysis Report Generator

Generate a comprehensive, structured data analysis report using the `notebookmd` library.
The report should read like a professional analyst's notebook — with clear sections,
key metrics, data tables, visualizations, and actionable insights.

## Input

Analyze: $ARGUMENTS

## Instructions

### 1. Setup

```python
from notebookmd import nb, NotebookConfig
import pandas as pd

cfg = NotebookConfig(max_table_rows=30)
n = nb("dist/analysis.md", title="<descriptive title based on the data>", cfg=cfg)
```

### 2. Report Structure

Build the report with these sections (adapt to the data):

```python
# Section 1: Data Overview
n.section("Data Overview")
n.kv({
    "Source": "<where the data came from>",
    "Records": f"{len(df):,}",
    "Columns": str(len(df.columns)),
    "Date Range": f"{df['date'].min()} to {df['date'].max()}",  # if applicable
}, title="Dataset Info")
n.summary(df, title="Statistical Summary")

# Section 2: Key Metrics
n.section("Key Metrics")
n.metric_row([
    {"label": "Total", "value": f"{total:,.0f}"},
    {"label": "Mean", "value": f"{mean:.2f}"},
    {"label": "Trend", "value": f"{trend:+.1f}%", "delta": f"{trend:+.1f}%"},
])

# Section 3: Data Sample
n.section("Data Preview")
n.dataframe(df.head(15), name="First 15 rows")

# Section 4: Analysis & Patterns
n.section("Analysis")
# Group by, aggregate, compute derived metrics
n.table(grouped_df, name="Aggregated Results")

# Section 5: Visualization (if matplotlib available)
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n.section("Visualizations")
    n.line_chart(df, x="date_col", y="value_col", title="Trend Over Time")
    n.bar_chart(top_n, x="category", y="count", title="Top Categories")
except ImportError:
    n.note("Install matplotlib for chart generation: pip install notebookmd[plotting]")

# Section 6: Export
n.section("Export")
n.export_csv(df, "analysis_data.csv", name="Full dataset")

# Section 7: Findings & Recommendations
n.section("Key Findings")
n.write("""
- **Finding 1**: Description with supporting evidence
- **Finding 2**: Description with supporting evidence
- **Finding 3**: Description with supporting evidence
""")

n.section("Recommendations")
n.write("""
1. Action item based on findings
2. Action item based on findings
3. Action item based on findings
""")

n.success("Analysis complete!")
out = n.save()
print(f"Report saved to: {out}")
```

### 3. Guidelines

- Always check if pandas is available before table/DataFrame operations
- Always check if matplotlib is available before chart operations
- Use `n.metric()` and `n.metric_row()` for KPIs — never raw text
- Use `n.table()` for DataFrames, not `print(df.to_string())`
- Use `n.summary()` for auto-generated statistics
- Use `n.kv()` for metadata and configuration details
- Use `n.badge()` for categorical labels (e.g., `n.badge("BULLISH", style="success")`)
- Use `n.change()` for period-over-period comparisons
- Always save a CSV export of the key data
- End with a findings/recommendations section
- Write the report as if a human analyst will read it

### 4. Output

Save the report and print the path. The report should be a self-contained Markdown file
with all charts saved as PNG assets in the `assets/` subdirectory.
