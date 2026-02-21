"""Generate the community launch plan report for notebookmd."""

import pandas as pd
from notebookmd import nb, NotebookConfig

n = nb("docs/community-launch-plan.md", title="notebookmd — Community Launch Plan")

# ─────────────────────────────────────────────────────────────
# Executive Summary
# ─────────────────────────────────────────────────────────────
n.section("Executive Summary")

n.write(
    "This document outlines the community launch strategy for **notebookmd** — "
    "a Python library that gives AI agents a Streamlit-like API for generating "
    "structured Markdown reports. The goal is to reach early adopters across "
    "Reddit, X/Twitter, Product Hunt, Hacker News, and developer communities, "
    "converting awareness into GitHub stars, PyPI installs, and community contributors."
)

n.metric_row([
    {"label": "Target Platforms", "value": "5"},
    {"label": "Content Pieces", "value": "12+"},
    {"label": "Launch Window", "value": "2 weeks"},
    {"label": "Goal: GitHub Stars", "value": "500+"},
])

# ─────────────────────────────────────────────────────────────
# Community Pain Points
# ─────────────────────────────────────────────────────────────
n.section("Community Pain Points — Why This Matters")

n.write(
    "The launch messaging should directly address pain points that developers "
    "and data scientists already feel. These are drawn from recurring themes across "
    "Reddit, Hacker News, and developer forums."
)

n.subheader("1. Jupyter Notebooks Are Not Production-Ready")
n.write(
    "Developers consistently complain about taking Jupyter notebooks to production. "
    "**87% of data science projects never make it to production** (VentureBeat). "
    "Common frustrations include:\n\n"
    '- *"Jupyter notebooks were fun to use for a bit, then I hit the inevitable wall of '
    "'ok, now let's turn this into a real, properly built script, but now everything is "
    "breaking for inexplicable reasons.'\"* — [Hacker News](https://news.ycombinator.com/item?id=17856700)\n"
    "- Hidden state and out-of-order cell execution cause unreproducible results\n"
    "- `.ipynb` files are JSON blobs that create merge conflicts in git — *\"try diffing a big JSON mess that mixes input and output\"*\n"
    "- No good way to run notebooks in CI/CD pipelines without heavy tooling (papermill, nbconvert)\n"
    "- Exporting to Markdown/HTML loses interactivity and often breaks formatting\n"
    '- *"There are many problems with producing a Jupyter notebook as a report. Nobody else wants to read it. '
    "Technical people don't want to spin up a Jupyter server to run it, and non-technical people can't even render it.\"*"
)

n.subheader("2. Streamlit Requires a Running Server")
n.write(
    "Streamlit is loved for interactive dashboards but has fundamental limitations for batch/agent workflows. "
    "A [detailed critique on tildehacker.com](https://tildehacker.com/streamlit-is-a-mess) titled "
    "\"Streamlit Is a Mess\" observes:\n\n"
    '- *"The most critical issue with Streamlit isn\'t what it includes, but what it omits: a clean, enforced architecture."*\n'
    "- The entire Python file re-runs on every user interaction — causing performance issues at scale\n"
    "- Can't be used in CI/CD, cron jobs, or agent pipelines — requires a running web server\n"
    "- Overkill for static reports — a Markdown file is just a file; Streamlit needs a running process\n"
    "- No artifact output — results exist only while the server runs\n"
    '- *"No fully supported enterprise deployment solution"* — lacks auth, scaling, and lifecycle management (Plotly blog)'
)

n.subheader("3. AI Agents Lack Structured Output Tools")
n.write(
    "As AI agents become mainstream for data analysis, a gap has emerged. The "
    "[LangChain State of Agent Engineering 2025](https://www.langchain.com/state-of-agent-engineering) "
    "report (1,340 respondents) found **32% cited output quality as their primary blocker** "
    "for production agents:\n\n"
    "- Agents default to `print()` statements and unformatted text dumps\n"
    "- **Formatting problems are 2.66x more common** in AI-generated output vs human code "
    "([CodeRabbit AI vs Human Report](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report))\n"
    "- **Missing context is reported by 65% of developers** as the primary cause of poor AI output quality "
    "([Qodo State of AI Code Quality](https://www.qodo.ai/reports/state-of-ai-code-quality/))\n"
    "- No standard way for agents to produce charts, metrics, and tables together\n"
    "- Agent frameworks (LangChain, CrewAI, Claude) focus on reasoning, not presentation\n"
    "- Cloudflare recognized this gap: *\"A simple `## About Us` in Markdown costs ~3 tokens; "
    "its HTML equivalent burns 12-15\"* — Markdown is becoming the AI lingua franca"
)

n.subheader("4. The 'Last Mile' of Data Analysis")
n.write(
    "Data scientists spend significant time formatting results after analysis is done:\n\n"
    "- Manually formatting Markdown tables is tedious and error-prone\n"
    "- Saving charts, linking them in reports, managing file paths — all manual\n"
    "- No single tool combines metrics + tables + charts + text in one API\n"
    '- *"80% of my time is analysis, 20% is making the output look presentable"*'
)

n.subheader("5. The Ecosystem Gap")
n.write(
    "The existing Python reporting tools fall into three categories, "
    "none of which fully address simple, programmatic report generation:"
)
n.table(
    pd.DataFrame(
        [
            ["Interactive apps", "Streamlit, Dash, Panel", "Require running servers; overkill for static reports"],
            ["Notebook-based", "Jupyter + nbconvert, Quarto", "Version control issues, export bugs, production gap"],
            ["Low-level markdown", "mdutils, SnakeMD", "Just text formatting; no data tables, charts, or metrics"],
            ["Abandoned", "Datapane (shut down)", "Was the closest to a data reporting tool; no longer maintained"],
        ],
        columns=["Category", "Tools", "Problem"],
    ),
    name="Current Ecosystem Gaps",
)
n.write(
    "**The gap notebookmd fills:** Streamlit-like API + static Markdown output + "
    "data-native widgets + zero-dependency core + AI agent friendly."
)

# ─────────────────────────────────────────────────────────────
# Positioning & Messaging
# ─────────────────────────────────────────────────────────────
n.section("Positioning & Core Messaging")

n.subheader("One-Line Pitch")
n.write("**The notebook for AI agents.** Write Python, get Markdown reports.")

n.subheader("Elevator Pitch (30 seconds)")
n.write(
    "notebookmd is a Python library with a Streamlit-like API that outputs clean Markdown "
    "instead of a web app. Call `n.metric()`, `n.table()`, `n.line_chart()` — get a structured "
    "report with embedded charts, metrics, and data tables. Zero dependencies. Built for AI agents, "
    "CI/CD pipelines, and anyone who wants reports without running a server."
)

