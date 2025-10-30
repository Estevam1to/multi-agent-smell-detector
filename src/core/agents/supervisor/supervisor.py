"""Supervisor Agent V2 com structured output."""

import asyncio
import logging
from typing import Any, Dict, List

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config.settings import settings
from core.agents.supervisor.agent_config import AGENT_CONFIGS
from core.agents.supervisor.constants import AGENT_EXECUTION_DELAY
from core.agents.supervisor.detection_enricher import enrich_detections

logger = logging.getLogger(__name__)


class CodeSmellSupervisor:
    def __init__(self):
        self.model = ChatOpenAI(
            model=settings.OPENROUTER_API_MODEL,
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
            temperature=0,
        )
        self.agents = AGENT_CONFIGS

    async def _execute_agent(
        self,
        agent_name: str,
        agent_config: Dict,
        python_code: str,
        file_path: str,
        project_name: str,
    ) -> List[Dict[str, Any]]:
        try:
            structured_model = self.model.with_structured_output(
                agent_config["schema"], method="json_mode"
            )

            messages = [
                SystemMessage(content=agent_config["prompt"]),
                HumanMessage(
                    content=f"Analise o seguinte código Python e retorne APENAS um objeto JSON válido:\n\n```python\n{python_code}\n```"
                ),
            ]

            result = await structured_model.ainvoke(messages)
            detections = [result] if result.detected else []
            
            return enrich_detections(
                detections, python_code, file_path, project_name, agent_name
            )

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
            await asyncio.sleep(AGENT_EXECUTION_DELAY)

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

def get_supervisor() -> CodeSmellSupervisor:
    return CodeSmellSupervisor()


async def analyze_code_with_supervisor_v2(
    python_code: str, file_path: str = "unknown.py", project_name: str = "Code"
) -> Dict[str, Any]:
    supervisor = get_supervisor()
    return await supervisor.analyze_code(python_code, file_path, project_name)
