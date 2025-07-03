#!/usr/bin/env python3
"""
Script para executar Bandit e gerar CSV com vulnerabilidades de segurança.
Foca em detectar vulnerabilidades de segurança em código Python.
"""

import json
import subprocess
import csv
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any


def run_bandit_on_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Executa Bandit em um arquivo específico e retorna os resultados.

    Args:
        file_path: Caminho para o arquivo Python

    Returns:
        Lista de dicionários com as vulnerabilidades encontradas
    """
    bandit_cmd = ["bandit", "-f", "json", file_path]

    try:
        result = subprocess.run(bandit_cmd, capture_output=True, text=True, check=False)

        if result.stderr:
            print(f"Warning for {file_path}: {result.stderr}", file=sys.stderr)

        if result.stdout:
            bandit_output = json.loads(result.stdout)
            return bandit_output.get("results", [])
        else:
            return []

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for {file_path}: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error running Bandit on {file_path}: {e}", file=sys.stderr)
        return []


def get_severity_description(severity: str) -> str:
    """
    Retorna a descrição do nível de severidade.

    Args:
        severity: Nível de severidade (LOW, MEDIUM, HIGH)

    Returns:
        Descrição da severidade
    """
    descriptions = {
        "LOW": "Low risk security issue that should be reviewed",
        "MEDIUM": "Medium risk security vulnerability that should be addressed",
        "HIGH": "High risk security vulnerability that requires immediate attention",
    }
    return descriptions.get(severity.upper(), "Unknown severity level")


def get_confidence_description(confidence: str) -> str:
    """
    Retorna a descrição do nível de confiança.

    Args:
        confidence: Nível de confiança (LOW, MEDIUM, HIGH)

    Returns:
        Descrição da confiança
    """
    descriptions = {
        "LOW": "Low confidence - may be false positive",
        "MEDIUM": "Medium confidence - likely a real issue",
        "HIGH": "High confidence - very likely a real security issue",
    }
    return descriptions.get(confidence.upper(), "Unknown confidence level")


def process_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Processa múltiplos arquivos Python e coleta todas as vulnerabilidades.

    Args:
        file_paths: Lista de caminhos para arquivos Python

    Returns:
        Lista consolidada de vulnerabilidades
    """
    all_vulnerabilities = []

    for file_path in file_paths:
        print(f"Analisando: {file_path}")
        bandit_results = run_bandit_on_file(file_path)

        for result in bandit_results:
            vulnerability = {
                "file": file_path,
                "test_id": result.get("test_id", ""),
                "test_name": result.get("test_name", ""),
                "issue_severity": result.get("issue_severity", ""),
                "issue_confidence": result.get("issue_confidence", ""),
                "issue_text": result.get("issue_text", ""),
                "line_number": result.get("line_number", ""),
                "line_range": f"{result.get('line_range', [''])[0]}-{result.get('line_range', ['', ''])[-1]}"
                if result.get("line_range")
                else "",
                "code": result.get("code", "").strip(),
                "severity_description": get_severity_description(
                    result.get("issue_severity", "")
                ),
                "confidence_description": get_confidence_description(
                    result.get("issue_confidence", "")
                ),
                "more_info": result.get("more_info", ""),
            }
            all_vulnerabilities.append(vulnerability)

    return all_vulnerabilities


def save_to_csv(vulnerabilities: List[Dict[str, Any]], output_file: str):
    """
    Salva as vulnerabilidades em um arquivo CSV.

    Args:
        vulnerabilities: Lista de vulnerabilidades
        output_file: Caminho do arquivo CSV de saída
    """
    if not vulnerabilities:
        print("Nenhuma vulnerabilidade encontrada.")
        return

    # Cria o diretório se não existir
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "file",
        "test_id",
        "test_name",
        "issue_severity",
        "issue_confidence",
        "issue_text",
        "line_number",
        "line_range",
        "code",
        "severity_description",
        "confidence_description",
        "more_info",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(vulnerabilities)

    print(f"Resultados salvos em: {output_file}")
    print(f"Total de vulnerabilidades encontradas: {len(vulnerabilities)}")


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
        description="Executa Bandit e gera CSV com vulnerabilidades de segurança"
    )
    parser.add_argument("input_path", help="Arquivo Python ou diretório para analisar")
    parser.add_argument(
        "-o",
        "--output",
        default="results/bandit_security_issues.csv",
        help="Arquivo CSV de saída (default: results/bandit_security_issues.csv)",
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
    vulnerabilities = process_files(python_files)

    # Salva no CSV
    save_to_csv(vulnerabilities, args.output)

    # Mostra resumo por severidade
    if vulnerabilities:
        print("\nResumo por severidade:")
        severity_counts = {}
        for vuln in vulnerabilities:
            severity = vuln["issue_severity"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        for severity, count in severity_counts.items():
            print(f"  {severity}: {count}")

        print("\nResumo por tipo de teste:")
        test_counts = {}
        for vuln in vulnerabilities:
            test_name = vuln["test_name"]
            test_counts[test_name] = test_counts.get(test_name, 0) + 1

        for test_name, count in sorted(test_counts.items()):
            print(f"  {test_name}: {count}")


if __name__ == "__main__":
    main()
