import time

from .logger import log
from .profiler import run as run_profiler
from .forecaster import run as run_forecaster
from .chart_planner import run as run_chart_planner
from .visual_builder import run as run_visual_builder
from .insight_writer import run as run_insight_writer
from .pdf_composer import run as run_pdf_composer


STAGES = [
    ("profiler", run_profiler),
    ("forecaster", run_forecaster),
    ("chart_planner", run_chart_planner),
    ("visual_builder", run_visual_builder),
    ("insight_writer", run_insight_writer),
    ("pdf_composer", run_pdf_composer),
]


def run_pipeline(data=None):
    """Run all stages and log their completion."""
    for name, stage_fn in STAGES:
        start = time.perf_counter()
        artefacts = stage_fn(data)
        duration = (time.perf_counter() - start) * 1000
        artefact_count = len(artefacts) if artefacts is not None else 0
        log.info(
            "stage_done",
            stage_name=name,
            duration_ms=int(duration),
            artefacts_count=artefact_count,
        )
