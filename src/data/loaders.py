"""Dataset loader functions."""

from pathlib import Path
import pandas as pd


def load_table(raw_dir: Path, file_name: str) -> pd.DataFrame:
    """Load a named CSV table from the raw data directory."""
    return pd.read_csv(raw_dir / file_name)
