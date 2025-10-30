"""
Agente especializado em detecção de Long Statement.

Baseado em PEP 8 - Style Guide for Python Code.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from agents.prompts.long_statement_prompt import LONG_STATEMENT_AGENT_PROMPT


def create_long_statement_agent(model: BaseChatModel) -> CompiledStateGraph:
    """
    Cria e retorna um agente para detectar Long Statement code smell.

    Args:
        model: Instância do modelo BaseChatModel configurado

    Returns:
        Agent configurado pronto para analisar código
    """
    agent = create_react_agent(
        model=model,
        tools=[],
        prompt=LONG_STATEMENT_AGENT_PROMPT,
        name="long_statement_agent",
    )

    return agent
