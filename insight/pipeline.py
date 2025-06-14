from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


StageCallback = Callable[[str, int, int], None]


def run_pipeline(csv_path: Path, output_dir: Path, progress_callback: Optional[StageCallback] = None) -> Path:
    """Process ``csv_path`` and generate a simple PDF report.

    Parameters
    ----------
    csv_path:
        Path to the input CSV file.
    output_dir:
        Directory where the PDF report will be saved.
    progress_callback:
        Function invoked after each stage. It receives the stage name,
        the current stage index (0-based) and the total number of stages.

    Returns
    -------
    Path
        Path to the generated PDF file.
    """
    if progress_callback is None:
        progress_callback = lambda *args, **kwargs: None

    stages = [
        "load_data",
        "create_summary",
        "generate_plot",
        "write_pdf",
    ]
    total = len(stages)

    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / "report.pdf"

    # Stage 0: load_data
    progress_callback(stages[0], 0, total)
    df = pd.read_csv(csv_path)

    # Stage 1: create_summary
    progress_callback(stages[1], 1, total)
    summary = df.describe(include="all")

    # Stage 2: generate_plot
    progress_callback(stages[2], 2, total)
    fig, ax = plt.subplots(figsize=(8, 4))
    df.head().plot(ax=ax)
    plt.tight_layout()

    # Stage 3: write_pdf
    progress_callback(stages[3], 3, total)
    with PdfPages(pdf_path) as pdf:
        # Summary table page
        fig_summary, ax_summary = plt.subplots(figsize=(8.27, 11.69))
        ax_summary.axis("off")
        table = ax_summary.table(
            cellText=summary.round(2).values,
            rowLabels=summary.index.tolist(),
            colLabels=summary.columns.tolist(),
            loc="center",
        )
        table.scale(1, 1.5)
        pdf.savefig(fig_summary)
        plt.close(fig_summary)

        # Plot page
        pdf.savefig(fig)
        plt.close(fig)

    progress_callback("done", total, total)
    return pdf_path
