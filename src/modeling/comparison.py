"""Model comparison utilities."""

import pandas as pd


def summarize_scores(results: dict[str, float]) -> pd.DataFrame:
    """Convert model score dictionary to sorted dataframe."""
    out = pd.DataFrame([{"model": k, "score": v} for k, v in results.items()])
    return out.sort_values("score", ascending=False).reset_index(drop=True)
