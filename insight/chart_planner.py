import pandas as pd
import matplotlib.pyplot as plt


def line_chart(df: pd.DataFrame, x: str, y: str):
    """Return a matplotlib Figure with a simple line plot."""
    fig, ax = plt.subplots()
    ax.plot(df[x], df[y])
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    return fig
