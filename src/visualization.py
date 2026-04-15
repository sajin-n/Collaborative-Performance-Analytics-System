import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

PROCESSED_DIR = Path("D:/projects/Sprint3project/data/processed")
OUTPUT_DIR = Path("D:/projects/Sprint3project/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")
COLORS = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B", "#44AF69"]


def plot_contribution_scores(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    df_sorted = df.sort_values("contribution_score", ascending=True)
    colors = [
        COLORS[0] if x >= 60 else COLORS[2] if x >= 40 else COLORS[3]
        for x in df_sorted["contribution_score"]
    ]
    ax.barh(df_sorted["student_name"], df_sorted["contribution_score"], color=colors)
    ax.set_xlabel("Contribution Score")
    ax.set_title("Individual Contribution Scores")
    ax.axvline(x=60, color="green", linestyle="--", alpha=0.7, label="Good (≥60)")
    ax.axvline(x=40, color="orange", linestyle="--", alpha=0.7, label="Warning (≥40)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "contribution_scores.png", dpi=150)
    plt.close()


def plot_team_performance(team_metrics):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    colors = [
        COLORS[0] if x == "Strong" else COLORS[2] if x == "Medium" else COLORS[3]
        for x in team_metrics["team_strength"]
    ]
    axes[0].bar(
        team_metrics["team_id"], team_metrics["team_performance_score"], color=colors
    )
    axes[0].set_xlabel("Team ID")
    axes[0].set_ylabel("Performance Score")
    axes[0].set_title("Team Performance Scores")
    axes[0].axhline(y=75, color="green", linestyle="--", alpha=0.7)
    axes[0].axhline(y=50, color="orange", linestyle="--", alpha=0.7)

    axes[1].bar(
        team_metrics["team_id"], team_metrics["team_balance_score"], color=COLORS[0]
    )
    axes[1].set_xlabel("Team ID")
    axes[1].set_ylabel("Balance Score")
    axes[1].set_title("Team Balance Scores")
    axes[1].axhline(y=70, color="green", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "team_performance.png", dpi=150)
    plt.close()


def plot_team_distribution(df):
    team_stats = (
        df.groupby("team_id")
        .agg(
            {
                "contribution_score": "mean",
                "peer_rating": "mean",
                "completion_rate": "mean",
            }
        )
        .reset_index()
    )

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].pie(
        team_stats.groupby("team_id").size(),
        labels=team_stats["team_id"],
        autopct="%1.0f%%",
        colors=COLORS[: len(team_stats)],
    )
    axes[0].set_title("Teams Distribution")

    axes[1].bar(
        team_stats["team_id"], team_stats["contribution_score"], color=COLORS[0]
    )
    axes[1].set_title("Avg Contribution by Team")
    axes[1].set_xlabel("Team ID")

    axes[2].scatter(
        team_stats["peer_rating"],
        team_stats["contribution_score"],
        c=range(len(team_stats)),
        cmap="viridis",
        s=100,
    )
    axes[2].set_xlabel("Peer Rating")
    axes[2].set_ylabel("Contribution Score")
    axes[2].set_title("Peer Rating vs Contribution")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "team_distribution.png", dpi=150)
    plt.close()


def plot_progress_trends(df):
    progress_cols = [
        "week1_progress",
        "week2_progress",
        "week3_progress",
        "week4_progress",
    ]
    week_labels = ["Week 1", "Week 2", "Week 3", "Week 4"]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    top_5 = df.nlargest(5, "contribution_score")
    for idx, row in top_5.iterrows():
        axes[0].plot(
            week_labels,
            [row[c] for c in progress_cols],
            marker="o",
            label=row["student_name"],
        )
    axes[0].set_xlabel("Week")
    axes[0].set_ylabel("Progress %")
    axes[0].set_title("Progress Trends - Top Contributors")
    axes[0].legend(loc="upper left", fontsize=8)

    bottom_5 = df.nsmallest(5, "contribution_score")
    for idx, row in bottom_5.iterrows():
        axes[1].plot(
            week_labels,
            [row[c] for c in progress_cols],
            marker="o",
            label=row["student_name"],
        )
    axes[1].set_xlabel("Week")
    axes[1].set_ylabel("Progress %")
    axes[1].set_title("Progress Trends - Needs Attention")
    axes[1].legend(loc="upper left", fontsize=8)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "progress_trends.png", dpi=150)
    plt.close()


def plot_correlation_matrix(df):
    numeric_cols = [
        "contribution_score",
        "completion_rate",
        "commits",
        "prs_merged",
        "code_lines_changed",
        "peer_rating",
        "attendance_rate",
        "week4_progress",
    ]
    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f", ax=ax)
    ax.set_title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "correlation_matrix.png", dpi=150)
    plt.close()


def plot_at_risk_analysis(df):
    at_risk = df[df["at_risk"] == True]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    risk_counts = at_risk["risk_reason"].value_counts()
    axes[0].pie(
        risk_counts.values,
        labels=risk_counts.index,
        autopct="%1.0f%%",
        colors=COLORS[: len(risk_counts)],
    )
    axes[0].set_title("Risk Factors Distribution")

    score_dist = [
        len(df[df["contribution_score"] >= 60]),
        len(df[(df["contribution_score"] >= 40) & (df["contribution_score"] < 60)]),
        len(df[df["contribution_score"] < 40]),
    ]
    labels = ["Good (≥60)", "Warning (40-59)", "At Risk (<40)"]
    axes[1].bar(labels, score_dist, color=[COLORS[0], COLORS[2], COLORS[3]])
    axes[1].set_xlabel("Category")
    axes[1].set_ylabel("Count")
    axes[1].set_title("Student Performance Distribution")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "at_risk_analysis.png", dpi=150)
    plt.close()


def create_summary_dashboard():
    df = pd.read_csv(PROCESSED_DIR / "student_scores.csv")
    team_metrics = pd.read_csv(PROCESSED_DIR / "team_metrics.csv")

    print("Generating visualizations...")

    plot_contribution_scores(df)
    plot_team_performance(team_metrics)
    plot_team_distribution(df)
    plot_progress_trends(df)
    plot_correlation_matrix(df)
    plot_at_risk_analysis(df)

    print(f"Visualizations saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    create_summary_dashboard()
