"""Configuração de logging."""

import logging
import sys


def get_logger(name: str = "app") -> logging.Logger:
    """Cria logger configurado."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False

    return logger


logger = get_logger()
