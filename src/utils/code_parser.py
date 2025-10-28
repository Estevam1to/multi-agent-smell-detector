"""Módulo para parsear código Python e extrair metadados estruturados."""

import ast
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class CodeParser:

    def __init__(self, code: str, file_path: Optional[str] = None):
        self.code = code
        self.file_path = file_path or "unknown.py"
        self.tree = None
        self.functions = []
        self.classes = []
        self.parse_error = None

        try:
            self.tree = ast.parse(code)
            self._extract_metadata()
        except SyntaxError as e:
            self.parse_error = e
            logger.warning(f"SyntaxError parsing {self.file_path}: {e}")

    def _extract_metadata(self):
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
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
        return "unknown"

    def _get_class_methods(self, class_node) -> List[Dict[str, Any]]:
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
        for func in self.functions:
            if func["lineno"] <= line <= func["end_lineno"]:
                return func

        for cls in self.classes:
            for method in cls["methods"]:
                if method["lineno"] <= line <= method["end_lineno"]:
                    return {**method, "class": cls["name"]}

        return None

    def get_class_at_line(self, line: int) -> Optional[str]:
        for cls in self.classes:
            if cls["lineno"] <= line <= cls["end_lineno"]:
                return cls["name"]
        return None

    def get_module_name(self) -> str:
        if self.file_path == "unknown.py":
            return "unknown"
        return Path(self.file_path).stem

    def get_package_name(self) -> str:
        if self.file_path == "unknown.py":
            return "unknown"

        path = Path(self.file_path)
        if path.parent.name:
            return path.parent.name
        return "unknown"

    def find_function_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        for func in self.functions:
            if func["name"] == name:
                return func

        for cls in self.classes:
            for method in cls["methods"]:
                if method["name"] == name:
                    return {**method, "class": cls["name"]}

        return None

    def count_parameters(self, function_name: str) -> int:
        func = self.find_function_by_name(function_name)
        if func and "args" in func:
            return len(func["args"])
        return 0

    def get_all_functions(self) -> List[Dict[str, Any]]:
        all_funcs = self.functions.copy()

        for cls in self.classes:
            for method in cls["methods"]:
                all_funcs.append({**method, "class": cls["name"]})

        return all_funcs

    def calculate_cyclomatic_complexity(self, function_name: str) -> int:
        func = self.find_function_by_name(function_name)
        if not func:
            return 0

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                return self._calculate_cc_for_node(node)

        return 0

    def _calculate_cc_for_node(self, node) -> int:
        cc = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                cc += 1
            elif isinstance(child, ast.BoolOp):
                cc += len(child.values) - 1

        return cc
