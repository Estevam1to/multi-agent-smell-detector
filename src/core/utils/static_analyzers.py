"""Analisadores estáticos para detecção de code smells simples."""

import ast
import re
from typing import List, Dict, Any


def detect_long_statements(code: str, threshold: int = 120) -> List[Dict[str, Any]]:
    """Detecta linhas com mais de threshold caracteres."""
    detections = []
    lines = code.split("\n")

    for i, line in enumerate(lines, 1):
        line_length = len(line.rstrip())
        if line_length > threshold:
            detections.append(
                {
                    "Line_no": str(i),
                    "line_length": line_length,
                    "threshold": threshold,
                    "Description": f"Line {i} has {line_length} characters (threshold: {threshold}). Break into multiple lines.",
                    "detected": True,
                    "Smell": "Long statement",
                    "Method": "",
                }
            )

    return detections[:10]


def detect_long_identifiers(code: str, threshold: int = 20) -> List[Dict[str, Any]]:
    """Detecta identificadores com mais de threshold caracteres."""
    detections = []
    lines = code.split("\n")

    for i, line in enumerate(lines, 1):
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=", line)
        if match:
            identifier = match.group(1)
            if len(identifier) > threshold:
                detections.append(
                    {
                        "Line_no": str(i),
                        "identifier_name": identifier,
                        "length": len(identifier),
                        "threshold": threshold,
                        "Description": f"Identifier '{identifier}' has {len(identifier)} characters (threshold: {threshold}). Consider shortening.",
                        "detected": True,
                        "Smell": "Long identifier",
                        "Method": "",
                    }
                )

    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if len(node.name) > threshold:
                    detections.append(
                        {
                            "Line_no": str(node.lineno),
                            "identifier_name": node.name,
                            "length": len(node.name),
                            "threshold": threshold,
                            "Description": f"Identifier '{node.name}' has {len(node.name)} characters (threshold: {threshold}). Consider shortening.",
                            "detected": True,
                            "Smell": "Long identifier",
                            "Method": node.name
                            if isinstance(node, ast.FunctionDef)
                            else "",
                        }
                    )
    except SyntaxError:
        pass

    return detections[:10]
