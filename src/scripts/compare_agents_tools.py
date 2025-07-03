#!/usr/bin/env python3
"""
Script para comparar resultados dos agentes com Pylint/Bandit.
"""

import csv
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict


def load_agent_csv(csv_file: str) -> List[Dict[str, Any]]:
    """
    Carrega resultados dos agentes de um arquivo CSV.

    Args:
        csv_file: Caminho para o arquivo CSV

    Returns:
        Lista de dicionários com os resultados
    """
    results = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
    return results


def load_tool_csv(csv_file: str) -> List[Dict[str, Any]]:
    """
    Carrega resultados do Pylint/Bandit de um arquivo CSV.

    Args:
        csv_file: Caminho para o arquivo CSV

    Returns:
        Lista de dicionários com os resultados
    """
    results = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
    return results


def compare_static_analysis(
    agent_results: List[Dict[str, Any]], pylint_results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Compara resultados de análise estática (agente vs Pylint).

    Args:
        agent_results: Resultados do agente estático
        pylint_results: Resultados do Pylint

    Returns:
        Dicionário com a comparação
    """
    comparison = {
        "summary": {
            "agent_total": len(agent_results),
            "pylint_total": len(pylint_results),
            "difference": len(agent_results) - len(pylint_results),
        },
        "by_file": {},
        "by_type": defaultdict(lambda: {"agent": 0, "pylint": 0}),
        "agent_only": [],
        "pylint_only": [],
        "common_issues": [],
    }

    # Agrupa por arquivo e tipo
    agent_by_file = defaultdict(lambda: defaultdict(int))
    pylint_by_file = defaultdict(lambda: defaultdict(int))

    for result in agent_results:
        file_path = result.get("file", "")
        issue_type = result.get("type", "").lower().replace(" ", "_")
        agent_by_file[file_path][issue_type] += 1
        comparison["by_type"][issue_type]["agent"] += 1

    for result in pylint_results:
        file_path = result.get("file", "")
        issue_type = result.get("type", "").lower().replace(" ", "_")
        pylint_by_file[file_path][issue_type] += 1
        comparison["by_type"][issue_type]["pylint"] += 1

    # Encontra questões comuns e diferentes
    all_files = set(agent_by_file.keys()) | set(pylint_by_file.keys())

    for file_path in all_files:
        agent_file = agent_by_file.get(file_path, {})
        pylint_file = pylint_by_file.get(file_path, {})

        comparison["by_file"][file_path] = {
            "agent": dict(agent_file),
            "pylint": dict(pylint_file),
            "differences": {},
        }

        all_types = set(agent_file.keys()) | set(pylint_file.keys())
        for issue_type in all_types:
            agent_count = agent_file.get(issue_type, 0)
            pylint_count = pylint_file.get(issue_type, 0)

            if agent_count != pylint_count:
                comparison["by_file"][file_path]["differences"][issue_type] = {
                    "agent": agent_count,
                    "pylint": pylint_count,
                    "diff": agent_count - pylint_count,
                }

    return comparison


def compare_security_analysis(
    agent_results: List[Dict[str, Any]], bandit_results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Compara resultados de análise de segurança (agente vs Bandit).

    Args:
        agent_results: Resultados do agente de segurança
        bandit_results: Resultados do Bandit

    Returns:
        Dicionário com a comparação
    """
    comparison = {
        "summary": {
            "agent_total": len(agent_results),
            "bandit_total": len(bandit_results),
            "difference": len(agent_results) - len(bandit_results),
        },
        "by_file": {},
        "by_severity": defaultdict(lambda: {"agent": 0, "bandit": 0}),
        "by_type": defaultdict(lambda: {"agent": 0, "bandit": 0}),
    }

    # Agrupa por arquivo
    agent_by_file = defaultdict(int)
    bandit_by_file = defaultdict(int)

    for result in agent_results:
        file_path = result.get("file", "")
        vuln_type = result.get("type", "").lower().replace(" ", "_")
        agent_by_file[file_path] += 1
        comparison["by_type"][vuln_type]["agent"] += 1

    for result in bandit_results:
        file_path = result.get("file", "")
        vuln_type = result.get("type", "").lower().replace(" ", "_")
        severity = result.get("severity", "").lower()
        bandit_by_file[file_path] += 1
        comparison["by_type"][vuln_type]["bandit"] += 1
        comparison["by_severity"][severity]["bandit"] += 1

    # Compara por arquivo
    all_files = set(agent_by_file.keys()) | set(bandit_by_file.keys())

    for file_path in all_files:
        agent_count = agent_by_file.get(file_path, 0)
        bandit_count = bandit_by_file.get(file_path, 0)

        comparison["by_file"][file_path] = {
            "agent": agent_count,
            "bandit": bandit_count,
            "difference": agent_count - bandit_count,
        }

    return comparison


def save_comparison_report(comparison: Dict[str, Any], output_file: str):
    """
    Salva o relatório de comparação em JSON.

    Args:
        comparison: Dados da comparação
        output_file: Arquivo de saída
    """
    # Cria o diretório se não existir
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2, ensure_ascii=False)

    print(f"Relatório de comparação salvo em: {output_file}")


