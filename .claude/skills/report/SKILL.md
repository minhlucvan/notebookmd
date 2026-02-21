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

n = nb("dist/report.md", title="<descriptive title>")
```

### 2. Report Structure

Adapt the structure to the topic. Common patterns:

**Executive Summary Pattern:**
```python
n.section("Executive Summary")
n.metric_row([...])  # Top-line KPIs
n.write("Brief overview...")

n.section("Background")
n.write("Context and motivation...")

n.section("Methodology")
with n.expander("Details"):
    n.write("Step-by-step approach...")

n.section("Results")
n.table(results_df, name="Key Results")
n.kv(metrics_dict, title="Performance Metrics")

n.section("Conclusion")
n.success("Summary of outcomes")
```

**Technical Report Pattern:**
```python
n.section("Overview")
n.kv(config_dict, title="Configuration")

n.section("Implementation")
n.code(code_snippet, lang="python")
n.note("Key technical detail...")

n.section("Results")
n.table(benchmarks_df, name="Benchmarks")

n.section("Next Steps")
n.write("1. Item one\n2. Item two")
```

**Status Report Pattern:**
```python
n.section("Status Overview")
n.metric_row([
    {"label": "Complete", "value": "73%", "delta": "+5%"},
    {"label": "On Track", "value": "12/15"},
    {"label": "Blocked", "value": "2"},
])

n.section("Completed This Period")
n.write("- Task 1\n- Task 2")

n.section("In Progress")
n.progress(0.73, "Overall completion")
n.write("Current work items...")

n.section("Risks & Blockers")
n.warning("Risk description...")
n.error("Blocker description...")
```

### 3. Available Widgets

**Text:** `n.title()`, `n.header()`, `n.subheader()`, `n.write()`, `n.md()`, `n.caption()`, `n.code()`, `n.latex()`, `n.text()`

**Data:** `n.metric()`, `n.metric_row()`, `n.table()`, `n.dataframe()`, `n.kv()`, `n.json()`, `n.summary()`

**Status:** `n.success()`, `n.error()`, `n.warning()`, `n.info()`, `n.progress()`, `n.badge()`

**Layout:** `n.section()`, `n.expander()`, `n.tabs()`, `n.divider()`

**Analytics:** `n.stat()`, `n.stats()`, `n.change()`, `n.ranking()`

**Charts:** `n.line_chart()`, `n.bar_chart()`, `n.area_chart()`, `n.figure()`

**Export:** `n.save()`, `n.to_markdown()`, `n.export_csv()`

### 4. Save and Output

```python
out = n.save()
print(f"Report saved to: {out}")
```
