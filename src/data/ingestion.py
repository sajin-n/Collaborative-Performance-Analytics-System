"""Data ingestion utilities."""

from pathlib import Path
import pandas as pd


def read_csv(path: Path) -> pd.DataFrame:
    """Read a CSV file into a DataFrame."""
    return pd.read_csv(path)
