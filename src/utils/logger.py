import logging
import pathlib
from datetime import UTC, datetime


def get_logger(name):
    log_dir = pathlib.Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    log_filename = log_dir / f"{datetime.now(UTC).date()}.log"
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fileHandler = logging.FileHandler(log_filename, encoding="utf-8")
        consoleHandler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        fileHandler.setFormatter(formatter)
        consoleHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        logger.addHandler(consoleHandler)

        logger.propagate = False

    return logger