n.subheader("Key Differentiators")
n.table(
    pd.DataFrame(
        [
            ["No kernel/server needed", "Yes", "No", "No", "Yes"],
            ["40+ rich widgets", "Yes", "Unlimited", "Unlimited", "No"],
            ["Structured Markdown output", "Yes", "No (.ipynb JSON)", "No (HTML)", "No"],
            ["Zero dependencies", "Yes", "No", "No", "Yes"],
            ["Git-friendly output", "Yes", "No", "N/A", "Yes"],
            ["Agent-friendly (sequential)", "Yes", "No (cells)", "No (reactive)", "Yes"],
            ["Built-in asset management", "Yes", "No", "No", "No"],
            ["CI/CD compatible", "Yes", "Painful", "No", "Yes"],
        ],
        columns=["Feature", "notebookmd", "Jupyter", "Streamlit", "print()"],
    ),
    name="Competitive Comparison",
)

n.subheader("Target Audiences (in priority order)")
n.write(
    "1. **AI/LLM agent builders** — using Claude, GPT, LangChain, CrewAI for data analysis\n"
    "2. **Data scientists** — frustrated with Jupyter-to-production workflows\n"
    "3. **DevOps/MLOps engineers** — need report generation in CI/CD pipelines\n"
    "4. **Python developers** — want a simple way to generate structured Markdown\n"
    "5. **Open-source enthusiasts** — looking for clean, well-architected Python packages"
)

# ─────────────────────────────────────────────────────────────
# Platform-Specific Content
# ─────────────────────────────────────────────────────────────
n.section("Platform-Specific Launch Content")

# --- Reddit ---
n.subheader("Reddit")

n.write("**Target subreddits:** r/Python, r/datascience, r/MachineLearning, r/LocalLLaMA, r/ChatGPTCoding")

n.info(
    "Reddit rewards authenticity and technical substance. Posts that lead with a problem "
    "and show real output perform best. Avoid marketing language."
)

n.write("**Post 1: r/Python (Primary Launch — viral hook)**")
n.info(
    "This post uses the \"AI agents can't use Jupyter, so I built them their own notebook\" angle. "
    "This framing works because it: (1) taps into the AI/agent hype, (2) acknowledges a universally "
    "known tool (Jupyter), (3) presents a clear problem→solution narrative, and (4) creates curiosity — "
    "\"what does a notebook for AI agents even look like?\""
)
n.code(
    """Title: AI agents can't use Jupyter notebooks, so I built them their own — notebookmd

Body:

Hey r/Python,

Here's something that's been bugging me: we have amazing AI agents that can
analyze data, write SQL, build dashboards — but when it comes to presenting
results? They're stuck with print() and unformatted text dumps.

Why? Because the tools we have don't work for agents:

- **Jupyter** needs a running kernel, interactive cells, and a browser.
  Agents don't have any of that.
- **Streamlit** needs a live web server. Agents don't serve web apps.
- **Plain Markdown** means every agent reinvents table formatting and chart
  embedding from scratch. And the output is never consistent.

So I built notebookmd — a Jupyter-style notebook that runs as plain Python
function calls and outputs clean Markdown.

```python
from notebookmd import nb

n = nb("report.md", title="Q4 Revenue Analysis")
n.metric("Revenue", "$4.2M", delta="+18%")
n.table(df, name="Top Performers")
n.line_chart(df, x="month", y="revenue", title="Trend")
n.success("Analysis complete!")
n.save()
```

The output is a self-contained Markdown file with tables, charts (as PNGs),
metrics with delta arrows, collapsible sections, and an artifact index.
Readable by humans, parseable by other LLMs, committable to git.

What makes it work for agents:
- **Sequential API** — agents call functions one at a time, exactly how they
  think. No cells, no execution context, no state management.
- **Zero dependencies** — the core is pure Python. pandas/matplotlib are
  optional extras that degrade gracefully if missing.
- **40+ widgets** — metrics, tables, charts, badges, progress bars, tabs,
  expanders, LaTeX, code blocks, JSON display...
- **Built-in asset management** — charts auto-saved as PNGs, CSVs exported,
  everything auto-linked with relative paths.
- **Plugin architecture** — 8 built-in plugins, extend with your own.

It's not just for agents though — works great for automated reports, CI/CD
pipelines, cron jobs, or anywhere you want structured output from Python
without spinning up a server.

[Screenshot: code on left, rendered Markdown report on right]

GitHub: [link]
PyPI: pip install notebookmd

I've been using it with Claude for automated data analysis and it's been a
game changer. Happy to answer any questions about the design!""",
    lang="markdown",
)

n.write("**Post 2: r/datascience**")
n.code(
    """Title: Jupyter can't run without a human. So I built a notebook that can — for
automated reports and AI agents.

Body:

As a data scientist, I love Jupyter for exploration. But every time I need to
automate a report, I hit the same wall:

1. Jupyter needs a kernel and a browser — can't run it in a cron job
2. nbconvert output is ugly and breaks half the time
3. Streamlit needs a running server — overkill for a weekly PDF

I wanted something simpler: call Python functions, get a Markdown report.

So I built notebookmd. It's like writing a Jupyter notebook, but every cell
is a function call, and the output is a clean .md file:

```python
n = nb("weekly_report.md", title="Weekly Sales Report")
n.metric_row([
    {"label": "Revenue", "value": "$1.2M", "delta": "+8%"},
    {"label": "Orders", "value": "3,450", "delta": "+12%"},
    {"label": "AOV", "value": "$348", "delta": "-2%"},
])
n.table(top_products_df, name="Top Products")
n.line_chart(daily_df, x="date", y="revenue", title="Daily Revenue")
n.summary(sales_df, title="Statistical Summary")
n.save()
```

The output includes formatted tables, metrics with delta arrows (▲/▼),
charts saved as PNGs, and a full artifact index. Zero dependencies by
default — add pandas/matplotlib only if you need them.

I've been running this in a daily cron job for automated analysis reports
and it's been incredibly reliable. Also works great as the output layer
for AI agent data analysis.

GitHub: [link] | PyPI: pip install notebookmd""",
    lang="markdown",
)

