"""
Módulo para formatar resultados no formato compatível com DPy.

Converte os resultados do sistema para o formato JSON usado pela ferramenta DPy.
"""

import re
from typing import Dict, List, Any, Optional
from utils.code_parser import CodeParser


class DPyFormatter:
    """Formatador para converter resultados no formato DPy."""

    # Mapeamento de smell_type para nome do smell no formato DPy
    SMELL_MAPPING = {
        "long_method": "Long method",
        "long_parameter_list": "Long parameter list",
        "long_statement": "Long statement",
        "long_identifier": "Long identifier",
        "empty_catch_block": "Empty catch block",
        "complex_method": "Complex method",
        "complex_conditional": "Complex conditional",
        "missing_default": "Missing default",
        "long_lambda_function": "Long lambda function",
        "long_message_chain": "Long message chain",
        "magic_number": "Magic number",
    }

    def __init__(self, code: str, file_path: Optional[str] = None):
        """
        Inicializa o formatador.

        Args:
            code: Código Python analisado
            file_path: Caminho do arquivo (opcional)
        """
        self.parser = CodeParser(code, file_path)
        self.code_lines = code.split("\n")

    def format_results(
        self, code_smells: List[Dict[str, Any]], project_name: str = "Code"
    ) -> List[Dict[str, Any]]:
        """
        Formata os resultados no formato DPy.

        Args:
            code_smells: Lista de code smells detectados
            project_name: Nome do projeto (padrão: "Code")

        Returns:
            Lista de code smells no formato DPy
        """
        dpy_results = []

        for smell in code_smells:
            dpy_smell = self._convert_smell_to_dpy(smell, project_name)
            if dpy_smell:
                dpy_results.append(dpy_smell)

        return dpy_results

    def _convert_smell_to_dpy(
        self, smell: Dict[str, Any], project_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Converte um smell individual para o formato DPy.

        Args:
            smell: Dicionário com smell_type e findings
            project_name: Nome do projeto

        Returns:
            Dicionário no formato DPy ou None se não puder converter
        """
        smell_type = smell.get("smell_type", "")
        findings = smell.get("findings", "")

        # Extrai informações estruturadas dos findings
        metadata = self._extract_metadata_from_findings(findings, smell_type)

        # Se não conseguiu extrair metadados, usa valores padrão
        if not metadata:
            metadata = {
                "method": "unknown",
                "line_no": "unknown",
                "class": "",
            }

        # Busca informações adicionais no parser
        method_name = metadata.get("method", "unknown")
        if method_name != "unknown":
            func_info = self.parser.find_function_by_name(method_name)
            if func_info:
                metadata["line_no"] = f"{func_info['lineno']}"
                if "end_lineno" in func_info:
                    metadata["line_no"] = f"{func_info['lineno']} - {func_info['end_lineno']}"
                if "class" in func_info:
                    metadata["class"] = func_info["class"]

        # Cria descrição em inglês
        description = self._create_description(smell_type, findings, metadata)

        return {
            "Project": project_name,
            "Package": self.parser.get_package_name() or project_name,
            "Module": self.parser.get_module_name(),
            "Class": metadata.get("class", ""),
            "Smell": self.SMELL_MAPPING.get(smell_type, smell_type.replace("_", " ").title()),
            "Method": metadata.get("method", ""),
            "Line no": metadata.get("line_no", "unknown"),
            "File": self.parser.file_path,
            "Description": description,
        }

    def _extract_metadata_from_findings(
        self, findings: str, smell_type: str
    ) -> Dict[str, Any]:
        """
        Extrai metadados estruturados dos findings (texto livre do LLM).

        Args:
            findings: Texto com os findings do agente
            smell_type: Tipo do smell

        Returns:
            Dicionário com metadados extraídos
        """
        metadata = {}

        # Tenta extrair nome da função/método
        # Padrões comuns: "função X", "método Y", "def nome"
        function_patterns = [
            r"função\s+['\"]?(\w+)['\"]?",
            r"método\s+['\"]?(\w+)['\"]?",
            r"def\s+(\w+)",
            r"Function\s+['\"]?(\w+)['\"]?",
            r"Method\s+['\"]?(\w+)['\"]?",
        ]

        for pattern in function_patterns:
            match = re.search(pattern, findings, re.IGNORECASE)
            if match:
                metadata["method"] = match.group(1)
                break

        # Se não encontrou nome de função, tenta pegar todas as funções do código
        if "method" not in metadata:
            all_functions = self.parser.get_all_functions()
            if all_functions:
                # Usa a primeira função encontrada como padrão
                metadata["method"] = all_functions[0]["name"]
                if "class" in all_functions[0]:
                    metadata["class"] = all_functions[0]["class"]

        # Tenta extrair número de linha
        line_patterns = [
            r"linha\s+(\d+)",
            r"line\s+(\d+)",
            r"linhas?\s+(\d+)\s*-\s*(\d+)",
        ]

        for pattern in line_patterns:
            match = re.search(pattern, findings, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    metadata["line_no"] = f"{match.group(1)} - {match.group(2)}"
                else:
                    metadata["line_no"] = match.group(1)
                break

        return metadata

    def _create_description(
        self, smell_type: str, findings: str, metadata: Dict[str, Any]
    ) -> str:
        """
        Cria uma descrição em inglês no estilo DPy.

        Args:
            smell_type: Tipo do smell
            findings: Findings originais do agente
            metadata: Metadados extraídos

        Returns:
            Descrição formatada
        """
        method = metadata.get("method", "unknown")
        smell_name = self.SMELL_MAPPING.get(smell_type, smell_type.replace("_", " ").title())

        # Templates específicos para cada tipo de smell
        if smell_type == "long_method":
            lines = self._extract_number(findings, ["linha", "line"])
            if lines:
                return f"Method '{method}' has {lines} lines, exceeding the max of 67."
            return f"Method '{method}' is too long, exceeding the recommended maximum of 67 lines."

        elif smell_type == "long_parameter_list":
            params = self._extract_number(findings, ["parâmetro", "parameter"])
            if not params:
                params = self.parser.count_parameters(method)
            if params:
                return f"Method '{method}' has {params} parameters, more than the recommended maximum 4 parameters."
            return f"Method '{method}' has too many parameters, more than the recommended maximum 4 parameters."

        elif smell_type == "complex_method":
            cc = self._extract_number(findings, ["complexidade", "complexity", "CC"])
            if cc:
                return f"Method '{method}' has a cyclomatic complexity of {cc}, exceeding the max of 7."
            return f"Method '{method}' has high cyclomatic complexity, exceeding the max of 7."

        elif smell_type == "complex_conditional":
            conditions = self._extract_number(findings, ["condição", "condition", "operador", "operator"])
            if conditions:
                return f"A conditional in {method} has {conditions} conditions, more than the recommended maximum 3 conditions."
            return f"A conditional in {method} has too many conditions, more than the recommended maximum 3 conditions."

        elif smell_type == "long_statement":
            chars = self._extract_number(findings, ["caractere", "character", "coluna", "column"])
            if chars:
                return f"Statement in {method} has {chars} characters, exceeding the max of 80."
            return f"Statement in {method} is too long, exceeding the recommended maximum of 80 characters."

        elif smell_type == "long_identifier":
            chars = self._extract_number(findings, ["caractere", "character"])
            identifier = self._extract_identifier(findings)
            if identifier and chars:
                return f"Identifier '{identifier}' has {chars} characters, exceeding the max of 20."
            elif identifier:
                return f"Identifier '{identifier}' is too long, exceeding the recommended maximum of 20 characters."
            return f"An identifier in {method} is too long, exceeding the recommended maximum of 20 characters."

        elif smell_type == "magic_number":
            numbers = self._extract_magic_numbers(findings)
            if numbers:
                return f"Magic number(s) {', '.join(numbers)} detected in {method}. Suggestion: create named constants."
            return f"Magic number detected in {method}. Suggestion: create named constants."

        elif smell_type == "empty_catch_block":
            return f"Method '{method}' contains an empty catch block that silences exceptions."

        elif smell_type == "missing_default":
            return f"Match statement in {method} is missing a default case."

        elif smell_type == "long_lambda_function":
            chars = self._extract_number(findings, ["caractere", "character"])
            if chars:
                return f"Lambda function in {method} has {chars} characters, exceeding the max of 80."
            return f"Lambda function in {method} is too long, exceeding the recommended maximum of 80 characters."

        elif smell_type == "long_message_chain":
            chain_length = self._extract_number(findings, ["método", "method", "encadeamento", "chain"])
            if chain_length:
                return f"Message chain in {method} has {chain_length} methods, more than the recommended maximum 2 methods."
            return f"Message chain in {method} is too long, more than the recommended maximum 2 methods."

        # Descrição genérica
        return f"{smell_name} detected in {method}. {findings[:100]}"

    def _extract_number(self, text: str, keywords: List[str]) -> Optional[int]:
        """
        Extrai um número do texto baseado em keywords.

        Args:
            text: Texto para buscar
            keywords: Lista de palavras-chave para buscar antes do número

        Returns:
            Número extraído ou None
        """
        for keyword in keywords:
            # Busca padrões como "X parametros", "parametros: X", etc.
            patterns = [
                rf"(\d+)\s*{keyword}",
                rf"{keyword}\s*:?\s*(\d+)",
            ]

            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return int(match.group(1))

        return None

    def _extract_identifier(self, text: str) -> Optional[str]:
        """
        Extrai o nome do identificador mencionado no texto.

        Args:
            text: Texto para buscar

        Returns:
            Nome do identificador ou None
        """
        patterns = [
            r"identificador\s+['\"]([^'\"]+)['\"]",
            r"identifier\s+['\"]([^'\"]+)['\"]",
            r"variável\s+['\"]([^'\"]+)['\"]",
            r"variable\s+['\"]([^'\"]+)['\"]",
            r"['\"]([a-zA-Z_][a-zA-Z0-9_]{20,})['\"]",  # Identificador longo
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    def _extract_magic_numbers(self, text: str) -> List[str]:
        """
        Extrai magic numbers mencionados no texto.

        Args:
            text: Texto para buscar

        Returns:
            Lista de magic numbers como strings
        """
        # Busca por padrões de números (inteiros ou decimais)
        patterns = [
            r"número\s+mágico\s+(\d+\.?\d*)",
            r"magic\s+number\s+(\d+\.?\d*)",
            r"(\d+\.?\d+)",  # Qualquer número
        ]

        numbers = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                num = match.group(1)
                if num not in numbers:
                    numbers.append(num)

        return numbers[:3]  # Limita a 3 números para não poluir
