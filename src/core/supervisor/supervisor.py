"""Supervisor para coordenação de agentes especializados."""

import asyncio
import logging
from typing import Any, Dict, List

from langchain_openai import ChatOpenAI

from config.settings import settings
from core.supervisor.agent_config import AGENT_CONFIGS
from core.supervisor.enricher import enrich_detections

logger = logging.getLogger(__name__)


class CodeSmellSupervisor:
    """Coordena 11 agentes especializados para detectar code smells."""

    MAX_FILE_LINES = 500
    MAX_FILE_SIZE_KB = 50

    def __init__(self, parallel: bool = True):
        self.parallel = parallel
        self.model = ChatOpenAI(
            model=settings.OPENROUTER_API_MODEL,
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
            temperature=0,
        )

    def _validate_code_size(self, code: str) -> tuple[bool, str]:
        """Valida tamanho do código."""
        lines = code.split("\n")
        size_kb = len(code.encode("utf-8")) / 1024

        if len(lines) > self.MAX_FILE_LINES:
            return False, f"Arquivo muito grande: {len(lines)} linhas (max: {self.MAX_FILE_LINES})"

        if size_kb > self.MAX_FILE_SIZE_KB:
            return False, f"Arquivo muito grande: {size_kb:.1f}KB (max: {self.MAX_FILE_SIZE_KB}KB)"

        return True, ""

    async def _call_agent(self, agent_name: str, config: Dict, code: str) -> List[Any]:
        """Executa um agente individual."""
        try:
            structured_model = self.model.with_structured_output(config["schema"], method="json_mode")
            message = f"{config['prompt']}\n\n## CODE:\n```python\n{code}\n```"

            logger.info(f"[{agent_name}] Executando...")

            response = await structured_model.ainvoke([
                {"role": "system", "content": "Code smell detector. Return valid JSON."},
                {"role": "user", "content": message}
            ])

            detections = response.detections if hasattr(response, "detections") and response.detected else []
            if not detections and response.detected:
                detections = [response]

            logger.info(f"[{agent_name}] {len(detections)} detecções")
            return detections

        except Exception as e:
            logger.error(f"[{agent_name}] Erro: {e}")
            return []

    async def _analyze_parallel(self, code: str, file_path: str, project: str) -> List[Any]:
        """Executa agentes em paralelo."""
        tasks = [self._call_agent(name, cfg, code) for name, cfg in AGENT_CONFIGS.items()]
        
        logger.info(f"Executando {len(tasks)} agentes em PARALELO...")
        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_detections = []
        for (name, _), result in zip(AGENT_CONFIGS.items(), results):
            if isinstance(result, Exception):
                logger.error(f"[{name}] Falhou: {result}")
                continue
            all_detections.extend(enrich_detections(result, code, file_path, project, name))

        return all_detections

    async def _analyze_sequential(self, code: str, file_path: str, project: str) -> List[Any]:
        """Executa agentes sequencialmente."""
        all_detections = []

        for name, config in AGENT_CONFIGS.items():
            detections = await self._call_agent(name, config, code)
            all_detections.extend(enrich_detections(detections, code, file_path, project, name))
            await asyncio.sleep(0.3)

        return all_detections

    async def analyze_code(
        self, python_code: str, file_path: str = "unknown.py", project_name: str = "Code"
    ) -> Dict[str, Any]:
        """Analisa código e retorna code smells detectados."""
        valid, error = self._validate_code_size(python_code)
        if not valid:
            logger.warning(f"Arquivo rejeitado: {error}")
            return {"total_smells_detected": 0, "code_smells": [], "agents_executed": 0, "error": error}

        detections = await (
            self._analyze_parallel(python_code, file_path, project_name)
            if self.parallel
            else self._analyze_sequential(python_code, file_path, project_name)
        )

        results = []
        for d in detections:
            data = d.model_dump()
            data["Line no"] = data.pop("Line_no", "")
            results.append(data)

        return {
            "total_smells_detected": len(results),
            "code_smells": results,
            "agents_executed": len(AGENT_CONFIGS),
        }


def get_supervisor(parallel: bool = True) -> CodeSmellSupervisor:
    """Factory para criar supervisor."""
    return CodeSmellSupervisor(parallel=parallel)


async def analyze_code(
    python_code: str, file_path: str = "unknown.py", project_name: str = "Code", parallel: bool = True
) -> Dict[str, Any]:
    """Analisa código Python e retorna code smells."""
    return await get_supervisor(parallel).analyze_code(python_code, file_path, project_name)