n.write("**Post 3: r/LocalLLaMA / r/ChatGPTCoding**")
n.code(
    """Title: Your AI agent's analysis output looks terrible. I built a library to fix
that — 40+ widgets, structured Markdown, zero dependencies.

Body:

If you're building AI agents that do data analysis (with Claude, GPT,
local models, etc.), you've probably noticed the output is always a mess:
- Unformatted tables that don't align
- No charts or visualizations
- Inconsistent formatting between runs
- Just... walls of text

I built notebookmd to solve this. It gives agents a toolkit of 40+ widgets
for generating professional reports:

```python
n = nb("analysis.md", title="Stock Analysis")
n.metric("Price", "$142.50", delta="+3.2%")
n.table(price_df, name="Price History")
n.line_chart(price_df, x="date", y="close", title="30-Day Trend")
n.badge("BULLISH", style="success")
n.save()
```

The API is sequential — one function call at a time — which is exactly how
agents work. The output is clean Markdown with embedded charts, formatted
tables, and an artifact index.

The Markdown output is also readable by other LLMs, so you can chain agents:
one agent analyzes data → produces a notebookmd report → another agent reads
the Markdown and summarizes it.

[Before/after comparison: raw agent output vs notebookmd output]

GitHub: [link] | pip install notebookmd""",
    lang="markdown",
)

n.write("**Post 4: r/MachineLearning (optional — more technical angle)**")
n.code(
    """Title: We need better tooling for ML experiment reporting. I built a
zero-dependency Python library that generates structured Markdown reports.

Body:

Every ML team I've worked with has the same problem: you run experiments,
get results, and then spend ages formatting them into something shareable.
Jupyter exports are messy, Streamlit is overkill for static reports, and
W&B/MLflow are heavy infrastructure for simple experiment summaries.

notebookmd is a lightweight alternative: call Python functions
(n.metric(), n.table(), n.bar_chart()), get a Markdown file with
everything formatted. Zero dependencies, plugin architecture, built-in
asset management.

Particularly useful for:
- Automated experiment reports in CI/CD
- Agent-generated analysis summaries
- Quick shareable reports without spinning up infrastructure

GitHub: [link]""",
    lang="markdown",
)

n.divider()

# --- Hacker News ---
n.subheader("Hacker News — Show HN")

n.info(
    "HN values technical depth, novel approaches, and solving real problems. "
    "Keep the title factual. The first comment should explain motivation and architecture."
)

n.write("**Title options (ranked by viral potential):**")
n.write(
    '1. `Show HN: notebookmd — AI agents can\'t use Jupyter, so I built them their own notebook` *(strongest hook)*\n'
    '2. `Show HN: notebookmd — Streamlit-like API that outputs Markdown instead of a web app`\n'
    '3. `Show HN: notebookmd — The notebook for AI agents (Python to Markdown reports)`\n'
    '4. `Show HN: A zero-dependency Python library for generating structured Markdown reports`'
)

n.write("**First comment (critical for HN):**")
n.code(
    """Author here. I built notebookmd because I was frustrated with the gap between
"writing analysis code" and "presenting results."

The core insight: AI agents (and batch scripts) think sequentially — they call
functions one after another. Jupyter's cell model and Streamlit's reactive model
don't match that. notebookmd does: call n.metric(), n.table(), n.line_chart()
in order, get a Markdown file with everything properly formatted.

Architecture decisions that might interest HN:
- Zero-dependency core: the base package is pure Python, no imports at all.
  pandas/matplotlib are optional extras with graceful degradation.
- Plugin system: 8 built-in plugins provide 40+ widgets. Custom plugins via
  entry points or per-instance registration.
- Asset management: charts are saved as PNGs, CSVs exported alongside,
  all auto-linked in the output with an artifact index.

The output is intentionally Markdown (not HTML, not PDF) because it's the
one format that's natively readable by LLMs, humans, GitHub, and CI/CD systems.

Happy to discuss any design decisions. Code is MIT licensed.

GitHub: [link]""",
    lang="markdown",
)

n.divider()

# --- X / Twitter ---
n.subheader("X / Twitter")

n.info(
    "Twitter/X works best with visual threads. Lead with a hook, show code + output, "
    "end with a call to action. Threads of 5-8 tweets perform best for dev tools."
)

n.write("**Launch Thread:**")
n.code(
    """Tweet 1 (Hook):
AI agents can analyze your data, write SQL, and build models.

But they can't use Jupyter. They can't run Streamlit.
They're stuck with print().

So I built them their own notebook. It's called notebookmd. 🧵

---

Tweet 2 (Problem):
The problem: Jupyter needs a kernel and a browser.
Streamlit needs a running web server.

AI agents have neither.

When an agent finishes analyzing your data, the output
is always ugly, unformatted text dumps. No tables. No charts.
No structure.

---

Tweet 3 (Solution — with code screenshot):
notebookmd: call Python functions, get structured Markdown.

```python
n = nb("report.md", title="Analysis")
n.metric("Revenue", "$4.2M", delta="+18%")
n.table(df, name="Results")
n.line_chart(df, x="date", y="value")
n.save()
```

That's it. No server. No kernel. Just a .md file.

[Attach: code screenshot + output screenshot side by side]

---

Tweet 4 (Features):
What you get:
- Metrics with delta arrows (▲/▼)
- DataFrames as clean Markdown tables
- Charts saved as PNGs, auto-linked
- Collapsible sections, tabs, badges
- LaTeX math, code blocks, JSON display
- Built-in artifact index

40+ widgets total.

---

Tweet 5 (Architecture):
Design decisions I'm proud of:

- Zero dependencies core (pandas/matplotlib optional)
- Plugin architecture (8 built-in, extensible via entry points)
- Graceful degradation (missing deps = helpful message, not crash)
- Streamlit-compatible API (easy to learn if you know st.*)

---

Tweet 6 (Use cases):
Who it's for:

→ AI agent builders (Claude, GPT, LangChain)
→ Data scientists automating reports
→ DevOps teams with CI/CD report pipelines
→ Anyone who wants structured output from Python

---

Tweet 7 (CTA):
notebookmd is MIT licensed and on PyPI:

pip install notebookmd

GitHub: [link]
Docs: [link]

Star it if you find it useful. PRs welcome.

Feedback? Reply to this thread — I read everything.""",
    lang="markdown",
)

n.divider()

# --- Product Hunt ---
n.subheader("Product Hunt")

n.info(
    "Product Hunt rewards polished presentation, clear value propositions, and social proof. "
    "Launch on Tuesday-Thursday for best visibility. Prepare visuals in advance."
)

n.write("**Listing Details:**")
n.kv(
    {
        "Name": "notebookmd",
        "Tagline": "AI agents can't use Jupyter — so we built them their own notebook",
        "Description (short)": "A Streamlit-like Python API that outputs structured Markdown instead of a web app. 40+ widgets, zero dependencies, built for AI agents.",
        "Categories": "Developer Tools, Artificial Intelligence, Open Source",
        "Pricing": "Free — MIT License",
        "Platform": "Python (PyPI)",
    },
    title="Product Hunt Listing",
)

