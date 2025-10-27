"""
Agente especializado em detecção de Long Identifier.

Baseado em Clean Code principles (Martin, 2008).
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from prompts.long_identifier_prompt import LONG_IDENTIFIER_AGENT_PROMPT


def create_long_identifier_agent(model: BaseChatModel) -> CompiledStateGraph:
    """
    Cria e retorna um agente para detectar Long Identifier code smell.

    Args:
        model: Instância do modelo BaseChatModel configurado

    Returns:
        Agent configurado pronto para analisar código
    """
    agent = create_react_agent(
        model=model,
        tools=[],
        prompt=LONG_IDENTIFIER_AGENT_PROMPT,
        name="long_identifier_agent",
    )

    return agent