def print_static_summary(comparison: Dict[str, Any]):
    """
    Imprime resumo da comparação de análise estática.

    Args:
        comparison: Dados da comparação
    """
    summary = comparison["summary"]

    print("\n=== COMPARAÇÃO: AGENTE ESTÁTICO vs PYLINT ===")
    print("Total de issues encontradas:")
    print(f"  Agente: {summary['agent_total']}")
    print(f"  Pylint: {summary['pylint_total']}")
    print(f"  Diferença: {summary['difference']:+d}")

    print("\n=== POR TIPO DE ISSUE ===")
    for issue_type, counts in comparison["by_type"].items():
        agent_count = counts["agent"]
        pylint_count = counts["pylint"]
        diff = agent_count - pylint_count

        print(f"{issue_type.replace('_', ' ').title()}:")
        print(f"  Agente: {agent_count}")
        print(f"  Pylint: {pylint_count}")
        print(f"  Diferença: {diff:+d}")


def print_security_summary(comparison: Dict[str, Any]):
    """
    Imprime resumo da comparação de análise de segurança.

    Args:
        comparison: Dados da comparação
    """
    summary = comparison["summary"]

    print("\n=== COMPARAÇÃO: AGENTE SEGURANÇA vs BANDIT ===")
    print("Total de vulnerabilidades encontradas:")
    print(f"  Agente: {summary['agent_total']}")
    print(f"  Bandit: {summary['bandit_total']}")
    print(f"  Diferença: {summary['difference']:+d}")

    print("\n=== POR TIPO DE VULNERABILIDADE ===")
    for vuln_type, counts in comparison["by_type"].items():
        agent_count = counts["agent"]
        bandit_count = counts["bandit"]
        diff = agent_count - bandit_count

        print(f"{vuln_type.replace('_', ' ').title()}:")
        print(f"  Agente: {agent_count}")
        print(f"  Bandit: {bandit_count}")
        print(f"  Diferença: {diff:+d}")


def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(
        description="Compara resultados dos agentes com Pylint/Bandit"
    )
    parser.add_argument("--static-agent", help="CSV com resultados do agente estático")
    parser.add_argument("--static-pylint", help="CSV com resultados do Pylint")
    parser.add_argument(
        "--security-agent", help="CSV com resultados do agente de segurança"
    )
    parser.add_argument("--security-bandit", help="CSV com resultados do Bandit")
    parser.add_argument(
        "-o",
        "--output",
        default="results/agent_tool_comparison.json",
        help="Arquivo JSON de saída (default: results/agent_tool_comparison.json)",
    )

    args = parser.parse_args()

    if not any([args.static_agent, args.security_agent]):
        print(
            "Erro: Especifique pelo menos um par de comparação (--static-agent ou --security-agent)"
        )
        return 1

    full_comparison = {}

    # Comparação de análise estática
    if args.static_agent and args.static_pylint:
        if not Path(args.static_agent).exists():
            print(f"Erro: Arquivo não encontrado: {args.static_agent}")
            return 1
        if not Path(args.static_pylint).exists():
            print(f"Erro: Arquivo não encontrado: {args.static_pylint}")
            return 1

        print("Carregando resultados de análise estática...")
        agent_results = load_agent_csv(args.static_agent)
        pylint_results = load_tool_csv(args.static_pylint)

        static_comparison = compare_static_analysis(agent_results, pylint_results)
        full_comparison["static_analysis"] = static_comparison

        print_static_summary(static_comparison)

    # Comparação de análise de segurança
    if args.security_agent and args.security_bandit:
        if not Path(args.security_agent).exists():
            print(f"Erro: Arquivo não encontrado: {args.security_agent}")
            return 1
        if not Path(args.security_bandit).exists():
            print(f"Erro: Arquivo não encontrado: {args.security_bandit}")
            return 1

        print("Carregando resultados de análise de segurança...")
        agent_results = load_agent_csv(args.security_agent)
        bandit_results = load_tool_csv(args.security_bandit)

        security_comparison = compare_security_analysis(agent_results, bandit_results)
        full_comparison["security_analysis"] = security_comparison

        print_security_summary(security_comparison)

    # Salva o relatório
    if full_comparison:
        save_comparison_report(full_comparison, args.output)

    return 0


if __name__ == "__main__":
    exit(main())
