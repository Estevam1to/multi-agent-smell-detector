"""
Agente especializado em detecção de Empty Catch Block.

Baseado em Clean Code - Robert C. Martin (2008), Capítulo 7.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from prompts.empty_catch_block_prompt import EMPTY_CATCH_BLOCK_AGENT_PROMPT


def create_empty_catch_block_agent(model: BaseChatModel) -> CompiledStateGraph:
    """
    Cria e retorna um agente para detectar Empty Catch Block code smell.

    Args:
        model: Instância do modelo BaseChatModel configurado

    Returns:
        Agent configurado pronto para analisar código
    """
    agent = create_react_agent(
        model=model,
        tools=[],
        prompt=EMPTY_CATCH_BLOCK_AGENT_PROMPT,
        name="empty_catch_block_agent",
    )

    return agent