n.write("**Description (full):**")
n.code(
    """notebookmd is a Python library that gives AI agents (and developers) a
familiar Streamlit-like API for generating structured Markdown reports.

THE PROBLEM:
AI agents are great at data analysis. But presenting results? They're stuck
with print() and unformatted text. Jupyter needs a kernel. Streamlit needs
a server. There's no tool designed for how agents actually work — sequential
function calls that produce a shareable artifact.

THE SOLUTION:
Call n.metric(), n.table(), n.line_chart() — get a self-contained Markdown
file with metrics, tables, charts (as PNGs), and an artifact index.

KEY FEATURES:
• 40+ widgets: metrics, tables, charts, layout, status, analytics
• Zero dependencies: core is pure Python, optional extras for pandas/matplotlib
• Plugin architecture: extend with custom widgets
• Asset management: charts and CSVs auto-saved and linked
• Streamlit-compatible API: easy to learn if you know Streamlit

BUILT FOR:
• AI agent pipelines (Claude, GPT, LangChain, CrewAI)
• Automated reporting (CI/CD, cron jobs)
• Data science workflows ("notebook to production")
• Anyone who wants structured output from Python code

100% open source. MIT licensed. On PyPI.""",
    lang="markdown",
)

n.write("**Visuals to prepare:**")
n.write(
    "1. **Hero image** — Split screen: Python code on left, rendered Markdown report on right\n"
    "2. **Gallery image 1** — Widget showcase (metrics, tables, charts side by side)\n"
    "3. **Gallery image 2** — Before/after: raw `print()` output vs notebookmd output\n"
    "4. **Gallery image 3** — Agent workflow diagram: Agent → notebookmd → Markdown report\n"
    "5. **GIF/Video** — 30-second demo: write code, run script, show output file"
)

n.write("**Launch day checklist:**")
n.write(
    "- [ ] Post at 12:01 AM PST (Product Hunt resets at midnight PST)\n"
    "- [ ] Share link on X/Twitter immediately\n"
    "- [ ] Post in relevant Discord/Slack communities\n"
    "- [ ] Respond to every comment within 1 hour\n"
    "- [ ] Ask 5-10 supporters to upvote and leave genuine comments\n"
    "- [ ] Cross-post to r/Python with Product Hunt link"
)

n.divider()

# --- Dev.to / Hashnode / Medium ---
n.subheader("Dev.to / Hashnode / Medium — Technical Blog Posts")

n.write("**Blog Post 1: Launch Announcement**")
n.write(
    '**Title:** *"I built a Streamlit-like library that outputs Markdown — here\'s why"*\n\n'
    "**Structure:**\n"
    "1. The problem (with relatable examples)\n"
    "2. Why existing tools don't solve it (Jupyter, Streamlit, print)\n"
    "3. The solution: notebookmd with code examples\n"
    "4. Architecture deep-dive (zero deps, plugins, assets)\n"
    "5. Real output examples (embed actual generated Markdown)\n"
    "6. What's next + call for contributors"
)

n.write("**Blog Post 2: Tutorial (publish 3-5 days after launch)**")
n.write(
    '**Title:** *"Building automated data analysis reports with notebookmd and Claude"*\n\n'
    "**Structure:**\n"
    "1. Setup: install notebookmd + create a sample dataset\n"
    "2. Build a report step by step (metrics → tables → charts → export)\n"
    "3. Show the generated Markdown output\n"
    "4. Integrate with an AI agent (Claude/GPT) for automated analysis\n"
    "5. Add to a CI/CD pipeline for scheduled reports"
)

n.write("**Blog Post 3: Architecture Deep-Dive (publish week 2)**")
n.write(
    '**Title:** *"Zero dependencies, 40+ widgets: how I designed notebookmd\'s plugin architecture"*\n\n'
    "**Structure:**\n"
    "1. Design philosophy: why zero dependencies matters\n"
    "2. The plugin architecture (PluginSpec, auto-loading, entry points)\n"
    "3. How widgets render Markdown (emitters, asset management)\n"
    "4. Graceful degradation without optional deps\n"
    "5. How to build custom plugins"
)

# ─────────────────────────────────────────────────────────────
# Launch Timeline
# ─────────────────────────────────────────────────────────────
n.section("Launch Timeline")

n.write("**Build in Public (Weeks -6 to -2): Audience Priming**")
n.write(
    "Based on Will McGugan's Rich strategy, start sharing progress publicly before the official launch:\n\n"
    "- Post progress screenshots on X/Twitter as you build features\n"
    "- Contribute genuinely to r/Python and r/datascience discussions (don't just self-promote)\n"
    "- Share early on r/coolgithubprojects and r/opensource to accumulate 30-40 initial stars\n"
    "- The 30-40 star threshold is critical: reaching this in 1-2 hours after a Reddit post "
    "significantly increases chances of hitting GitHub Trending\n"
    "- If your entire Reddit history is self-promotion, you will be downvoted — spend 2-3 weeks "
    "contributing to discussions before launching"
)

n.write("**Pre-Launch (Week -1): Preparation**")
n.table(
    pd.DataFrame(
        [
            ["-7", "Finalize README, examples, and documentation", "GitHub"],
            ["-7", "Record 30-second demo GIF", "All"],
            ["-6", "Create Product Hunt listing (draft)", "Product Hunt"],
            ["-6", "Prepare all visual assets (hero image, gallery, screenshots)", "All"],
            ["-5", "Write launch blog post for Dev.to", "Dev.to"],
            ["-5", "Draft all Reddit posts", "Reddit"],
            ["-4", "Draft Twitter/X launch thread", "X/Twitter"],
            ["-4", "Line up 5-10 early supporters for launch day", "All"],
            ["-3", "Final testing: pip install from PyPI, run all examples", "PyPI"],
            ["-2", "Soft launch: share with close developer friends for feedback", "Private"],
            ["-1", "Final review of all content, fix any issues from soft launch", "All"],
        ],
        columns=["Day", "Task", "Platform"],
    ),
    name="Pre-Launch Tasks",
)

n.write("**Launch Day (Day 0): Tuesday or Wednesday**")
n.table(
    pd.DataFrame(
        [
            ["12:01 AM", "Product Hunt listing goes live", "Product Hunt"],
            ["6:00 AM", "Post Twitter/X launch thread", "X/Twitter"],
            ["7:00 AM", "Post on r/Python", "Reddit"],
            ["7:30 AM", "Post Show HN", "Hacker News"],
            ["8:00 AM", "Publish Dev.to blog post", "Dev.to"],
            ["8:30 AM", "Post on r/datascience", "Reddit"],
            ["9:00 AM", "Share in relevant Discord/Slack communities", "Discord/Slack"],
            ["All day", "Respond to every comment within 1 hour", "All"],
            ["Evening", "Post on r/LocalLLaMA, r/ChatGPTCoding", "Reddit"],
        ],
        columns=["Time (PST)", "Action", "Platform"],
    ),
    name="Launch Day Schedule",
)

