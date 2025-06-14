from __future__ import annotations

from typing import Any, Dict

import numpy as np
import numpy.typing as npt
import pandas as pd

__all__ = ["profile_df"]


def profile_df(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """Profile a dataframe column-wise.

    Parameters
    ----------
    df:
        DataFrame to profile.

    Returns
    -------
    Dict[str, Dict[str, Any]]
        A dictionary keyed by column name containing profile information.
    """
    profile: Dict[str, Dict[str, Any]] = {}
    for col in df.columns:
        series = df[col]
        info: Dict[str, Any] = {
            "dtype": str(series.dtype),
            "pct_null": float(series.isna().mean() * 100),
            "n_unique": int(series.nunique(dropna=True)),
            "example_values": series.dropna().unique()[:3].tolist(),
        }

        if pd.api.types.is_numeric_dtype(series):
            values: npt.NDArray[np.float_] = series.dropna().to_numpy(dtype=float)
            if values.size:
                info.update(
                    mean=float(values.mean()),
                    std=float(values.std(ddof=1)) if values.size > 1 else float("nan"),
                    min=float(values.min()),
                    max=float(values.max()),
                )
            else:
                info.update(mean=np.nan, std=np.nan, min=np.nan, max=np.nan)

        if pd.api.types.is_datetime64_any_dtype(series):
            if series.notna().any():
                span_days = (series.max() - series.min()).days
            else:
                span_days = np.nan
            info["span_days"] = float(span_days) if span_days == span_days else np.nan

        profile[col] = info

    return profile
