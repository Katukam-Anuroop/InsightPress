"""Command line interface for InsightPress demo."""

from __future__ import annotations

import argparse
import pandas as pd
from . import pipeline
from . import cache_utils


def main(argv=None):
    parser = argparse.ArgumentParser(description="InsightPress demo")
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear cached results and exit",
    )
    args = parser.parse_args(argv)

    if args.clear_cache:
        cache_utils.clear_cache()
        print("Cache cleared.")
        return

    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    pipeline.build_figures(df)
    pipeline.maybe_forecast(df)
    narrative = pipeline.write_narrative(df)
    print(narrative)


if __name__ == "__main__":
    main()
