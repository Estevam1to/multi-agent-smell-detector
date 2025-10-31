"""Supervisor Agent usando langgraph-supervisor."""

import logging
from typing import Any, Dict

from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor

from config.settings import settings
from core.agents.supervisor.agent_config import AGENT_CONFIGS
from core.agents.supervisor.detection_enricher import enrich_detections
from core.agents.specialized.complexity import (
    create_complex_conditional_agent,
    create_complex_method_agent,
    create_long_method_agent,
)
from core.agents.specialized.naming import (
    create_long_identifier_agent,
    create_magic_number_agent,
)
from core.agents.specialized.statements import (
    create_empty_catch_block_agent,
    create_long_lambda_function_agent,
    create_long_statement_agent,
    create_missing_default_agent,
)
from core.agents.specialized.structure import (
    create_long_message_chain_agent,
    create_long_parameter_list_agent,
)

logger = logging.getLogger(__name__)


class CodeSmellSupervisor:
    def __init__(self):
        self.model = ChatOpenAI(
            model=settings.OPENROUTER_API_MODEL,
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
            temperature=0,
        )
        self.specialized_agents = [
            create_complex_method_agent(self.model),
            create_long_method_agent(self.model),
            create_complex_conditional_agent(self.model),
            create_long_parameter_list_agent(self.model),
            create_long_statement_agent(self.model),
            create_long_identifier_agent(self.model),
            create_magic_number_agent(self.model),
            create_empty_catch_block_agent(self.model),
            create_missing_default_agent(self.model),
            create_long_lambda_function_agent(self.model),
            create_long_message_chain_agent(self.model),
        ]
        self.supervisor = self._create_supervisor()

    def _create_supervisor(self):
        workflow = create_supervisor(
            self.specialized_agents,
            model=self.model,
            prompt="You are a code smell detection supervisor. Coordinate the 11 specialized agents to analyze Python code."
        )
        return workflow.compile()

    async def analyze_code(
        self,
        python_code: str,
        file_path: str = "unknown.py",
        project_name: str = "Code",
    ) -> Dict[str, Any]:
        max_retries = 2
        for attempt in range(max_retries):
            try:
                result = await self.supervisor.ainvoke({
                    "messages": [{"role": "use    r", "content": f"Analyze this Python code:\n\n```python\n{python_code}\n```"}]
                })
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"Supervisor error for {file_path} after {max_retries} attempts: {e}")
                    return {
                        "total_smells_detected": 0,
                        "code_smells": [],
                        "agents_executed": 0,
                        "error": str(e)
                    }
                logger.warning(f"Attempt {attempt + 1} failed for {file_path}, retrying...")
                continue
        
        all_detections = []
        for name, config in AGENT_CONFIGS.items():
            try:
                structured_model = self.model.with_structured_output(config["schema"], method="json_mode")
                
                for msg in result.get("messages", []):
                    if hasattr(msg, "name") and msg.name == name:
                        parsed = await structured_model.ainvoke(msg.content)
                        
                        if hasattr(parsed, 'detections'):
                            detections = parsed.detections if parsed.detected else []
                        else:
                            detections = [parsed] if parsed.detected else []
                        
                        enriched = enrich_detections(detections, python_code, file_path, project_name, name)
                        all_detections.extend(enriched)
            except Exception as e:
                logger.warning(f"Agent {name} error for {file_path}: {e}")
                continue

        detections_as_dicts = []
        for d in all_detections:
            dict_data = d.model_dump()
            dict_data["Line no"] = dict_data.pop("Line_no", "")
            detections_as_dicts.append(dict_data)

        return {
            "total_smells_detected": len(detections_as_dicts),
            "code_smells": detections_as_dicts,
            "agents_executed": len(AGENT_CONFIGS),
        }

def get_supervisor() -> CodeSmellSupervisor:
    return CodeSmellSupervisor()


async def analyze_code_with_supervisor_v2(
    python_code: str, file_path: str = "unknown.py", project_name: str = "Code"
) -> Dict[str, Any]:
    supervisor = get_supervisor()
    return await supervisor.analyze_code(python_code, file_path, project_name)