n.write("**Post-Launch (Week 1-2): Momentum**")
n.table(
    pd.DataFrame(
        [
            ["+1", "Follow up on all comments, answer questions", "All"],
            ["+2", "Share any positive reception/metrics on X/Twitter", "X/Twitter"],
            ["+3", "Publish tutorial blog post", "Dev.to / Hashnode"],
            ["+5", "Post in Python/AI newsletters (Python Weekly, etc.)", "Email"],
            ["+7", "Week 1 metrics review — adjust strategy", "Internal"],
            ["+10", "Publish architecture deep-dive blog post", "Dev.to / Medium"],
            ["+14", "Launch retrospective — document learnings", "Internal"],
        ],
        columns=["Day", "Task", "Platform"],
    ),
    name="Post-Launch Tasks",
)

# ─────────────────────────────────────────────────────────────
# Conversion Playbook — Make People Try It
# ─────────────────────────────────────────────────────────────
n.section("Conversion Playbook — From 'Interesting' to 'pip install'")

n.write(
    "Awareness is worthless without conversion. This section documents specific, "
    "proven tactics from Rich, FastAPI, and Marimo that convert post readers into "
    "actual users. Each tactic is annotated with what to mimic for notebookmd."
)

n.subheader("Tactic 1: The Zero-Friction Try Command (from Rich)")
n.write(
    "**What Rich did:** After `pip install rich`, users can immediately run `python -m rich` "
    "with zero code to see a full demo of every feature. No file to create, no imports to write. "
    "This single command converted curiosity into a dopamine hit.\n\n"
    "**What notebookmd should do:** Create a `python -m notebookmd` command that generates a "
    "complete demo report to `demo_report.md` and opens it. The user sees the full power of "
    "the library in 5 seconds:"
)
n.code(
    """$ pip install notebookmd
$ python -m notebookmd

✨ Demo report generated: demo_report.md
   - 5 metrics with deltas
   - 2 data tables
   - 1 line chart
   - Collapsible sections
   - Artifact index

Open demo_report.md to see the output!""",
    lang="bash",
)
n.write(
    "**Why this works:** Every Reddit post, every HN comment, every tweet should end with "
    "these two lines. The reader can go from \"interesting\" to \"wow\" in under 30 seconds. "
    "Rich's `python -m rich` is cited by Will McGugan as one of the key drivers of adoption."
)

n.subheader("Tactic 2: The README as Conversion Funnel (from FastAPI)")
n.write(
    "**What FastAPI did:** The README follows a strict funnel:\n"
    "1. Hook (tagline + badges)\n"
    "2. Social proof (Microsoft, Netflix, Uber logos)\n"
    "3. Install command\n"
    "4. Minimal working example (8 lines)\n"
    "5. Run command\n"
    "6. Immediate result (JSON response in browser)\n\n"
    "Every step is copy-pasteable. Nothing requires thinking.\n\n"
    "**What notebookmd should mimic:**"
)
n.code(
    """# README structure (in order)

## 1. Hook (first 2 lines)
> **The notebook for AI agents.** Write Python. Get Markdown reports.

## 2. Badges (star count, PyPI version, zero deps, tests passing)

## 3. GIF demo (code → rendered output, 5 seconds)

## 4. Install + Try (copy-paste)
pip install notebookmd
python -m notebookmd  # instant demo

## 5. Minimal working example (6 lines)
from notebookmd import nb
n = nb("report.md", title="My Report")
n.metric("Revenue", "$4.2M", delta="+18%")
n.table(df, name="Results")
n.save()

## 6. Show the output (screenshot of rendered Markdown)

## 7. Feature list (scan-friendly bullets)

## 8. Comparison table (vs Jupyter, Streamlit, print())

## 9. More examples link""",
    lang="markdown",
)

n.subheader("Tactic 3: Try Without Installing (from Marimo)")
n.write(
    "**What Marimo did:** A hosted playground where users can try the tool in-browser "
    "with zero installation. Every feature demo links to a runnable notebook.\n\n"
    "**What notebookmd can do (lighter-weight alternatives):**\n\n"
    "- **GitHub Codespaces / Gitpod button** — One-click cloud environment with notebookmd "
    "pre-installed and a demo script ready to run\n"
    "- **Google Colab notebook** — A Colab notebook that `!pip install notebookmd`, runs a "
    "demo, and shows the generated Markdown inline\n"
    "- **Replit template** — A pre-configured Replit with a \"Run\" button\n"
    "- **Copy-paste playground in docs** — An interactive code editor on the docs site "
    "that renders Markdown output in real-time\n\n"
    "Even one of these dramatically reduces the gap between \"saw a post\" and \"tried it.\""
)

n.subheader("Tactic 4: Before/After Visual Proof (from Rich)")
n.write(
    "**What Rich did:** Every feature showed the ugly default Python output next to the "
    "beautiful Rich-formatted version. The visual contrast was immediately shareable.\n\n"
    "**What notebookmd should create:**"
)
n.table(
    pd.DataFrame(
        [
            ["Agent text dump", "notebookmd report", "Reddit, HN, X thread"],
            ["Raw print() metrics", "n.metric() with delta arrows", "X thread tweet 3"],
            ["Unformatted data", "n.table() with headers", "README, blog post"],
            ["No visualization", "n.line_chart() embedded PNG", "Product Hunt gallery"],
            ["Scattered files", "Artifact index + auto-linked assets", "README features section"],
        ],
        columns=["Before (ugly)", "After (notebookmd)", "Where to use"],
    ),
    name="Before/After Comparison Assets",
)
n.write(
    "**The before/after image is the single most shareable asset.** Rich's entire viral "
    "spread was built on the visual contrast. For notebookmd, the contrast is between "
    "a wall of `print()` text and a structured Markdown report with metrics, tables, and charts."
)

n.subheader("Tactic 5: Progressive Complexity Ladder (from FastAPI + Rich)")
n.write(
    "**What they did:** Started with the simplest possible example, then gradually showed "
    "more advanced features. Never overwhelmed the reader upfront.\n\n"
    "**notebookmd's complexity ladder for posts and docs:**"
)
n.code(
    """# Level 1: One-liner (in tweet or comment)
python -m notebookmd  # generates a full demo report

# Level 2: Three lines (in Reddit post)
from notebookmd import nb
n = nb("report.md", title="My Report")
n.metric("Revenue", "$4.2M", delta="+18%")
n.save()

# Level 3: Full example (in README)
n = nb("report.md", title="Q4 Analysis")
n.metric_row([...])
n.table(df, name="Results")
n.line_chart(df, x="date", y="value")
n.save()

# Level 4: Advanced (in tutorial blog post)
with n.expander("Details"):
    n.summary(df)
    n.export_csv(df, "data.csv")
n.badge("COMPLETE", style="success")""",
    lang="python",
)

