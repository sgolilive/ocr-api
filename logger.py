import logging

def get_logger(name: str):
    logger = logging.getLogger(name)

    if not logger.handlers:  # Prevent adding multiple handlers
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()  # Logs to stdout
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger