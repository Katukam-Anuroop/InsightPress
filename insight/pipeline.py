from __future__ import annotations

from pathlib import Path
from typing import Any, List

import matplotlib.pyplot as plt
import pandas as pd

from .config import Config


def profile(infile: Path, cfg: Config) -> pd.DataFrame:
    """Load the input file as a dataframe."""
    df = pd.read_csv(infile)
    return df


def plan_charts(df: pd.DataFrame, cfg: Config) -> List[dict[str, Any]]:
    """Plan charts based on numeric columns."""
    charts = []
    for col in df.select_dtypes(include="number").columns:
        charts.append({"column": col, "type": "hist"})
    return charts


def build_figures(df: pd.DataFrame, plan: List[dict[str, Any]], cfg: Config) -> List[Path]:
    """Build figures from the chart plan."""
    output_dir = Path(cfg.cache_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for spec in plan:
        fig, ax = plt.subplots()
        if spec["type"] == "hist":
            df[spec["column"]].plot.hist(ax=ax)
        ax.set_title(spec["column"])
        path = output_dir / f"{spec['column']}.png"
        fig.savefig(path, dpi=cfg.dpi)
        plt.close(fig)
        paths.append(path)
    return paths


def maybe_forecast(df: pd.DataFrame, cfg: Config) -> dict[str, float]:
    """Return simple mean forecast for numeric columns."""
    return df.mean(numeric_only=True).to_dict()


def write_narrative(df: pd.DataFrame, forecast: dict[str, float], cfg: Config) -> str:
    """Generate a simple narrative summary."""
    summary = [
        f"Dataset has {len(df)} rows and {len(df.columns)} columns.",
    ]
    if forecast:
        summary.append("Column means: " + ", ".join(f"{k}={v:.2f}" for k, v in forecast.items()))
    return "\n".join(summary)


def compose_pdf(figures: List[Path], narrative: str, outfile: Path, cfg: Config) -> None:
    """Compose the PDF report from figures and narrative."""
    from matplotlib.backends.backend_pdf import PdfPages

    with PdfPages(outfile) as pdf:
        # narrative page
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        ax.text(0.05, 0.95, narrative, va="top", wrap=True)
        pdf.savefig(fig)
        plt.close(fig)

        for img_path in figures:
            img = plt.imread(img_path)
            fig, ax = plt.subplots()
            ax.imshow(img)
            ax.axis("off")
            pdf.savefig(fig)
            plt.close(fig)


def run_pipeline(infile: Path, outfile: Path, cfg: Config | None = None) -> None:
    """Run the insight pipeline."""
    cfg = cfg or Config()
    df = profile(infile, cfg)
    plan = plan_charts(df, cfg)
    figs = build_figures(df, plan, cfg)
    forecast = maybe_forecast(df, cfg)
    narrative = write_narrative(df, forecast, cfg)
    compose_pdf(figs, narrative, outfile, cfg)
