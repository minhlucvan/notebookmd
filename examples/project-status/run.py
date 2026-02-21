"""Project Status Report Demo — notebookmd

Builds a sprint status report from task tracking data:
- Sprint health badges and progress bars
- Task breakdown by status and priority
- Team workload analysis
- Risk and blocker callouts
- Burndown-style chart

Run:
    cd examples/project-status
    python run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from notebookmd import NotebookConfig, nb

try:
    import pandas as pd

    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    HAS_MPL = True
except ImportError:
    HAS_MPL = False

HERE = Path(__file__).resolve().parent


def main():
    cfg = NotebookConfig(max_table_rows=20)
    n = nb(HERE / "README.md", title="Project Status Report", cfg=cfg)

    if not HAS_PANDAS:
        n.warning("pandas is required for this demo. Install with: `pip install 'notebookmd[pandas]'`")
        n.save()
        return

    # ── Load Data ──
    df = pd.read_csv(HERE / "data" / "tasks.csv")

    # ══════════════════════════════════════════════════════════════
    # PROJECT OVERVIEW
    # ══════════════════════════════════════════════════════════════
    n.section("Project Overview")
    n.badge("Sprint 2", style="info")
    n.badge("IN PROGRESS", style="warning")

    total_tasks = len(df)
    completed = len(df[df["status"] == "completed"])
    in_progress = len(df[df["status"] == "in_progress"])
    blocked = len(df[df["status"] == "blocked"])
    completion_pct = completed / total_tasks

    n.metric_row(
        [
            {"label": "Total Tasks", "value": str(total_tasks)},
            {"label": "Completed", "value": str(completed), "delta": f"{completion_pct:.0%}"},
            {"label": "In Progress", "value": str(in_progress)},
            {"label": "Blocked", "value": str(blocked)},
        ]
    )

    n.progress(completion_pct, f"Overall: {completed}/{total_tasks} tasks complete")

    # ══════════════════════════════════════════════════════════════
    # SPRINT BREAKDOWN
    # ══════════════════════════════════════════════════════════════
    n.section("Sprint Breakdown")

    for sprint in df["sprint"].unique():
        sprint_df = df[df["sprint"] == sprint]
        sprint_done = len(sprint_df[sprint_df["status"] == "completed"])
        sprint_total = len(sprint_df)
        pct = sprint_done / sprint_total if sprint_total > 0 else 0

        if pct == 1.0:
            n.badge(sprint, style="success")
        elif pct > 0:
            n.badge(sprint, style="warning")
        else:
            n.badge(sprint, style="default")

        n.progress(pct, f"{sprint}: {sprint_done}/{sprint_total} complete")
        n.table(
            sprint_df[["task_id", "title", "assignee", "status", "priority"]],
            name=f"{sprint} Tasks",
        )

    # ══════════════════════════════════════════════════════════════
    # TASK STATUS SUMMARY
    # ══════════════════════════════════════════════════════════════
    n.section("Status Summary")

    status_counts = df["status"].value_counts().to_dict()
    n.kv(
        {k: str(v) for k, v in status_counts.items()},
        title="Tasks by Status",
    )

    priority_counts = df["priority"].value_counts().to_dict()
    n.kv(
        {k: str(v) for k, v in priority_counts.items()},
        title="Tasks by Priority",
    )

    if HAS_MPL:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Status pie
        status_labels = list(status_counts.keys())
        status_values = list(status_counts.values())
        colors_map = {"completed": "#22c55e", "in_progress": "#3b82f6", "pending": "#a1a1aa", "blocked": "#ef4444"}
        colors = [colors_map.get(s, "#a1a1aa") for s in status_labels]
        ax1.pie(status_values, labels=status_labels, colors=colors, autopct="%1.0f%%", startangle=90)
        ax1.set_title("Tasks by Status")

        # Priority bar
        prio_labels = list(priority_counts.keys())
        prio_values = list(priority_counts.values())
        prio_colors = {"high": "#ef4444", "medium": "#f59e0b", "low": "#22c55e"}
        ax2.bar(prio_labels, prio_values, color=[prio_colors.get(p, "#a1a1aa") for p in prio_labels])
        ax2.set_title("Tasks by Priority")
        ax2.set_ylabel("Count")
        ax2.grid(True, alpha=0.3, axis="y")

        fig.tight_layout()
        n.figure(fig, "task_breakdown.png", caption="Task distribution by status and priority")
        plt.close(fig)

    # ══════════════════════════════════════════════════════════════
    # TEAM WORKLOAD
    # ══════════════════════════════════════════════════════════════
    n.section("Team Workload")

    team = (
        df.groupby("assignee")
        .agg(
            tasks=("task_id", "count"),
            completed=("status", lambda x: (x == "completed").sum()),
            estimated=("estimate_hours", "sum"),
            actual=("actual_hours", "sum"),
        )
        .reset_index()
    )
    team["completion"] = (team["completed"] / team["tasks"] * 100).round(0).astype(int)
    team = team.sort_values("tasks", ascending=False)
    n.table(team, name="Workload by Team Member")

    # Highlight over/under estimates
    with n.expander("Estimation Accuracy", expanded=True):
        for _, row in team.iterrows():
            if row["actual"] > 0:
                ratio = row["actual"] / row["estimated"] if row["estimated"] > 0 else 0
                if ratio > 1.1:
                    n.warning(
                        f"**{row['assignee']}**: {row['actual']}h actual vs {row['estimated']}h estimated "
                        f"({ratio:.0%} — over estimate)"
                    )
                elif ratio < 0.9:
                    n.success(
                        f"**{row['assignee']}**: {row['actual']}h actual vs {row['estimated']}h estimated "
                        f"({ratio:.0%} — under estimate)"
                    )
                else:
                    n.info(
                        f"**{row['assignee']}**: {row['actual']}h actual vs {row['estimated']}h estimated "
                        f"({ratio:.0%} — on target)"
                    )

    # ══════════════════════════════════════════════════════════════
    # HOURS TRACKING
    # ══════════════════════════════════════════════════════════════
    n.section("Hours Tracking")

    total_estimated = df["estimate_hours"].sum()
    total_actual = df["actual_hours"].sum()
    remaining_est = df[df["status"].isin(["pending", "blocked"])]["estimate_hours"].sum()

    n.metric_row(
        [
            {"label": "Total Estimated", "value": f"{total_estimated}h"},
            {"label": "Hours Logged", "value": f"{total_actual}h"},
            {"label": "Remaining (est)", "value": f"{remaining_est}h"},
        ]
    )

    n.change("Hours Burned", total_actual, total_estimated, fmt=".0f", pct=True)

    if HAS_MPL:
        fig, ax = plt.subplots(figsize=(8, 4))
        members = team["assignee"].tolist()
        x_pos = range(len(members))
        width = 0.35
        ax.bar([x - width / 2 for x in x_pos], team["estimated"], width, label="Estimated", color="#94a3b8")
        ax.bar([x + width / 2 for x in x_pos], team["actual"], width, label="Actual", color="#2563eb")
        ax.set_xticks(list(x_pos))
        ax.set_xticklabels(members, rotation=30, ha="right")
        ax.set_ylabel("Hours")
        ax.set_title("Estimated vs Actual Hours by Team Member")
        ax.legend()
        ax.grid(True, alpha=0.3, axis="y")
        fig.tight_layout()
        n.figure(fig, "hours_comparison.png", caption="Estimated vs actual hours per team member")
        plt.close(fig)

    # ══════════════════════════════════════════════════════════════
    # RISKS & BLOCKERS
    # ══════════════════════════════════════════════════════════════
    n.section("Risks & Blockers")

    blocked_tasks = df[df["status"] == "blocked"]
    if len(blocked_tasks) > 0:
        for _, task in blocked_tasks.iterrows():
            n.error(f"**BLOCKED** — {task['task_id']}: {task['title']} (assigned to {task['assignee']})")
    else:
        n.success("No blocked tasks.")

    high_prio_pending = df[(df["priority"] == "high") & (df["status"].isin(["pending", "blocked"]))]
    if len(high_prio_pending) > 0:
        n.warning(f"{len(high_prio_pending)} high-priority tasks are not yet started or blocked:")
        n.table(
            high_prio_pending[["task_id", "title", "assignee", "status"]],
            name="At-Risk High-Priority Tasks",
        )

    # ══════════════════════════════════════════════════════════════
    # DATA EXPORT
    # ══════════════════════════════════════════════════════════════
    n.section("Data Export")
    n.export_csv(df, "tasks_full.csv", name="Full task list")
    n.export_csv(team, "team_workload.csv", name="Team workload summary")
    n.connection_status("Jira", status="connected", details="Project: DEMO-2026")
    n.success("Status report generation complete.")

    out = n.save()
    print(f"Report saved to: {out}")


if __name__ == "__main__":
    main()
