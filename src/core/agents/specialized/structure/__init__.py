"""Agentes especializados em detecao de code smells de estrutura."""

from .long_message_chain_agent import create_long_message_chain_agent
from .long_parameter_list_agent import create_long_parameter_list_agent

__all__ = [
    "create_long_message_chain_agent",
    "create_long_parameter_list_agent",
]