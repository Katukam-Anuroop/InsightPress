import pandas as pd


def basic_profile(df: pd.DataFrame) -> dict:
    """Return basic descriptive statistics for the given DataFrame."""
    desc = df.describe(include='all')
    return desc.to_dict()
