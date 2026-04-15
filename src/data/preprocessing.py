"""Data preprocessing helpers."""

import pandas as pd


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to lowercase snake-style text."""
    out = df.copy()
    out.columns = [c.strip().lower() for c in out.columns]
    return out
