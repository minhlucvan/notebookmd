"""Data Exploration Demo — notebookmd

Explores a sample employee dataset with:
- Summary statistics and shape info
- Department and role breakdowns
- Salary distributions and comparisons
- Collapsible deep-dives with expanders
- Filtered views and pivot tables
- CSV export for further analysis

Run:
    cd examples/data-exploration
    python run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from notebookmd import nb, NotebookConfig

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
    cfg = NotebookConfig(max_table_rows=25)
    n = nb(HERE / "README.md", title="Employee Data Exploration", cfg=cfg)

    if not HAS_PANDAS:
        n.warning("pandas is required for this demo. Install with: `pip install 'notebookmd[pandas]'`")
        n.save()
        return

    # ── Load Data ──
    df = pd.read_csv(HERE / "data" / "employees.csv", parse_dates=["hire_date"])

    # ══════════════════════════════════════════════════════════════
    # DATASET OVERVIEW
    # ══════════════════════════════════════════════════════════════
    n.section("Dataset Overview")
    n.write(f"Exploring a sample dataset of **{len(df)} employees** across multiple departments.")

    n.kv(
        {
            "Rows": str(len(df)),
            "Columns": str(len(df.columns)),
            "Departments": str(df["department"].nunique()),
            "Cities": str(df["city"].nunique()),
            "Date Range": f"{df['hire_date'].min():%Y-%m-%d} to {df['hire_date'].max():%Y-%m-%d}",
        },
        title="Dataset Shape",
    )

    n.subheader("Full Dataset")
    n.dataframe(df, name="Employee Directory")

    n.subheader("Statistical Summary")
    n.summary(df[["salary", "performance_score", "years_experience"]], title="Numeric Columns")

    # ══════════════════════════════════════════════════════════════
    # DEPARTMENT ANALYSIS
    # ══════════════════════════════════════════════════════════════
    n.section("Department Analysis")

    dept_summary = (
        df.groupby("department")
        .agg(
            headcount=("emp_id", "count"),
            avg_salary=("salary", "mean"),
            avg_performance=("performance_score", "mean"),
            avg_experience=("years_experience", "mean"),
        )
        .round(1)
        .sort_values("headcount", ascending=False)
        .reset_index()
    )
    dept_summary["avg_salary"] = dept_summary["avg_salary"].apply(lambda x: f"${x:,.0f}")
    n.table(dept_summary, name="Department Summary")

    tabs = n.tabs(["Engineering", "Product", "Design", "Sales", "Other"])

    for dept in ["Engineering", "Product", "Design", "Sales"]:
        with tabs.tab(dept):
            dept_df = df[df["department"] == dept]
            n.stats([
                {"label": "Headcount", "value": str(len(dept_df))},
                {"label": "Avg Salary", "value": f"${dept_df['salary'].mean():,.0f}"},
                {"label": "Avg Score", "value": f"{dept_df['performance_score'].mean():.1f}"},
            ])
            n.table(
                dept_df[["name", "title", "salary", "performance_score", "city"]],
                name=f"{dept} Team",
            )

    with tabs.tab("Other"):
        other = df[~df["department"].isin(["Engineering", "Product", "Design", "Sales"])]
        n.table(
            other[["name", "department", "title", "salary"]],
            name="Other Departments",
        )

    if HAS_MPL:
        fig, ax = plt.subplots(figsize=(8, 4))
        dept_counts = df["department"].value_counts()
        ax.barh(dept_counts.index, dept_counts.values, color="#7c3aed")
        ax.set_xlabel("Headcount")
        ax.set_title("Headcount by Department")
        ax.grid(True, alpha=0.3, axis="x")
        fig.tight_layout()
        n.figure(fig, "dept_headcount.png", caption="Employee distribution across departments")
        plt.close(fig)

    # ══════════════════════════════════════════════════════════════
    # SALARY ANALYSIS
    # ══════════════════════════════════════════════════════════════
    n.section("Salary Analysis")

    n.metric_row(
        [
            {"label": "Median Salary", "value": f"${df['salary'].median():,.0f}"},
            {"label": "Mean Salary", "value": f"${df['salary'].mean():,.0f}"},
            {"label": "Min", "value": f"${df['salary'].min():,.0f}"},
            {"label": "Max", "value": f"${df['salary'].max():,.0f}"},
        ]
    )

    # Salary by department
    salary_by_dept = (
        df.groupby("department")["salary"]
        .agg(["mean", "median", "min", "max"])
        .round(0)
        .sort_values("mean", ascending=False)
        .reset_index()
    )
    salary_by_dept.columns = ["Department", "Mean", "Median", "Min", "Max"]
    n.table(salary_by_dept, name="Salary by Department")

    if HAS_MPL:
        fig, ax = plt.subplots(figsize=(10, 4))
        departments = df["department"].unique()
        salary_data = [df[df["department"] == d]["salary"].values for d in departments]
        bp = ax.boxplot(salary_data, labels=departments, patch_artist=True)
        colors = ["#2563eb", "#7c3aed", "#059669", "#dc2626", "#f59e0b", "#6366f1", "#0891b2"]
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
        ax.set_ylabel("Salary ($)")
        ax.set_title("Salary Distribution by Department")
        ax.grid(True, alpha=0.3, axis="y")
        fig.tight_layout()
        n.figure(fig, "salary_distribution.png", caption="Box plot of salary ranges across departments")
        plt.close(fig)

    # ══════════════════════════════════════════════════════════════
    # PERFORMANCE ANALYSIS
    # ══════════════════════════════════════════════════════════════
    n.section("Performance Analysis")

    # Top performers
    top = df.nlargest(5, "performance_score")
    n.subheader("Top 5 Performers")
    n.table(
        top[["name", "department", "title", "performance_score", "salary"]],
        name="Top Performers",
    )

    for i, row in top.iterrows():
        n.ranking(
            row["name"],
            row["performance_score"],
            rank=list(top.index).index(i) + 1,
            total=len(df),
            fmt=".1f",
        )

    # Performance vs salary correlation
    with n.expander("Performance vs Salary", expanded=True):
        n.write("Examining the relationship between performance scores and compensation.")

        if HAS_MPL:
            fig, ax = plt.subplots(figsize=(8, 5))
            scatter = ax.scatter(
                df["years_experience"],
                df["salary"],
                c=df["performance_score"],
                cmap="RdYlGn",
                s=80,
                alpha=0.8,
                edgecolors="white",
                linewidth=0.5,
            )
            plt.colorbar(scatter, ax=ax, label="Performance Score")
            ax.set_xlabel("Years of Experience")
            ax.set_ylabel("Salary ($)")
            ax.set_title("Salary vs Experience (colored by Performance)")
            ax.grid(True, alpha=0.3)
            fig.tight_layout()
            n.figure(fig, "perf_vs_salary.png", caption="Each dot represents an employee")
            plt.close(fig)

    # ══════════════════════════════════════════════════════════════
    # REMOTE WORK ANALYSIS
    # ══════════════════════════════════════════════════════════════
    n.section("Remote Work")

    remote_counts = df["remote"].value_counts()
    remote_pct = remote_counts.get("yes", 0) / len(df) * 100
    n.stat("Remote Workers", f"{remote_counts.get('yes', 0)}/{len(df)}", description=f"{remote_pct:.0f}% of workforce")

    remote_salary = df.groupby("remote")["salary"].mean()
    n.kv(
        {f"Remote = {k}": f"${v:,.0f}" for k, v in remote_salary.items()},
        title="Average Salary by Work Mode",
    )

    remote_by_dept = pd.crosstab(df["department"], df["remote"])
    n.table(remote_by_dept.reset_index(), name="Remote Distribution by Department")

    # ══════════════════════════════════════════════════════════════
    # CITY BREAKDOWN
    # ══════════════════════════════════════════════════════════════
    n.section("City Breakdown")

    city_summary = (
        df.groupby("city")
        .agg(
            headcount=("emp_id", "count"),
            avg_salary=("salary", "mean"),
            remote_pct=("remote", lambda x: (x == "yes").mean() * 100),
        )
        .round(1)
        .sort_values("headcount", ascending=False)
        .reset_index()
    )
    city_summary["avg_salary"] = city_summary["avg_salary"].apply(lambda x: f"${x:,.0f}")
    city_summary["remote_pct"] = city_summary["remote_pct"].apply(lambda x: f"{x:.0f}%")
    n.table(city_summary, name="Employees by City")

    # ══════════════════════════════════════════════════════════════
    # DATA EXPORT
    # ══════════════════════════════════════════════════════════════
    n.section("Data Export")
    n.export_csv(df, "employees_full.csv", name="Full employee dataset")
    n.export_csv(dept_summary, "department_summary.csv", name="Department summary")
    n.success("Data exploration complete.")

    out = n.save()
    print(f"Report saved to: {out}")


if __name__ == "__main__":
    main()
