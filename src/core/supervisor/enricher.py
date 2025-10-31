"""Enriquecimento e validação de detecções."""

import logging
from typing import List, Any

from core.utils.code_parser import CodeParser

logger = logging.getLogger(__name__)


def _is_false_positive(detection: Any) -> bool:
    """Verifica se detecção é falso positivo."""
    if hasattr(detection, "identifier_name") and hasattr(detection, "length"):
        if detection.length <= 20:
            logger.debug(f"Falso positivo: {detection.identifier_name} ({detection.length} chars)")
            return True

    if detection.Smell == "Magic number":
        desc = detection.Description.lower()
        if any(f"magic number {n}" in desc for n in ["0", "1", "-1"]):
            logger.debug("Falso positivo: Magic number trivial")
            return True

    if hasattr(detection, "total_lines") and hasattr(detection, "threshold"):
        if detection.Smell == "Long method" and detection.total_lines <= detection.threshold:
            logger.debug(f"Falso positivo: Método com {detection.total_lines} linhas")
            return True

    return False


def enrich_detections(
    detections: List[Any], code: str, file_path: str, project: str, agent: str
) -> List[Any]:
    """Enriquece detecções com metadados e filtra falsos positivos."""
    parser = CodeParser(code, file_path)
    valid = []

    for d in detections:
        if not d.detected or not d.Description:
            continue

        if _is_false_positive(d):
            continue

        if hasattr(d, "identifier_name") and d.identifier_name:
            line = parser.find_identifier_line(d.identifier_name)
            if line:
                d.Line_no = str(line)
        elif hasattr(d, "Method") and d.Method:
            func = parser.find_function_by_name(d.Method)
            if func:
                d.Line_no = str(func["lineno"])

        if not d.Line_no:
            logger.warning(f"[{agent}] Detecção sem linha: {d.Description}")
            continue

        d.Project = project
        d.Package = parser.get_package_name()
        d.Module = parser.get_module_name()
        d.File = file_path
        valid.append(d)

    return valid
