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
    """Enriquece detecções com metadados do projeto e corrige números de linha."""
    parser = CodeParser(python_code, file_path)
    valid_detections = []
    
    for detection in detections:
        if not detection.detected:
            continue
            
        if not detection.Description:
            logger.warning(f"Detecção sem descrição ignorada em {agent_name}")
            continue
        
        # Corrige número de linha usando CodeParser
        if hasattr(detection, 'identifier_name') and detection.identifier_name:
            correct_line = parser.find_identifier_line(detection.identifier_name)
            if correct_line:
                detection.Line_no = str(correct_line)
        elif hasattr(detection, 'Method') and detection.Method:
            func = parser.find_function_by_name(detection.Method)
            if func:
                detection.Line_no = str(func['lineno'])
        
        if not detection.Line_no:
            logger.warning(f"Detecção sem linha ignorada em {agent_name}: {detection.Description}")
            continue
        
        detection.Project = project_name
        detection.Package = parser.get_package_name()
        detection.Module = parser.get_module_name()
        detection.File = file_path
        valid_detections.append(detection)
    
    return valid_detections
