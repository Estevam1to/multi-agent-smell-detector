import logging
import sys


def get_logger(name: str = "app") -> logging.Logger:
    """
    Cria e retorna um logger configurado para o projeto.

    Args:
        name (str): Nome do logger. Padrão: "app".

    Returns:
        logging.Logger: Instância configurada de logger.
    """

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
