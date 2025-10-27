"""
Agente especializado em detecção de Complex Conditional.

Baseado em Fowler (2018) - Refactoring, 2nd Edition.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from prompts.complex_conditional_prompt import COMPLEX_CONDITIONAL_AGENT_PROMPT


def create_complex_conditional_agent(model: BaseChatModel) -> CompiledStateGraph:
    """
    Cria e retorna um agente para detectar Complex Conditional code smell.

    Args:
        model: Instância do modelo BaseChatModel configurado

    Returns:
        Agent configurado pronto para analisar código
    """
    agent = create_react_agent(
        model=model,
        tools=[],
        prompt=COMPLEX_CONDITIONAL_AGENT_PROMPT,
        name="complex_conditional_agent",
    )

    return agent
