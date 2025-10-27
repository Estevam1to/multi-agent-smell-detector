"""Agentes especializados em detecção de code smells de statements."""

from .empty_catch_block_agent import create_empty_catch_block_agent
from .long_lambda_function_agent import create_long_lambda_function_agent
from .long_statement_agent import create_long_statement_agent
from .missing_default_agent import create_missing_default_agent

__all__ = [
    "create_empty_catch_block_agent",
    "create_long_lambda_function_agent",
    "create_long_statement_agent",
    "create_missing_default_agent",
]
