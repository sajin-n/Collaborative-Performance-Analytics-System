"""Feature preparation helpers for modeling."""

import pandas as pd


def split_features_target(df: pd.DataFrame, target: str):
    """Split a dataframe into X and y components."""
    X = df.drop(columns=[target])
    y = df[target]
    return X, y
