#!/usr/bin/env python3
"""
Script para testar os agentes de análise estática e segurança,
gerando CSV com os resultados para comparação.
"""

import json
import csv
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any

sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from src.agents.static_analizer_agent import static_agent
    from src.agents.security_agent import security_agent
except ImportError as e:
    print(f"Erro ao importar agentes: {e}")
    print(
        "Certifique-se de que as dependências estão instaladas e a API key está configurada."
    )
    sys.exit(1)


def read_file_content(file_path: str) -> str:
    """
    Lê o conteúdo de um arquivo Python.

    Args:
        file_path: Caminho para o arquivo

    Returns:
        Conteúdo do arquivo como string
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Erro ao ler arquivo {file_path}: {e}")
        return ""


def test_static_agent(code: str, file_path: str) -> List[Dict[str, Any]]:
    """
    Testa o agente de análise estática.

    Args:
        code: Código Python para analisar
        file_path: Caminho do arquivo (para contexto)

    Returns:
        Lista de code smells encontrados
    """
    try:
        print(f"Analisando code smells em: {file_path}")

        result = static_agent.invoke(
            {
                "messages": [
                    ("user", f"Analyze this Python code for code smells:\n\n{code}")
                ]
            }
        )

        # Extrai a resposta do agente
        if result and "messages" in result:
            last_message = result["messages"][-1]
            response_content = (
                last_message.content
                if hasattr(last_message, "content")
                else str(last_message)
            )

            # Tenta extrair JSON da resposta
            try:
                # Procura por JSON na resposta
                json_start = response_content.find("{")
                json_end = response_content.rfind("}") + 1

                if json_start >= 0 and json_end > json_start:
                    json_str = response_content[json_start:json_end]
                    result_data = json.loads(json_str)

                    code_smells = result_data.get("code_smells", [])

                    # Adiciona informação do arquivo
                    for smell in code_smells:
                        smell["file"] = file_path
                        smell["agent"] = "static_analyzer"

                    return code_smells

            except json.JSONDecodeError:
                print(
                    f"Erro ao decodificar JSON da resposta do agente estático para {file_path}"
                )

        return []

    except Exception as e:
        print(f"Erro ao testar agente estático em {file_path}: {e}")
        return []


def test_security_agent(code: str, file_path: str) -> List[Dict[str, Any]]:
    """
    Testa o agente de segurança.

    Args:
        code: Código Python para analisar
        file_path: Caminho do arquivo (para contexto)

    Returns:
        Lista de vulnerabilidades encontradas
    """
    try:
        print(f"Analisando vulnerabilidades em: {file_path}")

        result = security_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Analyze this Python code for security vulnerabilities:\n\n{code}",
                    )
                ]
            }
        )

        # Extrai a resposta do agente
        if result and "messages" in result:
            last_message = result["messages"][-1]
            response_content = (
                last_message.content
                if hasattr(last_message, "content")
                else str(last_message)
            )

            # Tenta extrair JSON da resposta
            try:
                # Procura por JSON na resposta
                json_start = response_content.find("{")
                json_end = response_content.rfind("}") + 1

                if json_start >= 0 and json_end > json_start:
                    json_str = response_content[json_start:json_end]
                    result_data = json.loads(json_str)

                    vulnerabilities = result_data.get("vulnerabilities", [])

                    # Adiciona informação do arquivo
                    for vuln in vulnerabilities:
                        vuln["file"] = file_path
                        vuln["agent"] = "security_analyzer"

                    return vulnerabilities

            except json.JSONDecodeError:
                print(
                    f"Erro ao decodificar JSON da resposta do agente de segurança para {file_path}"
                )

        return []

    except Exception as e:
        print(f"Erro ao testar agente de segurança em {file_path}: {e}")
        return []


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


def save_static_results_to_csv(results: List[Dict[str, Any]], output_file: str):
    """
    Salva os resultados de code smells em CSV.

    Args:
        results: Lista de code smells
        output_file: Arquivo CSV de saída
    """
    if not results:
        print("Nenhum code smell encontrado pelo agente.")
        return

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "file",
        "agent",
        "type",
        "description",
        "risk",
        "suggestion",
        "code",
        "line",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            row = {field: result.get(field, "") for field in fieldnames}
            writer.writerow(row)

    print(f"Resultados de code smells salvos em: {output_file}")
    print(f"Total de code smells encontrados: {len(results)}")


def save_security_results_to_csv(results: List[Dict[str, Any]], output_file: str):
    """
    Salva os resultados de vulnerabilidades em CSV.

    Args:
        results: Lista de vulnerabilidades
        output_file: Arquivo CSV de saída
    """
    if not results:
        print("Nenhuma vulnerabilidade encontrada pelo agente.")
        return

    # Cria o diretório se não existir
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "file",
        "agent",
        "type",
        "description",
        "risk",
        "suggestion",
        "code",
        "line",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            # Garante que todos os campos existem
            row = {field: result.get(field, "") for field in fieldnames}
            writer.writerow(row)

    print(f"Resultados de vulnerabilidades salvos em: {output_file}")
    print(f"Total de vulnerabilidades encontradas: {len(results)}")


def save_combined_results_to_json(
    static_results: List[Dict[str, Any]],
    security_results: List[Dict[str, Any]],
    output_file: str,
):
    """
    Salva os resultados combinados em JSON.

    Args:
        static_results: Resultados do agente estático
        security_results: Resultados do agente de segurança
        output_file: Arquivo JSON de saída
    """
    # Cria o diretório se não existir
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    combined = {
        "code_smells": static_results,
        "vulnerabilities": security_results,
        "summary": {
            "total_code_smells": len(static_results),
            "total_vulnerabilities": len(security_results),
            "total_issues": len(static_results) + len(security_results),
        },
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f"Resultados combinados salvos em: {output_file}")


def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(
        description="Testa os agentes de análise e gera CSV para comparação"
    )
    parser.add_argument("input_path", help="Arquivo Python ou diretório para analisar")
    parser.add_argument(
        "--static-csv",
        default="results/agent_code_smells.csv",
        help="Arquivo CSV para code smells (default: results/agent_code_smells.csv)",
    )
    parser.add_argument(
        "--security-csv",
        default="results/agent_vulnerabilities.csv",
        help="Arquivo CSV para vulnerabilidades (default: results/agent_vulnerabilities.csv)",
    )
    parser.add_argument(
        "--combined-json",
        default="results/agent_combined_results.json",
        help="Arquivo JSON combinado (default: results/agent_combined_results.json)",
    )
    parser.add_argument(
        "--agent",
        choices=["static", "security", "both"],
        default="both",
        help="Qual agente executar (default: both)",
    )

    args = parser.parse_args()

    # Verifica se o caminho existe
    if not Path(args.input_path).exists():
        print(f"Erro: Caminho não encontrado: {args.input_path}")
        sys.exit(1)

    # Encontra arquivos Python
    python_files = find_python_files(args.input_path)

    if not python_files:
        print("Nenhum arquivo Python encontrado.")
        sys.exit(1)

    print(f"Encontrados {len(python_files)} arquivo(s) Python para analisar")

    static_results = []
    security_results = []

    # Processa cada arquivo
    for file_path in python_files:
        code = read_file_content(file_path)
        if not code:
            continue

        # Testa agente estático
        if args.agent in ["static", "both"]:
            static_results.extend(test_static_agent(code, file_path))

        # Testa agente de segurança
        if args.agent in ["security", "both"]:
            security_results.extend(test_security_agent(code, file_path))

    # Salva os resultados
    if args.agent in ["static", "both"] and static_results:
        save_static_results_to_csv(static_results, args.static_csv)

    if args.agent in ["security", "both"] and security_results:
        save_security_results_to_csv(security_results, args.security_csv)

    if args.agent == "both":
        save_combined_results_to_json(
            static_results, security_results, args.combined_json
        )

    # Mostra resumo
    print("\n=== RESUMO ===")
    if args.agent in ["static", "both"]:
        print(f"Code smells encontrados: {len(static_results)}")
    if args.agent in ["security", "both"]:
        print(f"Vulnerabilidades encontradas: {len(security_results)}")


if __name__ == "__main__":
    main()
