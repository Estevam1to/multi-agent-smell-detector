#!/usr/bin/env python3
"""
Script para executar Pylint e gerar CSV com code smells específicos.
Foca apenas nos mesmos code smells detectados pelo agente:
- R0902: God Classes (too-many-instance-attributes)
- R0915: Long Methods (too-many-statements)
- R0912: Too Many Branches (too-many-branches)
- R0913: Too Many Arguments (too-many-arguments)
"""

import json
import subprocess
import csv
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any


def run_pylint_on_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Executa Pylint em um arquivo específico e retorna os resultados filtrados.

    Args:
        file_path: Caminho para o arquivo Python

    Returns:
        Lista de dicionários com os code smells encontrados
    """
    # Códigos específicos que o agente detecta
    enable_codes = "R0902,R0915,R0912,R0913"

    pylint_cmd = [
        "pylint",
        "--exit-zero",
        "--output-format=json",
        f"--enable={enable_codes}",
        "--disable=all",
        file_path,
    ]

    try:
        result = subprocess.run(pylint_cmd, capture_output=True, text=True, check=False)

        if result.stderr:
            print(f"Warning for {file_path}: {result.stderr}", file=sys.stderr)

        if result.stdout:
            return json.loads(result.stdout)
        else:
            return []

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for {file_path}: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error running Pylint on {file_path}: {e}", file=sys.stderr)
        return []


def get_code_smell_type(message_id: str) -> str:
    """
    Mapeia o código do Pylint para o tipo de code smell.

    Args:
        message_id: Código do Pylint (ex: R0902)

    Returns:
        Nome descritivo do code smell
    """
    mapping = {
        "R0902": "God Class",
        "R0915": "Long Method",
        "R0912": "Too Many Branches",
        "R0913": "Too Many Arguments",
    }
    return mapping.get(message_id, message_id)


def get_risk_description(message_id: str) -> str:
    """
    Retorna a descrição do risco para cada tipo de code smell.

    Args:
        message_id: Código do Pylint

    Returns:
        Descrição do risco
    """
    risks = {
        "R0902": "Classes with too many responsibilities violate Single Responsibility Principle and are hard to maintain",
        "R0915": "Long methods are difficult to test, understand and maintain",
        "R0912": "Too many branches increase cyclomatic complexity making code hard to test and understand",
        "R0913": "Too many parameters make functions difficult to invoke, test and understand",
    }
    return risks.get(message_id, "Code quality issue detected")


def process_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Processa múltiplos arquivos Python e coleta todos os code smells.

    Args:
        file_paths: Lista de caminhos para arquivos Python

    Returns:
        Lista consolidada de code smells
    """
    all_code_smells = []

    for file_path in file_paths:
        print(f"Analisando: {file_path}")
        pylint_results = run_pylint_on_file(file_path)

        for result in pylint_results:
            code_smell = {
                "file": file_path,
                "type": get_code_smell_type(result.get("message-id", "")),
                "message_id": result.get("message-id", ""),
                "description": result.get("message", ""),
                "risk": get_risk_description(result.get("message-id", "")),
                "line": result.get("line", ""),
                "column": result.get("column", ""),
                "symbol": result.get("symbol", ""),
                "obj": result.get("obj", ""),
            }
            all_code_smells.append(code_smell)

    return all_code_smells


def save_to_csv(code_smells: List[Dict[str, Any]], output_file: str):
    """
    Salva os code smells em um arquivo CSV.

    Args:
        code_smells: Lista de code smells
        output_file: Caminho do arquivo CSV de saída
    """
    if not code_smells:
        print("Nenhum code smell encontrado.")
        return

    # Cria o diretório se não existir
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "file",
        "type",
        "message_id",
        "description",
        "risk",
        "line",
        "column",
        "symbol",
        "obj",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(code_smells)

    print(f"Resultados salvos em: {output_file}")
    print(f"Total de code smells encontrados: {len(code_smells)}")


def find_python_files(directory: str) -> List[str]:
    """
    Encontra todos os arquivos Python em um diretório.

    Args:
        directory: Diretório para buscar

    Returns:
        Lista de caminhos para arquivos Python
    """
    python_files = []
    path = Path(directory)

    if path.is_file() and path.suffix == ".py":
        return [str(path)]

    if path.is_dir():
        for py_file in path.rglob("*.py"):
            # Ignora arquivos em __pycache__
            if "__pycache__" not in str(py_file):
                python_files.append(str(py_file))

    return python_files


def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(
        description="Executa Pylint e gera CSV com code smells específicos"
    )
    parser.add_argument("input_path", help="Arquivo Python ou diretório para analisar")
    parser.add_argument(
        "-o",
        "--output",
        default="results/pylint_code_smells.csv",
        help="Arquivo CSV de saída (default: results/pylint_code_smells.csv)",
    )

    args = parser.parse_args()

    # Verifica se o caminho existe
    if not Path(args.input_path).exists():
        print(f"Erro: Caminho não encontrado: {args.input_path}", file=sys.stderr)
        sys.exit(1)

    # Encontra arquivos Python
    python_files = find_python_files(args.input_path)

    if not python_files:
        print("Nenhum arquivo Python encontrado.", file=sys.stderr)
        sys.exit(1)

    print(f"Encontrados {len(python_files)} arquivo(s) Python para analisar")

    # Processa os arquivos
    code_smells = process_files(python_files)

    # Salva no CSV
    save_to_csv(code_smells, args.output)

    # Mostra resumo por tipo
    if code_smells:
        print("\nResumo por tipo de code smell:")
        smell_counts = {}
        for smell in code_smells:
            smell_type = smell["type"]
            smell_counts[smell_type] = smell_counts.get(smell_type, 0) + 1

        for smell_type, count in smell_counts.items():
            print(f"  {smell_type}: {count}")


if __name__ == "__main__":
    main()
