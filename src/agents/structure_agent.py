from typing import Any

from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph


def create_structure_agent(llm: Any, tools: list) -> StateGraph:
    """
    Cria o agente especializado em análise de estrutura

    Args:
        llm (ChatAnthropic): Instância do modelo de linguagem Anthropic
        tools (list): Lista de ferramentas disponíveis para o agente

    Returns:
        StateGraph: Agente configurado para análise de estrutura
    """

    system_message = """Você é um agente especializado em detectar problemas de ESTRUTURA em código Python.
    Seu foco é identificar:
    - Large Class (> 20 métodos ou > 300 linhas)
    - God Class (> 30 métodos ou > 15 atributos)
    - Feature Envy (métodos que usam demais outras classes)
    - Violações do Single Responsibility Principle

    INSTRUÇÕES IMPORTANTES:
    1. Você receberá código Python na mensagem do usuário
    2. Use as ferramentas disponíveis passando TODO o código que recebeu
    3. NÃO modifique o código antes de passá-lo para as ferramentas
    4. NÃO tente extrair apenas trechos - passe o código COMPLETO
    5. Após receber os resultados, analise e reporte os problemas com sugestões de refatoração
    """

    return create_react_agent(model=llm, tools=tools, prompt=system_message)
