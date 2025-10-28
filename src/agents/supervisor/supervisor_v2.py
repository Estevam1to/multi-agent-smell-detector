"""Supervisor Agent V2 com structured output."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Union

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage

from config.settings import settings
from utils.code_parser import CodeParser

logger = logging.getLogger(__name__)
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
from agents.prompts.complex_method_prompt import COMPLEX_METHOD_AGENT_PROMPT
from agents.prompts.long_method_prompt import LONG_METHOD_AGENT_PROMPT
from agents.prompts.complex_conditional_prompt import COMPLEX_CONDITIONAL_AGENT_PROMPT
from agents.prompts.long_parameter_list_prompt import LONG_PARAMETER_LIST_AGENT_PROMPT
from agents.prompts.long_statement_prompt import LONG_STATEMENT_AGENT_PROMPT
from agents.prompts.long_identifier_prompt import LONG_IDENTIFIER_AGENT_PROMPT
from agents.prompts.magic_number_prompt import MAGIC_NUMBER_AGENT_PROMPT
from agents.prompts.empty_catch_block_prompt import EMPTY_CATCH_BLOCK_AGENT_PROMPT
from agents.prompts.missing_default_prompt import MISSING_DEFAULT_AGENT_PROMPT
from agents.prompts.long_lambda_function_prompt import LONG_LAMBDA_FUNCTION_AGENT_PROMPT
from agents.prompts.long_message_chain_prompt import LONG_MESSAGE_CHAIN_AGENT_PROMPT


class CodeSmellSupervisorV2:

    def __init__(self):
        self.base_model = ChatAnthropic(
            model=settings.ANTHROPIC_MODEL,
            api_key=settings.ANTHROPIC_API_KEY,
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
        self, agent_name: str, agent_config: Dict, python_code: str, file_path: str, project_name: str
    ) -> List[Dict[str, Any]]:

        try:
            structured_model = self.base_model.with_structured_output(
                Union[agent_config["schema"], List[agent_config["schema"]]],
                method="json_mode"
            )

            messages = [
                SystemMessage(content=agent_config["prompt"]),
                HumanMessage(
                    content=f"Analise o seguinte código Python:\n\n```python\n{python_code}\n```"
                ),
            ]

            result = await structured_model.ainvoke(messages)

            detections = result if isinstance(result, list) else [result]

            parser = CodeParser(python_code, file_path)

            valid_detections = []
            for detection in detections:
                if detection.detected:
                    detection.Project = project_name
                    detection.Package = parser.get_package_name()
                    detection.Module = parser.get_module_name()
                    detection.File = file_path
                    valid_detections.append(detection)

            return valid_detections

        except Exception as e:
            logger.error(f"Error executing agent {agent_name} for {file_path}: {e}", exc_info=True)
            return []

    async def analyze_code(
        self, python_code: str, file_path: str = "unknown.py", project_name: str = "Code"
    ) -> Dict[str, Any]:

        tasks = [
            self._execute_agent(name, config, python_code, file_path, project_name)
            for name, config in self.agents.items()
        ]

        results = await asyncio.gather(*tasks)

        all_detections = []
        for detections in results:
            all_detections.extend(detections)

        detections_as_dicts = [d.model_dump(by_alias=True) for d in all_detections]

        return {
            "total_smells_detected": len(detections_as_dicts),
            "code_smells": detections_as_dicts,
            "agents_executed": len(self.agents),
        }

    @staticmethod
    def save_to_json(detections: List[Dict[str, Any]], output_file: str):
        Path(output_file).write_text(
            json.dumps(detections, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )


_supervisor_v2_instance = None


def get_supervisor_v2() -> CodeSmellSupervisorV2:
    global _supervisor_v2_instance
    if _supervisor_v2_instance is None:
        _supervisor_v2_instance = CodeSmellSupervisorV2()
    return _supervisor_v2_instance


async def analyze_code_with_supervisor_v2(
    python_code: str, file_path: str = "unknown.py", project_name: str = "Code"
) -> Dict[str, Any]:
    supervisor = get_supervisor_v2()
    return await supervisor.analyze_code(python_code, file_path, project_name)
