from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate_dataset(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    students_per_team = 5
    team_count = 8
    total_students = students_per_team * team_count

    names = [
        "Aarav", "Diya", "Ishan", "Meera", "Rohan", "Anaya", "Kabir", "Sneha", "Vihaan", "Nisha",
        "Arjun", "Kavya", "Dev", "Pooja", "Manav", "Ira", "Ayaan", "Neha", "Yash", "Ritika",
        "Aditya", "Saanvi", "Reyansh", "Maya", "Tanvi", "Harsh", "Riya", "Parth", "Ishita", "Karan",
        "Nandini", "Rahul", "Aditi", "Om", "Priya", "Siddharth", "Tara", "Varun", "Zara", "Krish",
    ]

    rows = []
    for i in range(total_students):
        student_id = f"S{i+1:03d}"
        student_name = names[i]
        team_id = f"T{(i // students_per_team) + 1:02d}"

        tasks_assigned = int(rng.integers(6, 15))
        completion_ratio = float(np.clip(rng.normal(0.78, 0.15), 0.35, 1.0))
        tasks_completed = int(np.clip(round(tasks_assigned * completion_ratio), 1, tasks_assigned))

        avg_task_hours = float(np.clip(rng.normal(5.0, 1.6), 2.0, 10.0))
        commits = int(np.clip(rng.normal(tasks_completed * 3.2, 6.0), 1, 90))
        prs_opened = int(np.clip(round(commits / rng.uniform(2.0, 4.0)), 1, 30))
        prs_merged = int(np.clip(prs_opened - rng.integers(0, 4), 0, prs_opened))
        code_lines_changed = int(np.clip(rng.normal(commits * 22, 220), 50, 5000))

        meetings_attended = int(rng.integers(4, 11))
        total_meetings = 10

        # Base contribution proxy for peer rating generation
        base_proxy = (
            0.30 * (tasks_completed / tasks_assigned)
            + 0.20 * min(commits / 50, 1)
            + 0.20 * min(prs_merged / 20, 1)
            + 0.15 * min(code_lines_changed / 2000, 1)
            + 0.15 * (meetings_attended / total_meetings)
        )
        peer_rating = float(np.clip(2.0 + 3.0 * base_proxy + rng.normal(0.0, 0.55), 1.0, 5.0))

        # Weekly progress (%)
        week1 = int(np.clip(rng.normal(20, 8), 5, 40))
        week2 = int(np.clip(week1 + rng.normal(18, 7), 20, 65))
        week3 = int(np.clip(week2 + rng.normal(20, 7), 35, 90))
        week4 = int(np.clip(week3 + rng.normal(15, 8), 55, 100))

        rows.append(
            {
                "student_id": student_id,
                "student_name": student_name,
                "team_id": team_id,
                "tasks_assigned": tasks_assigned,
                "tasks_completed": tasks_completed,
                "avg_task_hours": round(avg_task_hours, 2),
                "commits": commits,
                "prs_opened": prs_opened,
                "prs_merged": prs_merged,
                "code_lines_changed": code_lines_changed,
                "peer_rating": round(peer_rating, 2),
                "meetings_attended": meetings_attended,
                "total_meetings": total_meetings,
                "week1_progress": week1,
                "week2_progress": week2,
                "week3_progress": week3,
                "week4_progress": week4,
            }
        )

    df = pd.DataFrame(rows)

    # Inject a few missing values to demonstrate data cleaning workflow
    missing_idx = rng.choice(df.index, size=5, replace=False)
    df.loc[missing_idx[:2], "peer_rating"] = np.nan
    df.loc[missing_idx[2:4], "code_lines_changed"] = np.nan
    df.loc[missing_idx[4:], "meetings_attended"] = np.nan

    return df


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    raw_dir = project_root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    out_file = raw_dir / "student_project_activity.csv"
    df = generate_dataset(seed=42)
    df.to_csv(out_file, index=False)
    print(f"Created dataset: {out_file}")
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")


if __name__ == "__main__":
    main()
