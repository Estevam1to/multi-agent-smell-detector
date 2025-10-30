"""
Agente especializado em detecção de Missing Default.

Baseado em CWE-478 (MITRE) - Missing Default Case in Multiple Condition Expression.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from agents.prompts.missing_default_prompt import MISSING_DEFAULT_AGENT_PROMPT


def create_missing_default_agent(model: BaseChatModel) -> CompiledStateGraph:
    """
    Cria e retorna um agente para detectar Missing Default code smell.

    Args:
        model: Instância do modelo BaseChatModel configurado

    Returns:
        Agent configurado pronto para analisar código
    """
    agent = create_react_agent(
        model=model,
        tools=[],
        prompt=MISSING_DEFAULT_AGENT_PROMPT,
        name="missing_default_agent",
    )

    return agent
