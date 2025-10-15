"""
Agente especializado em detecção de Long Parameter List.

Baseado em:
Fowler, M. (1999). Refactoring: Improving the Design of Existing Code.
Addison-Wesley Professional.

Este módulo fornece uma função simples que cria um agente de detecção
de Long Parameter List usando LangGraph e o prompt acadêmico de Fowler.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from prompts.long_parameter_list_prompt import LONG_PARAMETER_LIST_AGENT_PROMPT


def create_long_parameter_list_agent(model: BaseChatModel) -> CompiledStateGraph:
    """
    Cria e retorna um agente para detectar Long Parameter List code smell.

    Esta função usa o paradigma funcional para criar um agente simples
    que analisa código e identifica listas de parâmetros muito longas.

    O agente é criado com:
    - Um modelo LLM para processar o código
    - Uma lista vazia de tools (não precisamos de ferramentas externas)
    - Um prompt acadêmico baseado em Fowler (1999) como state_modifier

    Args:
        model: Instância do modelo ChatAnthropic configurado

    Returns:
        Agent configurado pronto para analisar código
    """
    agent = create_react_agent(
        model=model,
        tools=[],
        prompt=LONG_PARAMETER_LIST_AGENT_PROMPT,
        name="long_parameter_list_agent",
    )

    return agent
