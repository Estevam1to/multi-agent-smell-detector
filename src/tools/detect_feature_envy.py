import ast
import traceback
from typing import Any, Dict

from langchain_core.tools import tool

from config.logs import logger


@tool
def detect_feature_envy(code: str) -> Dict[str, Any]:
    """
    Detecta Feature Envy: métodos que usam mais atributos/métodos de outras classes
    do que da própria classe.

    Args:
        code (str): Código Python a ser analisado.

    Returns:
        dict: Dicionário com sucesso, número de problemas encontrados e detalhes ou mensagem de erro

    Exceptions:
        SyntaxError: Se o código fornecido não for um Python válido.
    """
    try:
        tree = ast.parse(code)
        problems = []
    
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for method in [n for n in node.body if isinstance(n, ast.FunctionDef)]:
                    external_accesses = 0
                    for child in ast.walk(method):
                        if isinstance(child, ast.Attribute):
                            if (
                                isinstance(child.value, ast.Name)
                                and child.value.id != "self"
                            ):
                                external_accesses += 1

                    if external_accesses > 5:
                        problems.append(
                            {
                                "class": node.name,
                                "method": method.name,
                                "line": method.lineno,
                                "external_accesses": external_accesses,
                            }
                        )

        return {"success": True, "problems_found": len(problems), "problems": problems}
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
        logger.error(f"Erro ao detectar feature envy: {e}")
        logger.error(traceback.format_exc())
        return {"success": False, "error": str(e)}
