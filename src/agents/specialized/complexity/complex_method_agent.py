"""
Agente especializado em detecção de Complex Method.

Baseado em McCabe (1976) - "A complexity measure".
"""

from typing import Union, List
from langchain_core.language_models.chat_models import BaseChatModel
from agents.prompts.complex_method_prompt import COMPLEX_METHOD_AGENT_PROMPT
from agents.schemas.agent_response import ComplexMethodDetection


def create_complex_method_agent(model: BaseChatModel):
    """
    Cria e retorna um agente para detectar Complex Method code smell.

    Args:
        model: Instância do modelo BaseChatModel configurado

    Returns:
        Model configurado com structured output
    """
    # Configura o modelo para retornar JSON estruturado
    structured_model = model.with_structured_output(
        Union[ComplexMethodDetection, List[ComplexMethodDetection]],
        method="json_mode"
    )

    return structured_model
