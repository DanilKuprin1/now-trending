import logging

from pythonjsonlogger.json import JsonFormatter


def setup_logging() -> None:
    logger: logging.Logger = logging.getLogger()

    log_handler = logging.StreamHandler()
    formatter = JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"
    )
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel("INFO")