n.subheader("Tactic 6: Social Proof in Every Post (from FastAPI)")
n.write(
    "**What FastAPI did:** Every mention included logos of companies using it (Microsoft, "
    "Netflix, Uber). This transformed \"random library\" into \"trusted tool.\"\n\n"
    "**What notebookmd should do immediately after launch:**\n\n"
    "- Add a \"Used by\" section to the README as soon as anyone notable uses it\n"
    "- Screenshot any positive tweets/comments and add to a \"What people are saying\" section\n"
    "- If any agent framework (LangChain, CrewAI) integrates it, feature that prominently\n"
    "- Track GitHub stars publicly (star-history.com badge in README)\n"
    "- After the first blog mention, add \"Featured in\" badges"
)

n.subheader("Tactic 7: The Agent Demo That Sells Itself")
n.write(
    "**Unique to notebookmd — no comparable library has done this:**\n\n"
    "Create a short script or video showing an AI agent (Claude or GPT) analyzing a CSV "
    "file and producing a notebookmd report in real-time. The workflow:\n\n"
    "1. User gives agent a CSV file and asks \"analyze this data\"\n"
    "2. Agent writes a Python script using notebookmd\n"
    "3. Script runs, generates `report.md` with metrics, tables, charts\n"
    "4. Show the rendered Markdown — clean, structured, professional\n\n"
    "**This demo is the killer app.** No other library can show this workflow. "
    "It makes the value proposition visceral: *\"this is what your agent's output "
    "looks like with notebookmd vs without it.\"*\n\n"
    "Post this as:\n"
    "- A 30-second GIF in the GitHub README\n"
    "- A screen recording for Product Hunt\n"
    "- Tweet 3-4 in the X/Twitter thread\n"
    "- The hero image in blog posts"
)

n.subheader("Tactic 8: Copy-Paste Everywhere")
n.write(
    "**What all successful launches share:** Every code example is copy-pasteable. "
    "No placeholder variables, no ... ellipsis, no \"configure your settings here.\"\n\n"
    "**Rules for notebookmd examples:**\n\n"
    "- Every code block must run as-is (use inline data, not external files)\n"
    "- Always show the install command right before the code\n"
    "- Always show what the output looks like right after the code\n"
    "- Use realistic but simple data (revenue numbers, stock prices, sales counts)\n"
    "- End every post with the two-line install+demo:\n"
    "  ```\n"
    "  pip install notebookmd\n"
    "  python -m notebookmd\n"
    "  ```"
)

n.subheader("Conversion Checklist")
n.table(
    pd.DataFrame(
        [
            ["python -m notebookmd demo command", "Lets users try in 5 seconds", "Rich", "TODO"],
            ["README funnel (hook → install → example → output)", "Converts GitHub visitors", "FastAPI", "TODO"],
            ["Before/after comparison image", "Most shareable visual asset", "Rich", "TODO"],
            ["Google Colab or Gitpod one-click demo", "Try without installing", "Marimo", "TODO"],
            ["Agent demo GIF (CSV → analysis → report)", "Killer app demonstration", "Unique", "TODO"],
            ["Copy-paste examples with inline data", "Zero friction to first success", "All", "TODO"],
            ["Star-history badge in README", "Social proof momentum", "FastAPI", "TODO"],
            ["'What people are saying' README section", "Social validation", "Rich", "TODO"],
        ],
        columns=["Tactic", "Why It Works", "Inspired By", "Status"],
    ),
    name="Conversion Tactics Checklist",
)

# ─────────────────────────────────────────────────────────────
# Success Patterns from Similar Projects
# ─────────────────────────────────────────────────────────────
n.section("Lessons from Successful Open-Source Launches")

n.subheader("What Works on Reddit")
n.write(
    '- **Lead with the problem, not the solution.** Posts titled "I was frustrated with X, so I built Y" '
    "consistently outperform \"Check out my new library\" posts\n"
    "- **Show real output.** Screenshots/GIFs of actual generated reports get 3-5x more engagement\n"
    "- **Explain design decisions.** r/Python loves architecture discussions — \"why zero deps?\" "
    '"why Markdown?" are great conversation starters\n'
    "- **Be present in comments.** The author responding to every question signals commitment\n"
    "- **Don't cross-post simultaneously.** Stagger by 1-2 hours to avoid appearing spammy"
)

n.subheader("What Works on Hacker News")
n.write(
    "- **Factual titles.** No marketing language, no superlatives. State what it does.\n"
    "- **First comment is critical.** Explain motivation, architecture, and trade-offs immediately\n"
    "- **Technical depth wins.** HN commenters will ask about edge cases, performance, and alternatives\n"
    "- **Timing matters.** Post between 6-10 AM PST on weekdays for best visibility\n"
    "- **Respond thoughtfully.** HN rewards detailed, honest responses to criticism"
)

n.subheader("What Works on Product Hunt")
n.write(
    "- **Polished visuals.** The hero image and gallery are more important than the description\n"
    "- **Tagline is everything.** Must be clear in 10 words or less\n"
    "- **First hour momentum.** Initial upvotes determine ranking for the day\n"
    "- **Maker comments.** Product Hunt highlights maker responses — respond to everything\n"
    "- **Tuesday-Thursday launches.** Fewer competing launches, better visibility"
)

n.subheader("What Works on X/Twitter")
n.write(
    "- **Visual threads.** Code screenshots + output screenshots get shared\n"
    "- **Thread format.** 5-8 tweets, one idea per tweet, hook in tweet 1\n"
    "- **Tag relevant accounts.** Mention AI agent frameworks, Python accounts, data science influencers\n"
    "- **Retweet strategy.** Ask 5-10 people with >1K followers to RT the first tweet\n"
    "- **Follow-up content.** Post use cases and tips over the following week"
)

n.subheader("Case Studies: Successful Similar Launches")

n.write(
    "These Python/dev-tool launches demonstrate patterns directly applicable to notebookmd."
)

n.table(
    pd.DataFrame(
        [
            ["Rich (Will McGugan)", "49,000+ stars", "362 pts on HN", "Visual GIFs of terminal output"],
            ["Marimo", "10,000+ stars", "448 pts, 106 comments on HN", "\"Notebooks are broken\" narrative"],
            ["MarkItDown (Microsoft)", "86,000+ stars", "Top of HN", "Universal need + simple API"],
            ["FastAPI", "80,000+ stars", "Top of HN", "Comparison table vs Flask/Django"],
            ["Cursor", "PH Product of Year '24", "5 PH launches", "Iterated with multiple launches"],
            ["Polars", "35,000+ stars", "Top of HN", "Reproducible benchmark comparisons"],
        ],
        columns=["Project", "GitHub Stars", "Community Reception", "Key Tactic"],
    ),
    name="Comparable Launch Examples",
)

