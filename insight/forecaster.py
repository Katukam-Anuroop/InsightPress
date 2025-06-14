import numpy as np
import pandas as pd


def simple_forecast(series: pd.Series, steps: int = 1) -> np.ndarray:
    """Generate a naive linear forecast for the given series."""
    idx = np.arange(len(series))
    coeffs = np.polyfit(idx, series.values, 1)
    last_idx = len(series) - 1
    return np.array([coeffs[0] * (last_idx + i + 1) + coeffs[1] for i in range(steps)])
