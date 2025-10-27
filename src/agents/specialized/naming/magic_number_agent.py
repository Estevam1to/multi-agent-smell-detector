"""
Agente especializado em detecção de Magic Number.

Baseado em Fowler (1999, 2018) e Martin (2008) - Clean Code.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from prompts.magic_number_prompt import MAGIC_NUMBER_AGENT_PROMPT


def create_magic_number_agent(model: BaseChatModel) -> CompiledStateGraph:
    """
    Cria e retorna um agente para detectar Magic Number code smell.

    Args:
        model: Instância do modelo BaseChatModel configurado

    Returns:
        Agent configurado pronto para analisar código
    """
    agent = create_react_agent(
        model=model,
        tools=[],
        prompt=MAGIC_NUMBER_AGENT_PROMPT,
        name="magic_number_agent",
    )

    return agent
