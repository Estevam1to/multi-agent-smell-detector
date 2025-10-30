"""Supervisor Agent V2 com structured output."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from core.prompts.complex_conditional_prompt import COMPLEX_CONDITIONAL_AGENT_PROMPT
from core.prompts.complex_method_prompt import COMPLEX_METHOD_AGENT_PROMPT
from core.prompts.empty_catch_block_prompt import EMPTY_CATCH_BLOCK_AGENT_PROMPT
from core.prompts.long_identifier_prompt import LONG_IDENTIFIER_AGENT_PROMPT
from core.prompts.long_lambda_function_prompt import LONG_LAMBDA_FUNCTION_AGENT_PROMPT
from core.prompts.long_message_chain_prompt import LONG_MESSAGE_CHAIN_AGENT_PROMPT
from core.prompts.long_method_prompt import LONG_METHOD_AGENT_PROMPT
from core.prompts.long_parameter_list_prompt import LONG_PARAMETER_LIST_AGENT_PROMPT
from core.prompts.long_statement_prompt import LONG_STATEMENT_AGENT_PROMPT
from core.prompts.magic_number_prompt import MAGIC_NUMBER_AGENT_PROMPT
from core.prompts.missing_default_prompt import MISSING_DEFAULT_AGENT_PROMPT
from config.settings import settings
from core.schemas.agent_response import (
    ComplexConditionalDetection,
    ComplexMethodDetection,
    EmptyCatchBlockDetection,
    LongIdentifierDetection,
    LongLambdaFunctionDetection,
    LongMessageChainDetection,
    LongMethodDetection,
    LongParameterListDetection,
    LongStatementDetection,
    MagicNumberDetection,
    MissingDefaultDetection,
)
from core.utils.code_parser import CodeParser

logger = logging.getLogger(__name__)


class CodeSmellSupervisorV2:
    def __init__(self):
        self.base_model = ChatOpenAI(
            model=settings.OPENROUTER_API_MODEL,
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
            temperature=0,
        )

        self.agents = {
            "complex_method": {
                "prompt": COMPLEX_METHOD_AGENT_PROMPT,
                "schema": ComplexMethodDetection,
            },
            "long_method": {
                "prompt": LONG_METHOD_AGENT_PROMPT,
                "schema": LongMethodDetection,
            },
            "complex_conditional": {
                "prompt": COMPLEX_CONDITIONAL_AGENT_PROMPT,
                "schema": ComplexConditionalDetection,
            },
            "long_parameter_list": {
                "prompt": LONG_PARAMETER_LIST_AGENT_PROMPT,
                "schema": LongParameterListDetection,
            },
            "long_statement": {
                "prompt": LONG_STATEMENT_AGENT_PROMPT,
                "schema": LongStatementDetection,
            },
            "long_identifier": {
                "prompt": LONG_IDENTIFIER_AGENT_PROMPT,
                "schema": LongIdentifierDetection,
            },
            "magic_number": {
                "prompt": MAGIC_NUMBER_AGENT_PROMPT,
                "schema": MagicNumberDetection,
            },
            "empty_catch_block": {
                "prompt": EMPTY_CATCH_BLOCK_AGENT_PROMPT,
                "schema": EmptyCatchBlockDetection,
            },
            "missing_default": {
                "prompt": MISSING_DEFAULT_AGENT_PROMPT,
                "schema": MissingDefaultDetection,
            },
            "long_lambda_function": {
                "prompt": LONG_LAMBDA_FUNCTION_AGENT_PROMPT,
                "schema": LongLambdaFunctionDetection,
            },
            "long_message_chain": {
                "prompt": LONG_MESSAGE_CHAIN_AGENT_PROMPT,
                "schema": LongMessageChainDetection,
            },
        }

    async def _execute_agent(
        self,
        agent_name: str,
        agent_config: Dict,
        python_code: str,
        file_path: str,
        project_name: str,
    ) -> List[Dict[str, Any]]:
        try:
            structured_model = self.base_model.with_structured_output(
                agent_config["schema"],
                method="json_mode",
            )

            messages = [
                SystemMessage(content=agent_config["prompt"]),
                HumanMessage(
                    content=f"Analise o seguinte código Python e retorne APENAS um objeto JSON válido:\n\n```python\n{python_code}\n```"
                ),
            ]

            result = await structured_model.ainvoke(messages)

            detections = [result] if result.detected else []

            parser = CodeParser(python_code, file_path)

            valid_detections = []
            for detection in detections:
                if detection.detected:
                    if not detection.Line_no or not detection.Description:
                        logger.warning(f"Detecção incompleta ignorada em {agent_name}")
                        continue
                    
                    detection.Project = project_name
                    detection.Package = parser.get_package_name()
                    detection.Module = parser.get_module_name()
                    detection.File = file_path
                    valid_detections.append(detection)

            return valid_detections

        except Exception as e:
            logger.error(f"Error executing agent {agent_name} for {file_path}: {e}")
            return []

    async def analyze_code(
        self,
        python_code: str,
        file_path: str = "unknown.py",
        project_name: str = "Code",
    ) -> Dict[str, Any]:
        results = []
        for name, config in self.agents.items():
            result = await self._execute_agent(
                name, config, python_code, file_path, project_name
            )
            results.append(result)
            await asyncio.sleep(0.5)  # Delay para evitar rate limit

        all_detections = []
        for detections in results:
            all_detections.extend(detections)

        detections_as_dicts = []
        for d in all_detections:
            dict_data = d.model_dump()
            dict_data["Line no"] = dict_data.pop("Line_no", "")
            detections_as_dicts.append(dict_data)

        return {
            "total_smells_detected": len(detections_as_dicts),
            "code_smells": detections_as_dicts,
            "agents_executed": len(self.agents),
        }

    @staticmethod
    def save_to_json(detections: List[Dict[str, Any]], output_file: str):
        Path(output_file).write_text(
            json.dumps(detections, indent=2, ensure_ascii=False), encoding="utf-8"
        )


def get_supervisor_v2() -> CodeSmellSupervisorV2:
    return CodeSmellSupervisorV2()


async def analyze_code_with_supervisor_v2(
    python_code: str, file_path: str = "unknown.py", project_name: str = "Code"
) -> Dict[str, Any]:
    supervisor = get_supervisor_v2()
    return await supervisor.analyze_code(python_code, file_path, project_name)
