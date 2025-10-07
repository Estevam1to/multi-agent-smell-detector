import ast
import traceback
from typing import Any, Dict

from langchain_core.tools import tool

from config.logs import logger


@tool
def analyze_class_structure(code: str) -> Dict[str, Any]:
    """
    Analisa a estrutura de classes: número de métodos, atributos, LOC.
    Detecta Large Class e God Class patterns.

    Args:
        code (str): Código Python a ser analisado.

    Returns:
        dict: Dicionário com sucesso, total de classes e detalhes de cada classe ou mensagem de erro

    Exceptions:
        SyntaxError: Se o código fornecido não for um Python válido.
    """
    try:
        tree = ast.parse(code)
        results = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                public_methods = [m for m in methods if not m.name.startswith("_")]

                attributes = set()
                for item in ast.walk(node):
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Attribute):
                                attributes.add(target.attr)

                lines = node.end_lineno - node.lineno if node.end_lineno else 0

                bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        bases.append(base.id)

                results.append(
                    {
                        "class": node.name,
                        "line": node.lineno,
                        "num_methods": len(methods),
                        "num_public_methods": len(public_methods),
                        "num_attributes": len(attributes),
                        "lines": lines,
                        "inheritance": bases,
                        "large_class": len(methods) > 20 or lines > 300,
                        "god_class": len(methods) > 30 or len(attributes) > 15,
                    }
                )

        return {"success": True, "total_classes": len(results), "classes": results}
    except SyntaxError as e:
        logger.error(f"Erro: {e}")
        logger.error(f"Linha: {e.lineno}, Offset: {e.offset}")
        logger.error(f"Texto com erro: {e.text}")
        logger.error(traceback.format_exc())
        
        return {
            "success": False,
            "error": f"Erro de sintaxe ao analisar o código: {e}. Linha {e.lineno}: {e.text}",
        }
    except Exception as e:
        logger.error(f"Erro ao analisar estrutura de classes: {e}")
        logger.error(traceback.format_exc())
        return {"success": False, "error": str(e)}