n.write(
    "**Rich by Will McGugan** — The gold standard for Python library launches. "
    "Will posted to r/Python with a GIF demo, stayed in comments answering every question, "
    "and grew from zero to 49,000+ stars. His key insight: *\"The sweet-spot is closer to "
    "early than finished\"* — launch when you have a core feature and a decent README. "
    "Rich's inherently visual nature (formatted terminal output) drove massive sharing. "
    "notebookmd can replicate this with before/after screenshots of raw vs structured Markdown output.\n\n"
    "**Marimo** — The most directly comparable launch. A Python notebook tool positioned as a "
    "better alternative to Jupyter. Its Show HN post earned 448 points and 106 comments because "
    "it solved universally recognized pain points (Jupyter's hidden state, unreproducible execution, "
    "JSON file format that breaks git). The title was crystal clear: *\"Marimo — an open-source reactive "
    "notebook for Python.\"* They launched multiple times (5+ Show HN posts over 2024-2025), each "
    "building on the last (WASM version, VS Code extension, cloud workspace).\n\n"
    "**MarkItDown by Microsoft** — A document-to-Markdown converter that reached 86,000+ stars. "
    "Relevant because it occupies the same Python + Markdown generation space. Success came from "
    "solving a universal need with a dead-simple API.\n\n"
    "**Key takeaway for notebookmd:** Frame against a known tool (\"Streamlit-like API, but outputs "
    "Markdown\"), emphasize zero dependencies (HN loves minimal tools), target the AI agent use case "
    "(hottest trend in 2025-2026), and invest heavily in visual proof (GIF of code → rendered output)."
)

n.subheader("The Universal Formula Across Platforms")
n.write(
    "Analyzing all successful launches reveals 6 patterns that appear everywhere:\n\n"
    "1. **Solve a recognized pain point** — Every viral launch addresses a problem people already have. "
    "The problem should be explainable in one sentence.\n"
    "2. **Crystal-clear positioning in one line** — \"An open-source reactive notebook for Python\" (Marimo), "
    "\"Python lib for rich text, markdown, tables in the terminal\" (Rich)\n"
    "3. **Visual proof is the highest-leverage investment** — Every successful launch featured a GIF or screenshot. "
    "McGugan explicitly credits Rich's visual nature as a key factor.\n"
    "4. **Ship early, not perfect** — Early community feedback shapes the product. Waiting for feature-complete "
    "means missing the window for building interest.\n"
    "5. **Engage relentlessly on launch day** — Respond to every comment within 30 minutes. Clear your calendar. "
    "Active participation increases Product Hunt traffic by 60%.\n"
    "6. **Relaunch with updates** — Marimo did 5+ Show HN posts. Cursor did 5 Product Hunt launches. Each one "
    "builds on accumulated credibility."
)

n.subheader("Platform Conversion Comparison")
n.info(
    "Research shows HN converts better than Product Hunt for developer tools. "
    "One analysis found: HN yielded #2 on the front page, 107 points, 50+ stars, and 100+ installs. "
    "Product Hunt yielded #14 of the day, 193 votes, but only ~30 installs. "
    "Prioritize HN for a developer tool like notebookmd."
)

n.subheader("Optimal Timing by Platform")
n.table(
    pd.DataFrame(
        [
            ["Hacker News (Show HN)", "Sun or Tue-Thu", "6 AM UTC / 8 AM EST", "Weekends = less competition"],
            ["Reddit (r/Python)", "Tue-Thu", "8-10 AM EST", "US business hours; use 'I Made This' flair"],
            ["Product Hunt", "Tue-Thu or Sun", "12:01 AM PST", "Full 24-hour cycle; Sun = easier to win"],
            ["X/Twitter", "Weekdays", "Mid-day EST", "Align with US dev audiences"],
        ],
        columns=["Platform", "Best Day", "Best Time", "Notes"],
    ),
    name="Optimal Posting Times",
)

# ─────────────────────────────────────────────────────────────
# Content Assets to Prepare
# ─────────────────────────────────────────────────────────────
n.section("Content Assets Checklist")

n.write("Prepare these assets before launch day:")

n.table(
    pd.DataFrame(
        [
            ["Hero image (code to report split)", "PNG 1270x760", "Product Hunt, blog, social", "TODO"],
            ["Widget showcase screenshot", "PNG 1200x800", "Reddit, Product Hunt gallery", "TODO"],
            ["Before/after comparison", "PNG 1200x600", "Reddit, X/Twitter, blog", "TODO"],
            ["30-second demo GIF", "GIF 800x500", "GitHub README, Reddit, HN", "TODO"],
            ["Agent workflow diagram", "PNG/SVG", "Blog post, Product Hunt", "TODO"],
            ["Code example screenshots (3-4)", "PNG 800x400", "X/Twitter thread", "TODO"],
            ["Output example screenshots (3-4)", "PNG 800x600", "X/Twitter thread, Reddit", "TODO"],
            ["Logo / icon", "SVG + PNG", "Product Hunt, GitHub, PyPI", "TODO"],
            ["Open Graph image", "PNG 1200x630", "Link previews on social media", "TODO"],
        ],
        columns=["Asset", "Format", "Purpose", "Status"],
    ),
    name="Visual Assets",
)

# ─────────────────────────────────────────────────────────────
# Additional Channels
# ─────────────────────────────────────────────────────────────
n.section("Additional Distribution Channels")

n.subheader("Newsletters & Aggregators")
n.write(
    "Submit to these newsletters/aggregators after launch day:\n\n"
    "- **Python Weekly** — Submit via their website. Best if you have a blog post link.\n"
    "- **PyCoder's Weekly** — Submit interesting Python content. Architecture posts do well.\n"
    "- **Data Science Weekly** — Good for the data science angle.\n"
    "- **TLDR Newsletter** — Submit for the open-source section.\n"
    "- **Console.dev** — Curates developer tools. Submit early.\n"
    "- **awesome-python** — Submit a PR to the appropriate category after launch.\n"
    "- **awesome-ai-agents** — Submit a PR highlighting the agent use case."
)

n.subheader("Discord & Slack Communities")
n.write(
    "- **Python Discord** — #showcase channel\n"
    "- **MLOps Community Slack** — Share in #tools or #general\n"
    "- **Data Science Discord** — Relevant channels\n"
    "- **LangChain Discord** — Agent tooling discussions\n"
    "- **Claude/Anthropic Discord** — Tool use and agent workflows"
)

