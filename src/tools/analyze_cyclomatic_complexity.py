import ast
import traceback

from langchain_core.tools import tool

from config.logs import logger


@tool
def analyze_cyclomatic_complexity(code: str) -> dict:
    """
    Analisa a complexidade ciclomática de funções e métodos no código Python.

    Args:
        code (str): Código Python a ser analisado.

    Returns:
        dict: Dicionário com sucesso, lista de funções e suas complexidades ou mensagem de erro.

    Exceptions:
        SyntaxError: Se o código fornecido não for um Python válido.
    """

    try:
        logger.info(f"Recebendo código para análise: {len(code)} caracteres")
        logger.info(f"Primeiros 200 caracteres: {code[:200]}")
        tree = ast.parse(code)
        result = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = 1
                for child in ast.walk(node):
                    if isinstance(
                        child,
                        (
                            ast.If,
                            ast.For,
                            ast.While,
                            ast.And,
                            ast.Or,
                            ast.ExceptHandler,
                            ast.With,
                            ast.Try,
                        ),
                    ):
                        complexity += 1

                    elif isinstance(child, ast.BoolOp):
                        complexity += len(child.values) - 1

                    lines = child.end_lineno - child.lineno if node.end_lineno else 0

                result.append(
                    {
                        "function_name": node.name,
                        "complexity": complexity,
                        "lineno": node.lineno,
                        "lines": lines,
                        "problematic": complexity > 10 or lines > 50,
                    }
                )
        return {
            "success": True,
            "functions": result,
        }

    except SyntaxError as e:
        logger.error(f"Erro: {e}")
        logger.error(f"Linha: {e.lineno}, Offset: {e.offset}")
        logger.error(f"Texto com erro: {e.text}")
        logger.error(traceback.format_exc())
        
        return {
            "success": False,
            "error": f"Erro de sintaxe ao analisar o código: {e}. Linha {e.lineno}: {e.text}",
        }
