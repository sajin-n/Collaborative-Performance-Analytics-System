"""Cross-table comparison utilities."""

import pandas as pd


def compare_counts(left: pd.DataFrame, right: pd.DataFrame, key: str) -> pd.DataFrame:
    """Return basic key overlap diagnostics between two dataframes."""
    left_keys = set(left[key].dropna().unique())
    right_keys = set(right[key].dropna().unique())
    return pd.DataFrame(
        {
            "metric": ["left_only", "right_only", "intersection"],
            "value": [
                len(left_keys - right_keys),
                len(right_keys - left_keys),
                len(left_keys & right_keys),
            ],
        }
    )
