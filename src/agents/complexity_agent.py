from typing import Any

from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph  


def create_complexity_agent(llm: Any, tools: list) -> StateGraph:
    """
    Cria o agente especializado em análise de complexidade

    Args:
        llm (ChatAnthropic): Instância do modelo de linguagem Anthropic
        tools (list): Lista de ferramentas disponíveis para o agente

    Returns:
        StateGraph: Agente configurado para análise de complexidade
    """

    system_message = """Você é um agente especializado em detectar problemas de COMPLEXIDADE em código Python.
    Seu foco é identificar:
    - Complexidade ciclomática alta (> 10)
    - Funções muito longas (> 50 linhas)
    - Long Parameter List (> 5 parâmetros)
    - Condicionais aninhadas

    INSTRUÇÕES IMPORTANTES:
    1. Você receberá código Python na mensagem do usuário
    2. Use a ferramenta 'analyze_cyclomatic_complexity' passando TODO o código que recebeu
    3. NÃO modifique o código antes de passá-lo para a ferramenta
    4. NÃO tente extrair apenas trechos - passe o código COMPLETO
    5. Após receber o resultado da ferramenta, analise e reporte os problemas encontrados
    
    Seja específico sobre a localização (linha) e severidade do problema."""

    return create_react_agent(model=llm, tools=tools, prompt=system_message)
