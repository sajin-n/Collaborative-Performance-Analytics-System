import pandas as pd
import numpy as np
from pathlib import Path

PROCESSED_DIR = Path("D:/projects/Sprint3project/data/processed")


def normalize_column(series):
    min_val, max_val = series.min(), series.max()
    if max_val == min_val:
        return series * 0 + 50
    return (series - min_val) / (max_val - min_val)


def calculate_contribution_score(df):
    df = df.copy()

    task_norm = normalize_column(df["completion_rate"])
    git_norm = normalize_column(
        df["commits"] + df["prs_merged"] + df["code_lines_changed"] / 100
    )
    peer_norm = normalize_column(df["peer_rating"])
    attendance_norm = normalize_column(df["attendance_rate"])
    progress_norm = normalize_column(df["week4_progress"])

    df["contribution_score"] = (
        task_norm * 25
        + git_norm * 25
        + peer_norm * 20
        + attendance_norm * 15
        + progress_norm * 15
    ).clip(0, 100)

    return df


def calculate_team_metrics(df):
    team_stats = (
        df.groupby("team_id")
        .agg(
            {
                "contribution_score": ["mean", "std", "min", "max"],
                "peer_rating": "mean",
                "completion_rate": "mean",
                "attendance_rate": "mean",
                "week4_progress": "mean",
            }
        )
        .reset_index()
    )

    team_stats.columns = [
        "team_id",
        "avg_contribution",
        "std_contribution",
        "min_contribution",
        "max_contribution",
        "avg_peer_rating",
        "avg_completion_rate",
        "avg_attendance",
        "avg_progress",
    ]

    team_metrics = team_stats.copy()
    team_metrics["contribution_range"] = (
        team_metrics["max_contribution"] - team_metrics["min_contribution"]
    )

    team_metrics["team_balance_score"] = (
        100 - normalize_column(team_metrics["std_contribution"]) * 100
    ).clip(0, 100)

    team_metrics["team_performance_score"] = (
        normalize_column(team_metrics["avg_progress"]) * 40
        + normalize_column(team_metrics["avg_completion_rate"]) * 30
        + normalize_column(team_metrics["avg_peer_rating"]) * 30
    ).clip(0, 100)

    team_metrics["team_strength"] = team_metrics["team_performance_score"].apply(
        lambda x: "Strong" if x >= 75 else ("Medium" if x >= 50 else "Weak")
    )

    return df, team_metrics


def identify_at_risk_students(df):
    df = df.copy()
    df["at_risk"] = (
        (df["contribution_score"] < 40)
        | (df["attendance_rate"] < 0.5)
        | (df["completion_rate"] < 0.5)
    )
    df["risk_reason"] = ""
    df.loc[df["contribution_score"] < 40, "risk_reason"] += "Low Contribution; "
    df.loc[df["attendance_rate"] < 0.5, "risk_reason"] += "Low Attendance; "
    df.loc[df["completion_rate"] < 0.5, "risk_reason"] += "Low Task Completion; "
    df["risk_reason"] = df["risk_reason"].str.strip("; ")

    return df


def generate_insights(df, team_metrics):
    insights = []

    high_contributors = df.nlargest(5, "contribution_score")[
        ["student_name", "contribution_score"]
    ]
    insights.append(
        f"Top contributors: {', '.join(high_contributors['student_name'].tolist())}"
    )

    low_contributors = df.nsmallest(5, "contribution_score")[
        ["student_name", "contribution_score"]
    ]
    insights.append(
        f"Needs attention: {', '.join(low_contributors['student_name'].tolist())}"
    )

    strong_teams = team_metrics[team_metrics["team_strength"] == "Strong"][
        "team_id"
    ].tolist()
    weak_teams = team_metrics[team_metrics["team_strength"] == "Weak"][
        "team_id"
    ].tolist()
    insights.append(
        f"Strong teams: {', '.join(strong_teams) if strong_teams else 'None'}"
    )
    insights.append(f"Weak teams: {', '.join(weak_teams) if weak_teams else 'None'}")

    at_risk_count = df["at_risk"].sum()
    insights.append(f"At-risk students: {at_risk_count}")

    return insights


def run_analysis():
    df = pd.read_csv(PROCESSED_DIR / "cleaned_data.csv")

    df = calculate_contribution_score(df)
    df, team_metrics = calculate_team_metrics(df)
    df = identify_at_risk_students(df)

    df.to_csv(PROCESSED_DIR / "student_scores.csv", index=False)
    team_metrics.to_csv(PROCESSED_DIR / "team_metrics.csv", index=False)

    insights = generate_insights(df, team_metrics)
    print("=== ANALYSIS RESULTS ===")
    for insight in insights:
        print(insight)

    return df, team_metrics, insights


if __name__ == "__main__":
    run_analysis()