n.subheader("GitHub Ecosystem")
n.write(
    "- Ensure the GitHub repo has: descriptive README, topics/tags, license, contributing guide\n"
    "- Add **\"good first issue\"** labels to 3-5 issues for new contributors\n"
    "- Create a **GitHub Discussion** for community Q&A\n"
    "- Consider a **GitHub Pages** site for documentation"
)

# ─────────────────────────────────────────────────────────────
# Metrics & Goals
# ─────────────────────────────────────────────────────────────
n.section("Success Metrics & Goals")

n.subheader("Week 1 Targets")
n.metric_row([
    {"label": "GitHub Stars", "value": "200+"},
    {"label": "PyPI Downloads", "value": "500+"},
    {"label": "Reddit Upvotes", "value": "100+"},
    {"label": "HN Points", "value": "50+"},
])

n.subheader("Month 1 Targets")
n.metric_row([
    {"label": "GitHub Stars", "value": "500+"},
    {"label": "PyPI Downloads", "value": "2,000+"},
    {"label": "Contributors", "value": "5+"},
    {"label": "Blog Mentions", "value": "3+"},
])

n.subheader("Tracking")
n.write(
    "- **GitHub**: Stars, forks, issues, PRs (GitHub Insights)\n"
    "- **PyPI**: Download stats via pypistats.org or `pypistats` CLI\n"
    "- **Reddit**: Post upvotes, comments, cross-posts\n"
    "- **Hacker News**: Points, comments, front page duration\n"
    "- **Product Hunt**: Upvotes, comments, daily ranking\n"
    "- **X/Twitter**: Thread impressions, retweets, link clicks\n"
    "- **Blog**: Views, claps/likes, time on page"
)

# ─────────────────────────────────────────────────────────────
# Risk Mitigation
# ─────────────────────────────────────────────────────────────
n.section("Risks & Mitigation")

n.warning("**Risk: \"Why not just use Jinja2 templates?\"**")
n.write(
    "**Response:** Jinja2 is a general-purpose template engine — you still have to design "
    "the template, handle data formatting, manage assets, and write the rendering logic. "
    "notebookmd gives you 40+ pre-built widgets with a sequential API. It's the difference "
    "between building a car and driving one."
)

n.warning("**Risk: \"Markdown is too limited for real reports\"**")
n.write(
    "**Response:** Markdown is intentionally the output format because it's universal — "
    "readable by LLMs, renderable by GitHub, convertible to HTML/PDF via pandoc. "
    "For richer output, the Markdown contains embedded PNGs for charts and structured "
    "tables that render well everywhere."
)

n.warning("**Risk: \"This is just a print() wrapper\"**")
n.write(
    "**Response:** Show the output. The structured Markdown with metrics (delta arrows), "
    "formatted tables, embedded charts, collapsible sections, and artifact indexes "
    "is clearly more than print(). The asset management alone (auto-saving PNGs, CSVs, "
    "deduplication, relative linking) solves real problems."
)

n.warning("**Risk: Low engagement on launch day**")
n.write(
    "**Mitigation:** Don't launch on all platforms simultaneously. Start with Reddit (most "
    "forgiving), gauge reception, iterate messaging, then launch on HN and Product Hunt. "
    "A staggered launch over 2-3 days reduces risk and lets you refine the pitch."
)

# ─────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────
n.section("Summary & Next Steps")

n.success(
    "notebookmd solves a real, widely-felt pain point (structured output from Python/AI agents) "
    "with a clean, zero-dependency solution. The launch strategy focuses on authenticity, "
    "technical depth, and visual demonstrations across 5+ platforms."
)

n.write(
    "**Immediate next steps:**\n\n"
    "1. Prepare visual assets (hero image, demo GIF, screenshots)\n"
    "2. Finalize and polish all platform content drafts above\n"
    "3. Set up tracking for all metrics\n"
    "4. Identify and reach out to 5-10 early supporters\n"
    "5. Choose launch date (Tuesday or Wednesday, avoid major tech news days)\n"
    "6. Execute pre-launch checklist starting 7 days before"
)

# ─────────────────────────────────────────────────────────────
# References
# ─────────────────────────────────────────────────────────────
n.section("References & Further Reading")

n.write(
    "Research sources used to compile this launch plan:\n\n"
    "**Launch strategy guides:**\n"
    "- Will McGugan: [Promoting Your Open Source Project](https://www.willmcgugan.com/blog/tech/post/promoting-your-open-source-project-or-how-to-get-your-first-1k-github-stars/) — How Rich went from 0 to 1K+ stars\n"
    "- Markepear: [How to Launch a Dev Tool on Hacker News](https://www.markepear.dev/blog/dev-tool-hacker-news-launch) — Deep tactical HN guide\n"
    "- Product Hunt: [Preparing for Launch](https://www.producthunt.com/launch/preparing-for-launch) — Official launch guidance\n"
    "- Stackfix: [Product Hunt Launch Guide](https://www.stackfix.com/blog/startup-advice/product-hunt-launch-guide)\n"
    "- freeCodeCamp: [How We Got Trending on GitHub in 48 Hours](https://www.freecodecamp.org/news/how-we-got-a-2-year-old-repo-trending-on-github-in-just-48-hours-12151039d78b/)\n\n"
    "**Comparable launches:**\n"
    "- Marimo Show HN post: [448 points, 106 comments](https://news.ycombinator.com/item?id=38971966)\n"
    "- Rich Show HN post: [362 points](https://bestofshowhn.com/search?q=python) — via Best of Show HN\n"
    "- Best of Show HN 2024-2025: [bestofshowhn.com](https://bestofshowhn.com/2025)\n"
    "- Product Hunt Developer Tools: [producthunt.com/topics/developer-tools](https://www.producthunt.com/topics/developer-tools)\n\n"
    "**Timing research:**\n"
    "- [Best time to post on HN](https://www.indiehackers.com/post/best-time-to-post-to-hacker-news-b52bece549) — Indie Hackers analysis\n"
    "- [Best time for Show HN](https://www.myriade.ai/blogs/when-is-it-the-best-time-to-post-on-show-hn) — Myriade analysis\n"
    "- [chanind HN timing analysis](https://chanind.github.io/2019/05/07/best-time-to-submit-to-hacker-news.html)\n\n"
    "**Content creation:**\n"
    "- Build Solo: [Twitter Thread Template](https://buildsolo.io/twitter-thread-template/)\n"
    "- [awesome-readme on GitHub](https://github.com/matiassingers/awesome-readme) — README best practices\n"
    "- HN: [Show HN Guidelines](https://news.ycombinator.com/showhn.html)"
)

# Save
out = n.save()
print(f"Report saved to: {out}")
