"""
Módulo para parsear código Python e extrair metadados estruturados.

Extrai informações como funções, classes, linhas, etc.
"""

import ast
from typing import Dict, List, Any, Optional


class CodeParser:
    """Parser para extrair metadados estruturados de código Python."""

    def __init__(self, code: str, file_path: Optional[str] = None):
        """
        Inicializa o parser com o código a ser analisado.

        Args:
            code: Código Python a ser parseado
            file_path: Caminho do arquivo (opcional)
        """
        self.code = code
        self.file_path = file_path or "unknown.py"
        self.tree = None
        self.functions = []
        self.classes = []

        try:
            self.tree = ast.parse(code)
            self._extract_metadata()
        except SyntaxError:
            # Se houver erro de sintaxe, mantém listas vazias
            pass

    def _extract_metadata(self):
        """Extrai metadados do código (funções, classes, etc.)."""
        if not self.tree:
            return

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                self.functions.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "end_lineno": node.end_lineno or node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                    "decorators": [self._get_decorator_name(d) for d in node.decorator_list],
                })
            elif isinstance(node, ast.ClassDef):
                self.classes.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "end_lineno": node.end_lineno or node.lineno,
                    "methods": self._get_class_methods(node),
                })

    def _get_decorator_name(self, decorator) -> str:
        """Extrai o nome de um decorator."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
        return "unknown"

    def _get_class_methods(self, class_node) -> List[Dict[str, Any]]:
        """Extrai métodos de uma classe."""
        methods = []
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                methods.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "end_lineno": node.end_lineno or node.lineno,
                })
        return methods

    def get_function_at_line(self, line: int) -> Optional[Dict[str, Any]]:
        """
        Retorna informações da função que contém a linha especificada.

        Args:
            line: Número da linha

        Returns:
            Dicionário com informações da função ou None
        """
        for func in self.functions:
            if func["lineno"] <= line <= func["end_lineno"]:
                return func

        # Verifica em métodos de classes
        for cls in self.classes:
            for method in cls["methods"]:
                if method["lineno"] <= line <= method["end_lineno"]:
                    return {
                        **method,
                        "class": cls["name"]
                    }

        return None

    def get_class_at_line(self, line: int) -> Optional[str]:
        """
        Retorna o nome da classe que contém a linha especificada.

        Args:
            line: Número da linha

        Returns:
            Nome da classe ou None
        """
        for cls in self.classes:
            if cls["lineno"] <= line <= cls["end_lineno"]:
                return cls["name"]
        return None

    def get_module_name(self) -> str:
        """
        Extrai o nome do módulo a partir do caminho do arquivo.

        Returns:
            Nome do módulo
        """
        if self.file_path == "unknown.py":
            return "unknown"

        # Remove extensão .py e pega apenas o nome do arquivo
        return self.file_path.split("/")[-1].replace(".py", "")

    def get_package_name(self) -> str:
        """
        Extrai o nome do pacote a partir do caminho do arquivo.

        Returns:
            Nome do pacote
        """
        if self.file_path == "unknown.py":
            return "unknown"

        parts = self.file_path.split("/")
        if len(parts) > 1:
            return parts[-2]
        return "unknown"

    def find_function_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Busca uma função pelo nome.

        Args:
            name: Nome da função

        Returns:
            Dicionário com informações da função ou None
        """
        for func in self.functions:
            if func["name"] == name:
                return func

        # Verifica em métodos de classes
        for cls in self.classes:
            for method in cls["methods"]:
                if method["name"] == name:
                    return {
                        **method,
                        "class": cls["name"]
                    }

        return None

    def count_parameters(self, function_name: str) -> int:
        """
        Conta o número de parâmetros de uma função.

        Args:
            function_name: Nome da função

        Returns:
            Número de parâmetros
        """
        func = self.find_function_by_name(function_name)
        if func and "args" in func:
            return len(func["args"])
        return 0

    def get_all_functions(self) -> List[Dict[str, Any]]:
        """
        Retorna todas as funções encontradas no código.

        Returns:
            Lista de funções
        """
        all_funcs = self.functions.copy()

        # Adiciona métodos de classes
        for cls in self.classes:
            for method in cls["methods"]:
                all_funcs.append({
                    **method,
                    "class": cls["name"]
                })

        return all_funcs

    def calculate_cyclomatic_complexity(self, function_name: str) -> int:
        """
        Calcula a complexidade ciclomática aproximada de uma função.

        Args:
            function_name: Nome da função

        Returns:
            Complexidade ciclomática (aproximada)
        """
        func = self.find_function_by_name(function_name)
        if not func:
            return 0

        # Encontra o nó da função na árvore
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                return self._calculate_cc_for_node(node)

        return 0

    def _calculate_cc_for_node(self, node) -> int:
        """
        Calcula CC de um nó da AST.

        CC = 1 + número de pontos de decisão
        """
        cc = 1
        for child in ast.walk(node):
            # Pontos de decisão
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                cc += 1
            elif isinstance(child, ast.BoolOp):
                # and/or contam como decisões
                cc += len(child.values) - 1

        return cc
