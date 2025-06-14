from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import pmdarima as pm


def maybe_forecast(df: pd.DataFrame, out_dir: str | Path) -> Optional[Path]:
    """Forecast a univariate time series if conditions are met.

    Parameters
    ----------
    df:
        Input dataframe with a datetime index and one numeric column.
    out_dir:
        Directory to save the forecast plot.

    Returns
    -------
    Optional[Path]
        Path to the saved plot, or ``None`` if forecasting was skipped.
    """
    if not (
        pd.api.types.is_datetime64_any_dtype(df.index)
        and len(df) > 30
        and df.select_dtypes("number").shape[1] == 1
    ):
        return None

    series = df[df.select_dtypes("number").columns[0]]

    model = pm.auto_arima(series)
    forecast, confint = model.predict(90, return_conf_int=True)

    freq = series.index.freq or pd.infer_freq(series.index)
    if freq is None:
        return None

    forecast_index = pd.date_range(series.index[-1], periods=91, freq=freq)[1:]

    plt.figure(figsize=(10, 6))
    plt.plot(series.index, series.values, label="Actual")
    plt.plot(forecast_index, forecast, label="Forecast")
    plt.fill_between(
        forecast_index,
        confint[:, 0],
        confint[:, 1],
        color="orange",
        alpha=0.3,
        label="Prediction Interval",
    )
    plt.legend()
    plt.tight_layout()

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "forecast.png"
    plt.savefig(path)
    plt.close()

    return path
