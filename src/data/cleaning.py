import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("D:/projects/Sprint3project/data/raw")
PROCESSED_DIR = Path("D:/projects/Sprint3project/data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_raw_data():
    student_info = pd.read_csv(DATA_DIR / "student_info.csv")
    task_logs = pd.read_csv(DATA_DIR / "task_logs.csv")
    git_activity = pd.read_csv(DATA_DIR / "git_activity.csv")
    peer_reviews = pd.read_csv(DATA_DIR / "peer_reviews.csv")
    attendance = pd.read_csv(DATA_DIR / "attendance.csv")
    progress = pd.read_csv(DATA_DIR / "progress.csv")
    return student_info, task_logs, git_activity, peer_reviews, attendance, progress


def clean_task_logs(df):
    df["completion_rate"] = df["tasks_completed"] / df["tasks_assigned"]
    df["avg_task_hours"] = df["avg_task_hours"].fillna(df["avg_task_hours"].median())
    return df


def clean_git_activity(df):
    df["code_lines_changed"] = df["code_lines_changed"].fillna(
        df["code_lines_changed"].median()
    )
    df["pr_success_rate"] = df["prs_merged"] / df["prs_opened"].replace(0, np.nan)
    df["pr_success_rate"] = df["pr_success_rate"].fillna(0)
    return df


def clean_peer_reviews(df):
    df["peer_rating"] = df["peer_rating"].fillna(df["peer_rating"].median())
    return df


def clean_attendance(df):
    df["meetings_attended"] = df["meetings_attended"].fillna(
        df["meetings_attended"].median()
    )
    df["attendance_rate"] = df["meetings_attended"] / df["total_meetings"]
    return df


def clean_progress(df):
    for col in ["week1_progress", "week2_progress", "week3_progress", "week4_progress"]:
        df[col] = df[col].fillna(df[col].median())
    df["progress_improvement"] = df["week4_progress"] - df["week1_progress"]
    return df


def merge_all_data(
    student_info, task_logs, git_activity, peer_reviews, attendance, progress
):
    df = student_info.copy()
    df = df.merge(task_logs, on="student_id", how="left")
    df = df.merge(git_activity, on="student_id", how="left")
    df = df.merge(peer_reviews, on="student_id", how="left")
    df = df.merge(attendance, on="student_id", how="left")
    df = df.merge(progress, on="student_id", how="left")
    return df


def clean_data():
    print("Loading raw data...")
    student_info, task_logs, git_activity, peer_reviews, attendance, progress = (
        load_raw_data()
    )

    print("Cleaning datasets...")
    task_logs = clean_task_logs(task_logs)
    git_activity = clean_git_activity(git_activity)
    peer_reviews = clean_peer_reviews(peer_reviews)
    attendance = clean_attendance(attendance)
    progress = clean_progress(progress)

    print("Merging all data...")
    merged_df = merge_all_data(
        student_info, task_logs, git_activity, peer_reviews, attendance, progress
    )

    print(f"Final dataset shape: {merged_df.shape}")
    print(f"Missing values:\n{merged_df.isnull().sum()}")

    merged_df.to_csv(PROCESSED_DIR / "cleaned_data.csv", index=False)
    print(f"Saved cleaned data to {PROCESSED_DIR / 'cleaned_data.csv'}")

    return merged_df


if __name__ == "__main__":
    clean_data()
