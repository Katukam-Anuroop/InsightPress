from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Dict, Any

import matplotlib.pyplot as plt
import pandas as pd


def _plot(ax: plt.Axes, df: pd.DataFrame, plan: Dict[str, Any]) -> None:
    """Create a plot on ``ax`` based on ``plan`` specifications."""
    kind = plan.get("kind", "line")
    x = plan.get("x")
    y = plan.get("y")

    if kind == "line":
        if x is not None and y is not None:
            ax.plot(df[x], df[y])
        elif y is not None:
            ax.plot(df[y])
        else:
            raise ValueError("Line plot requires 'y' or both 'x' and 'y'")
    elif kind == "bar":
        if y is None:
            raise ValueError("Bar plot requires 'y' column")
        ax.bar(df[x] if x else df.index, df[y])
    elif kind == "scatter":
        if x is None or y is None:
            raise ValueError("Scatter plot requires 'x' and 'y'")
        ax.scatter(df[x], df[y])
    elif kind == "hist":
        column = y if y is not None else x
        if column is None:
            raise ValueError("Hist plot requires 'x' or 'y'")
        ax.hist(df[column].dropna())
    else:
        raise ValueError(f"Unsupported plot kind: {kind}")

    if "title" in plan:
        ax.set_title(plan["title"])
    if x is not None:
        ax.set_xlabel(plan.get("xlabel", x))
    if y is not None:
        ax.set_ylabel(plan.get("ylabel", y))


def build_figures(df: pd.DataFrame, plans: Iterable[Dict[str, Any]], out_dir: Path) -> List[Path]:
    """Build figures from ``plans`` and save them to ``out_dir``.

    Parameters
    ----------
    df:
        DataFrame containing the data to plot.
    plans:
        Iterable of plot specifications. Supported keys for each plan are::

            kind:     One of ``line``, ``bar``, ``scatter`` or ``hist``.
            x:        Column name for the x-axis.
            y:        Column name for the y-axis.
            title:    Title of the chart.
            xlabel:   Label for the x-axis.
            ylabel:   Label for the y-axis.
            filename: Name of the output PNG file.
    out_dir:
        Directory in which the figures will be written.

    Returns
    -------
    List[Path]
        Paths to the created figure files.
    """
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    saved_paths: List[Path] = []
    for i, plan in enumerate(plans):
        fig, ax = plt.subplots()
        _plot(ax, df, plan)
        plt.tight_layout()

        filename = plan.get("filename", f"figure_{i}.png")
        file_path = out_path / filename
        fig.savefig(file_path, dpi=300)
        plt.close(fig)
        saved_paths.append(file_path)

    return saved_paths
