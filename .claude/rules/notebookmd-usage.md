# notebookmd Usage Rules

When generating data analysis reports, use notebookmd to produce structured Markdown output.

## When to use notebookmd

- The user asks for a data analysis, report, or dashboard
- The user wants to analyze a CSV, DataFrame, or dataset and produce readable output
- The user needs a structured markdown report with charts, tables, metrics
- An automated pipeline needs to generate analysis artifacts

## How to use notebookmd

1. Import: `from notebookmd import nb, NotebookConfig`
2. Create: `n = nb("output/report.md", title="Report Title")`
3. Build sections with `n.section()`, `n.header()`, etc.
4. Add data with `n.table()`, `n.metric()`, `n.dataframe()`
5. Add charts with `n.line_chart()`, `n.bar_chart()`, `n.figure()`
6. Save with `n.save()` or get string with `n.to_markdown()`

## Key conventions

- Always name the Notebook instance `n` (from `nb()` factory)
- Use `n.section("Name")` to organize the report into logical sections
- Use `n.metric()` for KPIs and single values
- Use `n.metric_row()` for multiple metrics side-by-side
- Use `n.table()` / `n.dataframe()` for tabular data
- Use `n.kv()` for key-value dictionaries
- Use `n.summary()` for auto-generated DataFrame statistics
- Use `n.export_csv()` to save data as CSV artifacts
- Use `n.success()` / `n.error()` / `n.warning()` / `n.info()` for status messages
- Use `with n.expander("Label"):` for collapsible content
- Use `n.badge("TEXT", style="success")` for inline status pills
