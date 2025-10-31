"""Parser AST para extrair metadados de código Python."""

import ast
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class CodeParser:
    """Parser de código Python usando AST."""

    def __init__(self, code: str, file_path: Optional[str] = None):
        self.code = code
        self.file_path = file_path or "unknown.py"
        self.tree = None
        self.functions = []
        self.classes = []

        try:
            self.tree = ast.parse(code)
            self._extract_metadata()
        except SyntaxError as e:
            logger.warning(f"SyntaxError parsing {self.file_path}: {e}")

    def _extract_metadata(self):
        """Extrai funções e classes do código."""
        if not self.tree:
            return

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                self.functions.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "end_lineno": node.end_lineno or node.lineno,
                })
            elif isinstance(node, ast.ClassDef):
                self.classes.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "methods": self._get_class_methods(node),
                })

    def _get_class_methods(self, class_node) -> List[Dict]:
        """Extrai métodos de uma classe."""
        methods = []
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                methods.append({
                    "name": node.name,
                    "lineno": node.lineno,
                })
        return methods

    def find_identifier_line(self, identifier_name: str) -> Optional[int]:
        """Encontra a linha onde um identificador é definido."""
        if not self.tree:
            return None

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == identifier_name:
                        return node.lineno
            elif isinstance(node, ast.FunctionDef) and node.name == identifier_name:
                return node.lineno
            elif isinstance(node, ast.ClassDef) and node.name == identifier_name:
                return node.lineno

        return None

    def find_function_by_name(self, name: str) -> Optional[Dict]:
        """Encontra função por nome."""
        for func in self.functions:
            if func["name"] == name:
                return func

        for cls in self.classes:
            for method in cls["methods"]:
                if method["name"] == name:
                    return method

        return None

    def get_module_name(self) -> str:
        """Retorna nome do módulo."""
        if self.file_path == "unknown.py":
            return "unknown"
        return Path(self.file_path).stem

    def get_package_name(self) -> str:
        """Retorna nome do pacote."""
        if self.file_path == "unknown.py":
            return "unknown"

        path = Path(self.file_path)
        return path.parent.name if path.parent.name else "unknown"
