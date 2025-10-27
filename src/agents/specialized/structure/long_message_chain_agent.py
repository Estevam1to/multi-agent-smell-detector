"""
Agente especializado em detecção de Long Message Chain.

Baseado em Fowler (1999) - Refactoring: Improving the Design of Existing Code.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from prompts.long_message_chain_prompt import LONG_MESSAGE_CHAIN_AGENT_PROMPT


def create_long_message_chain_agent(model: BaseChatModel) -> CompiledStateGraph:
    """
    Cria e retorna um agente para detectar Long Message Chain code smell.

    Args:
        model: Instância do modelo BaseChatModel configurado

    Returns:
        Agent configurado pronto para analisar código
    """
    agent = create_react_agent(
        model=model,
        tools=[],
        prompt=LONG_MESSAGE_CHAIN_AGENT_PROMPT,
        name="long_message_chain_agent",
    )

    return agent
