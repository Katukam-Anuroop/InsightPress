"""InsightPress package."""

from .logger import configure_logging, log
from .pipeline import run_pipeline

__all__ = [
    "configure_logging",
    "log",
    "run_pipeline",
]
