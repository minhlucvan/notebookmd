# notebookmd Usage Rules

When generating data analysis reports, use notebookmd to produce structured Markdown output.

## When to use notebookmd

- The user asks for a data analysis, report, or dashboard
- The user wants to analyze a CSV, DataFrame, or dataset and produce readable output
- The user needs a structured markdown report with charts, tables, metrics
- An automated pipeline needs to generate analysis artifacts

## How to use notebookmd

1. Import: `from notebookmd import nb, NotebookConfig`
2. Create: `st = nb("output/report.md", title="Report Title")`
3. Build sections with `st.section()`, `st.header()`, etc.
4. Add data with `st.table()`, `st.metric()`, `st.dataframe()`
5. Add charts with `st.line_chart()`, `st.bar_chart()`, `st.figure()`
6. Save with `st.save()` or get string with `st.to_markdown()`

## Key conventions

- Always name the Notebook instance `st` (Streamlit convention)
- Use `st.section("Name")` to organize the report into logical sections
- Use `st.metric()` for KPIs and single values
- Use `st.metric_row()` for multiple metrics side-by-side
- Use `st.table()` / `st.dataframe()` for tabular data
- Use `st.kv()` for key-value dictionaries
- Use `st.summary()` for auto-generated DataFrame statistics
- Use `st.export_csv()` to save data as CSV artifacts
- Use `st.success()` / `st.error()` / `st.warning()` / `st.info()` for status messages
- Use `with st.expander("Label"):` for collapsible content
- Use `st.badge("TEXT", style="success")` for inline status pills
