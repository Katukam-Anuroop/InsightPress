import pandas as pd


def narrative(df: pd.DataFrame, column: str) -> str:
    """Generate a simple narrative text for the given column."""
    mean = df[column].mean()
    median = df[column].median()
    return f"The average {column} is {mean:.2f} and the median is {median:.2f}."
