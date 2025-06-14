from __future__ import annotations

from pathlib import Path
from pydantic import BaseSettings

class Config(BaseSettings):
    """Global configuration for the insight pipeline."""

    cache_dir: Path = Path("cache")
    dpi: int = 300
    llm_model: str = "local-llm"

    class Config:
        env_prefix = "INSIGHT_"
