"""Enriquece detecções com metadados do projeto."""

import logging
from typing import List, Any

from core.utils.code_parser import CodeParser

logger = logging.getLogger(__name__)


def enrich_detections(
    detections: List[Any],
    python_code: str,
    file_path: str,
    project_name: str,
    agent_name: str
) -> List[Any]:
    """Enriquece detecções com metadados do projeto."""
    parser = CodeParser(python_code, file_path)
    valid_detections = []
    
    for detection in detections:
        if not detection.detected:
            continue
            
        if not detection.Line_no or not detection.Description:
            logger.warning(f"Detecção incompleta ignorada em {agent_name}")
            continue
        
        detection.Project = project_name
        detection.Package = parser.get_package_name()
        detection.Module = parser.get_module_name()
        detection.File = file_path
        valid_detections.append(detection)
    
    return valid_detections
