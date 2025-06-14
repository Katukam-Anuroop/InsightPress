import sys, os
venv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'.venv','lib','python3.11','site-packages')
if os.path.exists(venv_path):
    sys.path.insert(0, venv_path)
import pandas as pd
import matplotlib.figure
from insight import profiler, chart_planner, forecaster, insight_writer


def test_basic_profiling_output():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    profile = profiler.basic_profile(df)
    assert "a" in profile
    assert profile["a"]["mean"] == 2.0


def test_chart_generation_returns_matplotlib_object():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})
    fig = chart_planner.line_chart(df, "x", "y")
    assert isinstance(fig, matplotlib.figure.Figure)


def test_forecasting_produces_numeric_predictions():
    series = pd.Series([1, 2, 3, 4, 5])
    preds = forecaster.simple_forecast(series, steps=2)
    assert len(preds) == 2
    assert all(isinstance(v, (int, float)) for v in preds)


def test_narrative_includes_statistics():
    df = pd.DataFrame({"value": [1, 3, 5]})
    text = insight_writer.narrative(df, "value")
    assert "average value is" in text
    assert "median is" in text
