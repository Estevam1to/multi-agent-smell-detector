"""
Agente especializado em detecção de Long Lambda Function.

Baseado em Chen et al. (2016) - "Detecting code smells in python programs".
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from core.prompts.long_lambda_function_prompt import LONG_LAMBDA_FUNCTION_AGENT_PROMPT
from core.tools import get_code_structure


def create_long_lambda_function_agent(model: BaseChatModel) -> CompiledStateGraph:
    """
    Cria e retorna um agente para detectar Long Lambda Function code smell.

    Args:
        model: Instância do modelo BaseChatModel configurado

    Returns:
        Agent configurado pronto para analisar código
    """
    agent = create_react_agent(
        model=model,
        tools=[get_code_structure],
        prompt=LONG_LAMBDA_FUNCTION_AGENT_PROMPT,
        name="long_lambda_function_agent",
    )

    return agent
