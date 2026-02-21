---
name: report
description: Generate a structured Markdown report using notebookmd. Use when the user asks for a report, documentation, summary, or writeup that should be saved as a formatted Markdown file with sections, tables, metrics, and artifacts.
argument-hint: "[topic or description]"
allowed-tools: ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]
---

# Markdown Report Generator

Generate a structured, professional Markdown report using the `notebookmd` library.

## Input

Report topic: $ARGUMENTS

## Instructions

### 1. Setup

```python
from notebookmd import nb, NotebookConfig

st = nb("dist/report.md", title="<descriptive title>")
```

### 2. Report Structure

Adapt the structure to the topic. Common patterns:

**Executive Summary Pattern:**
```python
st.section("Executive Summary")
st.metric_row([...])  # Top-line KPIs
st.write("Brief overview...")

st.section("Background")
st.write("Context and motivation...")

st.section("Methodology")
with st.expander("Details"):
    st.write("Step-by-step approach...")

st.section("Results")
st.table(results_df, name="Key Results")
st.kv(metrics_dict, title="Performance Metrics")

st.section("Conclusion")
st.success("Summary of outcomes")
```

**Technical Report Pattern:**
```python
st.section("Overview")
st.kv(config_dict, title="Configuration")

st.section("Implementation")
st.code(code_snippet, lang="python")
st.note("Key technical detail...")

st.section("Results")
st.table(benchmarks_df, name="Benchmarks")

st.section("Next Steps")
st.write("1. Item one\n2. Item two")
```

**Status Report Pattern:**
```python
st.section("Status Overview")
st.metric_row([
    {"label": "Complete", "value": "73%", "delta": "+5%"},
    {"label": "On Track", "value": "12/15"},
    {"label": "Blocked", "value": "2"},
])

st.section("Completed This Period")
st.write("- Task 1\n- Task 2")

st.section("In Progress")
st.progress(0.73, "Overall completion")
st.write("Current work items...")

st.section("Risks & Blockers")
st.warning("Risk description...")
st.error("Blocker description...")
```

### 3. Available Widgets

**Text:** `st.title()`, `st.header()`, `st.subheader()`, `st.write()`, `st.md()`, `st.caption()`, `st.code()`, `st.latex()`, `st.text()`

**Data:** `st.metric()`, `st.metric_row()`, `st.table()`, `st.dataframe()`, `st.kv()`, `st.json()`, `st.summary()`

**Status:** `st.success()`, `st.error()`, `st.warning()`, `st.info()`, `st.progress()`, `st.badge()`

**Layout:** `st.section()`, `st.expander()`, `st.tabs()`, `st.divider()`

**Analytics:** `st.stat()`, `st.stats()`, `st.change()`, `st.ranking()`

**Charts:** `st.line_chart()`, `st.bar_chart()`, `st.area_chart()`, `st.figure()`

**Export:** `st.save()`, `st.to_markdown()`, `st.export_csv()`

### 4. Save and Output

```python
out = st.save()
print(f"Report saved to: {out}")
```
