"""Tool para agentes LLM entenderem a estrutura do código."""

import ast
from typing import Dict, Any
from langchain_core.tools import tool


@tool
def get_code_structure(code: str) -> Dict[str, Any]:
    """Retorna a estrutura do código Python (funções, classes, linhas).
    
    Esta ferramenta NÃO detecta code smells, apenas fornece informações estruturais.
    
    Args:
        code: Código Python para analisar
        
    Returns:
        Dicionário com total_lines, functions, classes
    """
    try:
        tree = ast.parse(code)
        lines = code.split('\n')
        
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'start_line': node.lineno,
                    'end_line': node.end_lineno or node.lineno,
                    'total_lines': (node.end_lineno or node.lineno) - node.lineno + 1,
                    'parameters': [arg.arg for arg in node.args.args],
                    'parameter_count': len(node.args.args)
                })
            elif isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append({
                            'name': item.name,
                            'start_line': item.lineno,
                            'end_line': item.end_lineno or item.lineno
                        })
                
                classes.append({
                    'name': node.name,
                    'start_line': node.lineno,
                    'end_line': node.end_lineno or node.lineno,
                    'methods': methods
                })
        
        return {
            'total_lines': len(lines),
            'functions': functions,
            'classes': classes,
            'has_functions': len(functions) > 0,
            'has_classes': len(classes) > 0
        }
    
    except SyntaxError as e:
        return {
            'error': f'Syntax error: {str(e)}',
            'total_lines': len(code.split('\n')),
            'functions': [],
            'classes': []
        }
