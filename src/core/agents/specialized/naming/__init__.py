"""Agentes especializados em detecao de code smells de nomenclatura."""

from .long_identifier_agent import create_long_identifier_agent
from .magic_number_agent import create_magic_number_agent

__all__ = [
    "create_long_identifier_agent",
    "create_magic_number_agent",
]