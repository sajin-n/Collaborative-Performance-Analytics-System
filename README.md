# Student Project Performance Analytics Dashboard

An assessment-ready data science mini-system for college project monitoring.

It helps administrators:
- measure student contribution objectively,
- detect team imbalance and delay risks,
- compare peer ratings against activity evidence,
- generate reproducible visual and tabular reports.

## Tech Stack

- Python 3.12+
- Pandas, NumPy
- Matplotlib, Seaborn, Plotly
- Jupyter Notebook

## Project Structure

- `data/raw/` – raw and source split CSVs
- `data/processed/` – scored/cleaned datasets
- `notebooks/` – analytics and dashboard notebooks
- `scripts/` – helper generators
- `outputs/graphs/` – exported charts
- `outputs/reports/` – exported summary reports

## Notebooks

1. `notebooks/01_student_performance_analytics.ipynb`
   - Complete pipeline: ingestion, cleaning, feature engineering, scoring, bias checks, EDA, exports, tests.

2. `notebooks/02_admin_dashboard.ipynb`
   - Compact demo dashboard with contributor, team health, and bias snapshots.

## Metrics Implemented

- **Contribution Score (0–100)**
  - Weighted mix of task completion, commits, PR merges, code churn, attendance, peer rating.

- **Team Balance Score (0–100)**
  - Based on contribution coefficient of variation within each team.

- **Team Performance Score**
  - Combined view of contribution, progress, and completion quality.

- **Bias Flag**
  - Flags mismatch between peer review score and activity-derived evidence.

## How to Run

1. Install dependencies from `requirements.txt`.
2. (Optional) regenerate sample dataset using `scripts/generate_sample_data.py`.
3. Run notebook 1 from top to bottom.
4. Run notebook 2 for admin-ready visuals.

## Expected Output Files

After running notebook 1 and 2:

- Processed CSVs:
  - `data/processed/student_scores.csv`
  - `data/processed/team_metrics.csv`

- Graphs:
  - `outputs/graphs/top_student_contributions.png`
  - `outputs/graphs/team_balance_scores.png`
  - `outputs/graphs/team_progress_trends.png`
  - `outputs/graphs/peer_vs_activity.png`
  - `outputs/graphs/dashboard_top10_contributors.png`
  - `outputs/graphs/dashboard_team_health.png`

- Reports:
  - `outputs/reports/evaluation_summary.csv`
  - `outputs/reports/final_summary_report.md`

## Current Verified Snapshot

- Students analyzed: **40**
- Teams analyzed: **8**
- Average contribution score: **54.37**
- Average team balance score: **72.73**
- At-risk teams flagged: **5**
- Potential peer-review bias cases: **9**
