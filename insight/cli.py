from .logger import configure_logging
from .pipeline import run_pipeline


def main() -> None:
    configure_logging()
    run_pipeline()


if __name__ == "__main__":
    main()
