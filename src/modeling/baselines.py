"""Baseline model definitions."""

from sklearn.dummy import DummyClassifier


def majority_baseline() -> DummyClassifier:
    """Return a simple most-frequent baseline classifier."""
    return DummyClassifier(strategy="most_frequent")
