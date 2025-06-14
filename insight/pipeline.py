"""Minimal data pipeline with caching."""

from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt
from . import cache_utils


@cache_utils.cache_with_versions
def build_figures(df: pd.DataFrame, _lib_versions=None):
    """Generate simple plot from dataframe."""
    fig, ax = plt.subplots()
    if hasattr(df, "plot"):
        df.plot(ax=ax)
    ax.set_title("Data plot")
    return [fig]


@cache_utils.cache_with_versions
def maybe_forecast(df: pd.DataFrame, _lib_versions=None) -> pd.DataFrame:
    """Placeholder forecasting step returning dataframe unmodified."""
    # Real implementation would forecast future values
    return df


@cache_utils.cache_with_versions
def write_narrative(df: pd.DataFrame, _lib_versions=None) -> str:
    """Return short narrative about dataframe."""
    return f"Data has {len(df)} rows and {len(df.columns)} columns."
