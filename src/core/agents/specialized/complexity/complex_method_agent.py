"""
Agente especializado em detecção de Complex Method.

Baseado em McCabe (1976) - "A complexity measure".
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from core.prompts.complex_method_prompt import COMPLEX_METHOD_AGENT_PROMPT
from core.tools import get_code_structure


def create_complex_method_agent(model: BaseChatModel) -> CompiledStateGraph:
    """
    Cria e retorna um agente para detectar Complex Method code smell.

    Args:
        model: Instância do modelo BaseChatModel configurado

    Returns:
        Agent configurado pronto para analisar código
    """
    agent = create_react_agent(
        model=model,
        tools=[get_code_structure],
        prompt=COMPLEX_METHOD_AGENT_PROMPT,
        name="complex_method_agent"
    )

    return agent
