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
    "Common frustrations include:\n\n"
    '- *"Jupyter is great for exploration, terrible for automation"* — a sentiment echoed across r/datascience\n'
    '- Hidden state and out-of-order cell execution cause unreproducible results\n'
    '- `.ipynb` files are JSON blobs that create merge conflicts in git\n'
    '- No good way to run notebooks in CI/CD pipelines without heavy tooling (papermill, nbconvert)\n'
    '- Exporting to Markdown/HTML loses interactivity and often breaks formatting'
)

n.subheader("2. Streamlit Requires a Running Server")
n.write(
    "Streamlit is loved for interactive dashboards but has fundamental limitations for batch/agent workflows:\n\n"
    '- *"I just want to generate a report, not run a web server"*\n'
    "- Can't be used in CI/CD, cron jobs, or agent pipelines\n"
    "- Overkill for one-off analysis results that need to be saved and shared\n"
    "- No artifact output — results exist only while the server runs"
)

n.subheader("3. AI Agents Lack Structured Output Tools")
n.write(
    "As AI agents become mainstream for data analysis, a gap has emerged:\n\n"
    '- Agents default to `print()` statements and unformatted text dumps\n'
    '- LLM-generated Markdown is inconsistent — tables break, formatting varies\n'
    "- No standard way for agents to produce charts, metrics, and tables together\n"
    '- *"I want my agent to produce a report a stakeholder can actually read"*\n'
    "- Agent frameworks (LangChain, CrewAI, Claude) focus on reasoning, not presentation"
)

n.subheader("4. The 'Last Mile' of Data Analysis")
n.write(
    "Data scientists spend significant time formatting results after analysis is done:\n\n"
    "- Manually formatting Markdown tables is tedious and error-prone\n"
    "- Saving charts, linking them in reports, managing file paths — all manual\n"
    "- No single tool combines metrics + tables + charts + text in one API\n"
    '- *"80% of my time is analysis, 20% is making the output look presentable"*'
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

n.write("**Post 1: r/Python (Primary Launch)**")
n.code(
    """Title: I built a Streamlit-like library that outputs Markdown instead of a web app — for AI agents and batch reports

Body:

Hey r/Python,

I kept running into the same problem: I'd write a data analysis script (or have
an AI agent write one), and the output was always ugly print() dumps or
unstructured text. Jupyter needs a kernel, Streamlit needs a server — I just
wanted to call functions and get a clean report.

So I built notebookmd — a Python library with 40+ widgets (metrics, tables,
charts, layout) that outputs structured Markdown files instead of a web app.

```python
from notebookmd import nb

n = nb("report.md", title="Q4 Analysis")
n.metric("Revenue", "$4.2M", delta="+18%")
n.table(df, name="Top Performers")
n.line_chart(df, x="month", y="revenue", title="Trend")
n.save()
```

Key design decisions:
- Zero dependencies core (pandas/matplotlib optional)
- Streamlit-compatible API (n.metric(), n.table(), n.bar_chart()...)
- Built-in asset management (charts saved as PNGs, auto-linked)
- Plugin architecture for custom widgets
- Output is readable by LLMs, humans, GitHub, and CI/CD

I built this primarily for AI agent workflows, but it works great for any
batch reporting or "notebook to production" pipeline.

GitHub: [link]
PyPI: pip install notebookmd
Docs: [link]

Happy to answer any questions about the architecture or design decisions!""",
    lang="markdown",
)

n.write("**Post 2: r/datascience**")
n.code(
    """Title: Tired of Jupyter for production reports? I made a library that generates
Markdown reports from Python function calls

Body:

As a data scientist, my workflow was always:
1. Do analysis in Python
2. Spend 30 minutes formatting results into something shareable
3. Realize I need to re-run it next week and do it all over again

notebookmd fixes step 2 and 3. It's a Python library where you call functions
like n.metric(), n.table(), n.summary() and get a clean Markdown report with
charts, metrics, and tables — no Jupyter kernel, no Streamlit server.

[Code example + output screenshot]

It's particularly useful for:
- Automated weekly/monthly reports
- AI agent analysis pipelines
- Anything where you want reproducible, git-friendly report output

Zero dependencies by default. MIT licensed.

GitHub: [link] | PyPI: pip install notebookmd""",
    lang="markdown",
)

n.write("**Post 3: r/LocalLLaMA / r/ChatGPTCoding**")
n.code(
    """Title: I built a report-generation library specifically designed for AI agents —
call n.metric(), n.table(), n.chart() and get structured Markdown

Body:

If you're building AI agents that do data analysis, you've probably noticed
the output is always a mess — unformatted tables, no charts, just text dumps.

notebookmd gives agents a proper toolkit for generating reports. The API is
sequential (one function call at a time, exactly how agents work), and the
output is clean Markdown that's readable by both humans and other LLMs.

40+ widgets. Zero dependencies. Plugin system for custom needs.

[Before/after comparison: raw agent output vs notebookmd output]

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

n.write("**Title options (pick one):**")
n.write(
    '1. `Show HN: notebookmd — A Streamlit-like API that outputs Markdown instead of a web app`\n'
    '2. `Show HN: notebookmd — The notebook for AI agents (Python to Markdown reports)`\n'
    '3. `Show HN: I built a zero-dependency Python library for generating structured Markdown reports`'
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
I built a Python library that works like Streamlit — but outputs
Markdown files instead of a web app.

40+ widgets. Zero dependencies. Built for AI agents.

It's called notebookmd. Here's why it exists: 🧵

---

Tweet 2 (Problem):
The problem: AI agents are great at data analysis.

But their output? Ugly print() dumps and unformatted text.

- Jupyter needs a kernel
- Streamlit needs a server
- Raw Markdown is tedious

Agents need something simpler.

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
        "Tagline": "The notebook for AI agents — Write Python, get Markdown reports",
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

n.subheader("Examples of Successful Similar Launches")
n.write(
    "These Python/dev-tool launches demonstrate patterns worth emulating:\n\n"
    "- **Rich (Python)** — Terminal formatting library. Launched with beautiful screenshots showing "
    "before/after terminal output. The visual impact drove massive sharing.\n"
    "- **FastAPI** — Positioned against Flask/Django with a clear comparison table and benchmark numbers. "
    "Technical credibility + clear differentiation.\n"
    "- **Pydantic** — Grew through genuine developer word-of-mouth. Tutorial content on Dev.to and "
    "Medium drove sustained adoption.\n"
    "- **Typer** — Same author as FastAPI. Leveraged existing community trust. Launch posts "
    "referenced the familiar FastAPI API design.\n"
    "- **Marimo** — Reactive notebook alternative. Launched with a compelling \"notebooks are broken\" "
    "narrative and live demo. Strong HN reception.\n"
    "- **Polars** — DataFrame library. Launched with benchmark comparisons against pandas. "
    "Performance claims backed by reproducible benchmarks drove technical credibility."
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

# Save
out = n.save()
print(f"Report saved to: {out}")
