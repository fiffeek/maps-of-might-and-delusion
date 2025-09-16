import logging

logger = logging.getLogger("aiomad")


def setup_logging(debug: bool = False) -> None:
    """Configure the global logger based on debug flag"""
    level = logging.DEBUG if debug else logging.INFO

    logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(level)
