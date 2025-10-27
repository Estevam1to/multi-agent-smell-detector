"""
Supervisor Agent para coordenar os agentes especializados de detecção de code smells.

Implementação simples e eficiente que executa todos os agentes em paralelo.
"""

import asyncio
from typing import Dict, List

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from config.settings import settings
from specialized.complexity import (
    create_complex_conditional_agent,
    create_complex_method_agent,
    create_long_method_agent,
)
from specialized.naming import create_long_identifier_agent, create_magic_number_agent
from specialized.statements import (
    create_empty_catch_block_agent,
    create_long_lambda_function_agent,
    create_long_statement_agent,
    create_missing_default_agent,
)
from specialized.structure import (
    create_long_message_chain_agent,
    create_long_parameter_list_agent,
)


class CodeSmellSupervisor:
    """
    Supervisor que coordena a execução de todos os agentes de detecção de code smells.

    Executa todos os agentes em paralelo para economizar tempo e retorna os resultados consolidados.
    """

    def __init__(self):
        """Inicializa o supervisor e todos os agentes especializados."""
        # Inicializa o modelo LLM
        self.model = ChatAnthropic(
            model=settings.ANTHROPIC_MODEL,
            api_key=settings.ANTHROPIC_API_KEY,
            temperature=0,
        )

        # Cria todos os agentes especializados
        self.agents = {
            "long_method": create_long_method_agent(self.model),
            "long_parameter_list": create_long_parameter_list_agent(self.model),
            "long_statement": create_long_statement_agent(self.model),
            "long_identifier": create_long_identifier_agent(self.model),
            "empty_catch_block": create_empty_catch_block_agent(self.model),
            "complex_method": create_complex_method_agent(self.model),
            "complex_conditional": create_complex_conditional_agent(self.model),
            "missing_default": create_missing_default_agent(self.model),
            "long_lambda_function": create_long_lambda_function_agent(self.model),
            "long_message_chain": create_long_message_chain_agent(self.model),
            "magic_number": create_magic_number_agent(self.model),
        }

    async def _execute_agent(
        self, agent_name: str, agent, python_code: str
    ) -> Dict[str, any]:
        """
        Executa um agente específico e retorna o resultado.

        Args:
            agent_name: Nome do agente
            agent: Instância do agente
            python_code: Código Python a ser analisado

        Returns:
            Dicionário com resultados do agente
        """
        try:
            # Cria o estado inicial para o agente
            state = {
                "messages": [
                    HumanMessage(
                        content=f"Analise o seguinte código Python:\n\n```python\n{python_code}\n```"
                    )
                ]
            }

            # Executa o agente
            result = await agent.ainvoke(state)

            # Extrai a resposta do agente
            messages = result.get("messages", [])
            if messages:
                response = messages[-1].content
            else:
                response = "Nenhuma resposta do agente"

            return {
                "agent": agent_name,
                "status": "success",
                "findings": response,
                "has_smells": not (
                    "nenhum" in response.lower() and "detectado" in response.lower()
                ),
            }

        except Exception as e:
            return {
                "agent": agent_name,
                "status": "error",
                "error": str(e),
                "has_smells": False,
            }

    async def analyze_code(self, python_code: str) -> Dict[str, any]:
        """
        Analisa código Python usando todos os agentes especializados em paralelo.

        Args:
            python_code: Código Python a ser analisado

        Returns:
            Dicionário com resultados consolidados de todos os agentes
        """
        # Executa todos os agentes em paralelo
        tasks = [
            self._execute_agent(name, agent, python_code)
            for name, agent in self.agents.items()
        ]

        results = await asyncio.gather(*tasks)

        # Consolida os resultados
        code_smells = []
        for result in results:
            if result["status"] == "success" and result["has_smells"]:
                code_smells.append(
                    {
                        "smell_type": result["agent"],
                        "findings": result["findings"],
                    }
                )

        return {
            "total_smells_detected": len(code_smells),
            "code_smells": code_smells,
            "agents_executed": len(self.agents),
            "detailed_results": results,
        }


# Instância global do supervisor
_supervisor_instance = None


def get_supervisor() -> CodeSmellSupervisor:
    """
    Retorna a instância singleton do supervisor.

    Returns:
        Instância do CodeSmellSupervisor
    """
    global _supervisor_instance
    if _supervisor_instance is None:
        _supervisor_instance = CodeSmellSupervisor()
    return _supervisor_instance


async def analyze_code_with_supervisor(python_code: str) -> Dict[str, any]:
    """
    Função auxiliar para analisar código usando o supervisor.

    Args:
        python_code: Código Python a ser analisado

    Returns:
        Dicionário com resultados da análise
    """
    supervisor = get_supervisor()
    return await supervisor.analyze_code(python_code)
