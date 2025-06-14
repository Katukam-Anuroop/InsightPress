import logging
import sys

import structlog


def configure_logging():
    """Configure structlog with JSON or rich renderer."""
    timestamper = structlog.processors.TimeStamper(fmt="iso")
    shared_processors = [
        structlog.processors.add_log_level,
        timestamper,
    ]

    if sys.stderr.isatty():
        try:
            from structlog.rich import RichRenderer

            renderer = RichRenderer()
        except Exception:  # pragma: no cover - fallback for older structlog
            from structlog.dev import ConsoleRenderer

            renderer = ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=shared_processors + [renderer],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(format="%(message)s", level=logging.INFO)


log = structlog.get_logger()
