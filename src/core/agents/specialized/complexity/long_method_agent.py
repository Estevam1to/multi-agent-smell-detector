"""
Agente especializado em detecção de Long Method.

Baseado em:
Fowler, M. (1999). Refactoring: Improving the Design of Existing Code.
Addison-Wesley Professional.

Este módulo fornece uma função simples que cria um agente de detecção
de Long Method usando LangGraph e o prompt acadêmico de Fowler.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from core.prompts.long_method_prompt import LONG_METHOD_AGENT_PROMPT
from core.tools import get_code_structure


def create_long_method_agent(model: BaseChatModel) -> CompiledStateGraph:
    """
    Cria e retorna um agente para detectar Long Method code smell.

    Esta função usa o paradigma funcional para criar um agente simples
    que analisa código e identifica métodos muito longos.

    O agente é criado com:
    - Um modelo LLM para processar o código
    - Uma lista vazia de tools (não precisamos de ferramentas externas)
    - Um prompt acadêmico baseado em Fowler (1999) como state_modifier

    Args:
        model: Instância do modelo BaseChatModel configurado

    Returns:
        Agent configurado pronto para analisar código
    """
    agent = create_react_agent(
        model=model,
        tools=[get_code_structure],
        prompt=LONG_METHOD_AGENT_PROMPT,
        name="long_method_agent",
    )

    return agent
