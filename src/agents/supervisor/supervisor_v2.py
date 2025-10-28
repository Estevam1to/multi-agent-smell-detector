"""
Supervisor Agent V2 para coordenar os agentes com structured output.

Implementação que usa response format do Claude para saídas estruturadas.
"""

import asyncio
from typing import Dict, List, Any, Union

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage

from config.settings import settings
from schemas.agent_response import (
    ComplexMethodDetection,
    LongMethodDetection,
    LongParameterListDetection,
    ComplexConditionalDetection,
    LongStatementDetection,
    LongIdentifierDetection,
    MagicNumberDetection,
    EmptyCatchBlockDetection,
    MissingDefaultDetection,
    LongLambdaFunctionDetection,
    LongMessageChainDetection,
)
from prompts.complex_method_prompt import COMPLEX_METHOD_AGENT_PROMPT
from prompts.long_method_prompt import LONG_METHOD_AGENT_PROMPT
from prompts.complex_conditional_prompt import COMPLEX_CONDITIONAL_AGENT_PROMPT
from prompts.long_parameter_list_prompt import LONG_PARAMETER_LIST_AGENT_PROMPT
from prompts.long_statement_prompt import LONG_STATEMENT_AGENT_PROMPT
from prompts.long_identifier_prompt import LONG_IDENTIFIER_AGENT_PROMPT
from prompts.magic_number_prompt import MAGIC_NUMBER_AGENT_PROMPT
from prompts.empty_catch_block_prompt import EMPTY_CATCH_BLOCK_AGENT_PROMPT
from prompts.missing_default_prompt import MISSING_DEFAULT_AGENT_PROMPT
from prompts.long_lambda_function_prompt import LONG_LAMBDA_FUNCTION_AGENT_PROMPT
from prompts.long_message_chain_prompt import LONG_MESSAGE_CHAIN_AGENT_PROMPT


class CodeSmellSupervisorV2:
    """
    Supervisor que coordena a execução de todos os agentes com structured output.

    Usa response format do Claude para garantir saídas JSON estruturadas.
    """

    def __init__(self):
        """Inicializa o supervisor e configura os agentes com structured output."""
        self.base_model = ChatAnthropic(
            model=settings.ANTHROPIC_MODEL,
            api_key=settings.ANTHROPIC_API_KEY,
            temperature=0,
        )

        # Configura cada agente com seu prompt e schema específico
        self.agents = {
            "complex_method": {
                "prompt": COMPLEX_METHOD_AGENT_PROMPT,
                "schema": Union[ComplexMethodDetection, List[ComplexMethodDetection]],
            },
            "long_method": {
                "prompt": LONG_METHOD_AGENT_PROMPT,
                "schema": Union[LongMethodDetection, List[LongMethodDetection]],
            },
            "complex_conditional": {
                "prompt": COMPLEX_CONDITIONAL_AGENT_PROMPT,
                "schema": Union[ComplexConditionalDetection, List[ComplexConditionalDetection]],
            },
            "long_parameter_list": {
                "prompt": LONG_PARAMETER_LIST_AGENT_PROMPT,
                "schema": Union[LongParameterListDetection, List[LongParameterListDetection]],
            },
            "long_statement": {
                "prompt": LONG_STATEMENT_AGENT_PROMPT,
                "schema": Union[LongStatementDetection, List[LongStatementDetection]],
            },
            "long_identifier": {
                "prompt": LONG_IDENTIFIER_AGENT_PROMPT,
                "schema": Union[LongIdentifierDetection, List[LongIdentifierDetection]],
            },
            "magic_number": {
                "prompt": MAGIC_NUMBER_AGENT_PROMPT,
                "schema": Union[MagicNumberDetection, List[MagicNumberDetection]],
            },
            "empty_catch_block": {
                "prompt": EMPTY_CATCH_BLOCK_AGENT_PROMPT,
                "schema": Union[EmptyCatchBlockDetection, List[EmptyCatchBlockDetection]],
            },
            "missing_default": {
                "prompt": MISSING_DEFAULT_AGENT_PROMPT,
                "schema": Union[MissingDefaultDetection, List[MissingDefaultDetection]],
            },
            "long_lambda_function": {
                "prompt": LONG_LAMBDA_FUNCTION_AGENT_PROMPT,
                "schema": Union[LongLambdaFunctionDetection, List[LongLambdaFunctionDetection]],
            },
            "long_message_chain": {
                "prompt": LONG_MESSAGE_CHAIN_AGENT_PROMPT,
                "schema": Union[LongMessageChainDetection, List[LongMessageChainDetection]],
            },
        }

    async def _execute_agent(
        self, agent_name: str, agent_config: Dict, python_code: str
    ) -> Dict[str, Any]:
        """
        Executa um agente específico com structured output.

        Args:
            agent_name: Nome do agente
            agent_config: Configuração do agente (prompt e schema)
            python_code: Código Python a ser analisado

        Returns:
            Dicionário com resultados estruturados do agente
        """
        try:
            # Cria modelo com structured output para este agente
            structured_model = self.base_model.with_structured_output(
                agent_config["schema"],
                method="json_mode"
            )

            # Monta mensagens
            messages = [
                SystemMessage(content=agent_config["prompt"]),
                HumanMessage(
                    content=f"Analise o seguinte código Python:\n\n```python\n{python_code}\n```"
                ),
            ]

            # Invoca o modelo
            result = await structured_model.ainvoke(messages)

            # Normaliza resultado (pode ser um item ou lista)
            if isinstance(result, list):
                detections = result
            else:
                detections = [result] if result.detected else []

            return {
                "agent": agent_name,
                "status": "success",
                "detections": detections,
                "has_smells": len(detections) > 0 and any(d.detected for d in detections),
            }

        except Exception as e:
            return {
                "agent": agent_name,
                "status": "error",
                "error": str(e),
                "detections": [],
                "has_smells": False,
            }

    async def analyze_code(self, python_code: str) -> Dict[str, Any]:
        """
        Analisa código Python usando todos os agentes em paralelo.

        Args:
            python_code: Código Python a ser analisado

        Returns:
            Dicionário com resultados estruturados consolidados
        """
        # Executa todos os agentes em paralelo
        tasks = [
            self._execute_agent(name, config, python_code)
            for name, config in self.agents.items()
        ]

        results = await asyncio.gather(*tasks)

        # Consolida todas as detecções estruturadas
        all_detections = []
        for result in results:
            if result["status"] == "success" and result["has_smells"]:
                all_detections.extend(result["detections"])

        # Converte detecções Pydantic para dicts
        detections_as_dicts = [
            detection.model_dump() for detection in all_detections
        ]

        return {
            "total_smells_detected": len(detections_as_dicts),
            "code_smells": detections_as_dicts,
            "agents_executed": len(self.agents),
            "detailed_results": results,
        }


_supervisor_v2_instance = None


def get_supervisor_v2() -> CodeSmellSupervisorV2:
    """
    Retorna a instância singleton do supervisor V2.

    Returns:
        Instância do CodeSmellSupervisorV2
    """
    global _supervisor_v2_instance
    if _supervisor_v2_instance is None:
        _supervisor_v2_instance = CodeSmellSupervisorV2()
    return _supervisor_v2_instance


async def analyze_code_with_supervisor_v2(python_code: str) -> Dict[str, Any]:
    """
    Função auxiliar para analisar código usando o supervisor V2.

    Args:
        python_code: Código Python a ser analisado

    Returns:
        Dicionário com resultados estruturados da análise
    """
    supervisor = get_supervisor_v2()
    return await supervisor.analyze_code(python_code)
