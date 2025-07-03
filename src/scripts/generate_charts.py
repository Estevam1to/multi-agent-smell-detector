#!/usr/bin/env python3
"""
Script para gerar gráficos comparativos dos resultados de análise.
Cria visualizações para comparar agentes vs ferramentas tradicionais.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from pathlib import Path
import json

plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


def load_csv_data(file_path: str) -> pd.DataFrame:
    """Carrega dados de um arquivo CSV."""
    return pd.read_csv(file_path)


def analyze_static_comparison(pylint_df: pd.DataFrame, agent_df: pd.DataFrame):
    """Analisa e compara resultados de análise estática."""

    # Contagem por tipo - Pylint
    pylint_counts = pylint_df["type"].value_counts()

    # Contagem por tipo - Agente
    agent_counts = agent_df["type"].value_counts()

    # Combina os dados para comparação
    comparison_data = []
    all_types = set(pylint_counts.index) | set(agent_counts.index)

    for issue_type in all_types:
        pylint_count = pylint_counts.get(issue_type, 0)
        agent_count = agent_counts.get(issue_type, 0)

        comparison_data.append(
            {"Type": issue_type, "Pylint": pylint_count, "Agent": agent_count}
        )

    return pd.DataFrame(comparison_data)


def analyze_security_comparison(bandit_df: pd.DataFrame, agent_df: pd.DataFrame):
    """Analisa e compara resultados de análise de segurança."""

    bandit_counts = bandit_df["test_name"].value_counts()

    agent_counts = agent_df["type"].value_counts()

    severity_data = bandit_df["issue_severity"].value_counts()

    return {
        "bandit_total": len(bandit_df),
        "agent_total": len(agent_df),
        "bandit_by_type": bandit_counts,
        "agent_by_type": agent_counts,
        "severity_distribution": severity_data,
    }


def create_static_comparison_charts(comparison_df: pd.DataFrame, output_dir: str):
    """Cria gráficos de comparação para análise estática."""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    x_pos = range(len(comparison_df))
    width = 0.35

    ax1.bar(
        [x - width / 2 for x in x_pos],
        comparison_df["Pylint"],
        width,
        label="Pylint",
        alpha=0.8,
        color="skyblue",
    )
    ax1.bar(
        [x + width / 2 for x in x_pos],
        comparison_df["Agent"],
        width,
        label="Static Agent",
        alpha=0.8,
        color="lightcoral",
    )

    ax1.set_xlabel("Tipo de Code Smell")
    ax1.set_ylabel("Quantidade")
    ax1.set_title("Comparação: Pylint vs Agente Estático")
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(comparison_df["Type"], rotation=45, ha="right")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Gráfico 2: Diferenças
    comparison_df["Difference"] = comparison_df["Agent"] - comparison_df["Pylint"]
    colors = ["red" if x < 0 else "green" for x in comparison_df["Difference"]]

    ax2.bar(comparison_df["Type"], comparison_df["Difference"], color=colors, alpha=0.7)
    ax2.set_xlabel("Tipo de Code Smell")
    ax2.set_ylabel("Diferença (Agente - Pylint)")
    ax2.set_title("Diferenças na Detecção")
    ax2.axhline(y=0, color="black", linestyle="-", alpha=0.3)
    ax2.tick_params(axis="x", rotation=45)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        f"{output_dir}/static_analysis_comparison.png", dpi=300, bbox_inches="tight"
    )
    plt.close()

    fig, ax = plt.subplots(1, 1, figsize=(8, 6))

    totals = {
        "Pylint": comparison_df["Pylint"].sum(),
        "Static Agent": comparison_df["Agent"].sum(),
    }

    bars = ax.bar(
        totals.keys(), totals.values(), color=["skyblue", "lightcoral"], alpha=0.8
    )
    ax.set_ylabel("Total de Issues")
    ax.set_title("Total de Code Smells Detectados")

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.5,
            f"{int(height)}",
            ha="center",
            va="bottom",
        )

    ax.grid(True, alpha=0.3)
    plt.savefig(
        f"{output_dir}/static_analysis_totals.png", dpi=300, bbox_inches="tight"
    )
    plt.close()


def create_security_comparison_charts(security_data: dict, output_dir: str):
    """Cria gráficos de comparação para análise de segurança."""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    totals = {
        "Bandit": security_data["bandit_total"],
        "Security Agent": security_data["agent_total"],
    }

    bars = ax1.bar(
        totals.keys(), totals.values(), color=["orange", "purple"], alpha=0.8
    )
    ax1.set_ylabel("Total de Vulnerabilidades")
    ax1.set_title("Total de Vulnerabilidades Detectadas")

    for bar in bars:
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 1,
            f"{int(height)}",
            ha="center",
            va="bottom",
        )

    ax1.grid(True, alpha=0.3)

    severity_data = security_data["severity_distribution"]
    colors_severity = {"HIGH": "red", "MEDIUM": "orange", "LOW": "yellow"}
    colors = [colors_severity.get(sev, "gray") for sev in severity_data.index]

    ax2.pie(
        severity_data.values,
        labels=severity_data.index,
        autopct="%1.1f%%",
        colors=colors,
    )
    ax2.set_title("Distribuição por Severidade (Bandit)")

    plt.tight_layout()
    plt.savefig(
        f"{output_dir}/security_analysis_comparison.png", dpi=300, bbox_inches="tight"
    )
    plt.close()

    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    top_bandit = security_data["bandit_by_type"].head(10)

    ax.barh(range(len(top_bandit)), top_bandit.values, alpha=0.8, color="orange")
    ax.set_yticks(range(len(top_bandit)))
    ax.set_yticklabels(top_bandit.index)
    ax.set_xlabel("Quantidade")
    ax.set_title("Top 10 Tipos de Vulnerabilidades (Bandit)")
    ax.grid(True, alpha=0.3)

    for i, v in enumerate(top_bandit.values):
        ax.text(v + 0.1, i, str(v), va="center")

    plt.tight_layout()
    plt.savefig(
        f"{output_dir}/security_vulnerability_types.png", dpi=300, bbox_inches="tight"
    )
    plt.close()


def create_summary_dashboard(
    pylint_df: pd.DataFrame,
    bandit_df: pd.DataFrame,
    agent_static_df: pd.DataFrame,
    agent_security_df: pd.DataFrame,
    output_dir: str,
):
    """Cria um dashboard resumo com todos os dados."""

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

    # Gráfico 1: Totais gerais
    tools = ["Pylint", "Bandit", "Static Agent", "Security Agent"]
    totals = [
        len(pylint_df),
        len(bandit_df),
        len(agent_static_df),
        len(agent_security_df),
    ]
    colors = ["skyblue", "orange", "lightcoral", "purple"]

    bars = ax1.bar(tools, totals, color=colors, alpha=0.8)
    ax1.set_ylabel("Total de Issues/Vulnerabilidades")
    ax1.set_title("Comparação Geral: Total de Detecções")
    ax1.tick_params(axis="x", rotation=45)

    for bar in bars:
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 1,
            f"{int(height)}",
            ha="center",
            va="bottom",
        )

    # Gráfico 2: Distribuição por arquivo (Code Smells)
    files_static = pylint_df["file"].value_counts().head(5)
    ax2.pie(
        files_static.values,
        labels=[f.split("/")[-1] for f in files_static.index],
        autopct="%1.1f%%",
    )
    ax2.set_title("Top 5 Arquivos com Code Smells (Pylint)")

    # Gráfico 3: Distribuição por arquivo (Vulnerabilidades)
    files_security = bandit_df["file"].value_counts().head(5)
    ax3.pie(
        files_security.values,
        labels=[f.split("/")[-1] for f in files_security.index],
        autopct="%1.1f%%",
    )
    ax3.set_title("Top 5 Arquivos com Vulnerabilidades (Bandit)")

    # Gráfico 4: Comparação de eficácia
    categories = ["Code Smells", "Security Issues"]
    traditional = [len(pylint_df), len(bandit_df)]
    agents = [len(agent_static_df), len(agent_security_df)]

    x_pos = range(len(categories))
    width = 0.35

    ax4.bar(
        [x - width / 2 for x in x_pos],
        traditional,
        width,
        label="Traditional Tools",
        color="lightblue",
        alpha=0.8,
    )
    ax4.bar(
        [x + width / 2 for x in x_pos],
        agents,
        width,
        label="AI Agents",
        color="lightgreen",
        alpha=0.8,
    )

    ax4.set_xlabel("Categoria")
    ax4.set_ylabel("Quantidade")
    ax4.set_title("Ferramentas Tradicionais vs Agentes IA")
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(categories)
    ax4.legend()

    # Adiciona valores nas barras
    for i, (trad, agent) in enumerate(zip(traditional, agents)):
        ax4.text(i - width / 2, trad + 0.5, str(trad), ha="center", va="bottom")
        ax4.text(i + width / 2, agent + 0.5, str(agent), ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(f"{output_dir}/summary_dashboard.png", dpi=300, bbox_inches="tight")
    plt.close()


def generate_comparison_report(
    pylint_df: pd.DataFrame,
    bandit_df: pd.DataFrame,
    agent_static_df: pd.DataFrame,
    agent_security_df: pd.DataFrame,
    output_dir: str,
):
    """Gera relatório textual da comparação."""

    report = {
        "summary": {
            "pylint_total": len(pylint_df),
            "bandit_total": len(bandit_df),
            "agent_static_total": len(agent_static_df),
            "agent_security_total": len(agent_security_df),
        },
        "static_analysis": {
            "pylint_by_type": pylint_df["type"].value_counts().to_dict(),
            "agent_by_type": agent_static_df["type"].value_counts().to_dict(),
        },
        "security_analysis": {
            "bandit_by_severity": bandit_df["issue_severity"].value_counts().to_dict(),
            "bandit_by_type": bandit_df["test_name"].value_counts().to_dict(),
            "agent_by_type": agent_security_df["type"].value_counts().to_dict(),
        },
    }

    with open(f"{output_dir}/comparison_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Relatório em texto
    with open(f"{output_dir}/comparison_report.txt", "w", encoding="utf-8") as f:
        f.write("RELATÓRIO DE COMPARAÇÃO - ANÁLISE DE CÓDIGO\n")
        f.write("=" * 50 + "\n\n")

        f.write("RESUMO GERAL:\n")
        f.write(f"Pylint (Code Smells): {len(pylint_df)} issues\n")
        f.write(f"Bandit (Vulnerabilidades): {len(bandit_df)} issues\n")
        f.write(f"Agente Estático: {len(agent_static_df)} issues\n")
        f.write(f"Agente Segurança: {len(agent_security_df)} issues\n\n")

        f.write("ANÁLISE ESTÁTICA:\n")
        f.write("Pylint por tipo:\n")
        for tipo, count in pylint_df["type"].value_counts().items():
            f.write(f"  {tipo}: {count}\n")

        f.write("\nAgente Estático por tipo:\n")
        for tipo, count in agent_static_df["type"].value_counts().items():
            f.write(f"  {tipo}: {count}\n")

        f.write("\nANÁLISE DE SEGURANÇA:\n")
        f.write("Bandit por severidade:\n")
        for sev, count in bandit_df["issue_severity"].value_counts().items():
            f.write(f"  {sev}: {count}\n")


def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(
        description="Gera gráficos comparativos dos resultados de análise"
    )
    parser.add_argument(
        "--pylint-csv", required=True, help="CSV com resultados do Pylint"
    )
    parser.add_argument(
        "--bandit-csv", required=True, help="CSV com resultados do Bandit"
    )
    parser.add_argument(
        "--agent-static-csv",
        required=True,
        help="CSV com resultados do agente estático",
    )
    parser.add_argument(
        "--agent-security-csv",
        required=True,
        help="CSV com resultados do agente de segurança",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="results/charts",
        help="Diretório para salvar os gráficos (default: results/charts)",
    )

    args = parser.parse_args()

    # Cria diretório de saída
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Carrega os dados
    print("Carregando dados...")
    pylint_df = load_csv_data(args.pylint_csv)
    bandit_df = load_csv_data(args.bandit_csv)
    agent_static_df = load_csv_data(args.agent_static_csv)
    agent_security_df = load_csv_data(args.agent_security_csv)

    print("Dados carregados:")
    print(f"  Pylint: {len(pylint_df)} issues")
    print(f"  Bandit: {len(bandit_df)} vulnerabilidades")
    print(f"  Agente Estático: {len(agent_static_df)} issues")
    print(f"  Agente Segurança: {len(agent_security_df)} vulnerabilidades")

    # Análise de comparação estática
    print("\nGerando gráficos de análise estática...")
    comparison_df = analyze_static_comparison(pylint_df, agent_static_df)
    create_static_comparison_charts(comparison_df, str(output_dir))

    # Análise de comparação de segurança
    print("Gerando gráficos de análise de segurança...")
    security_data = analyze_security_comparison(bandit_df, agent_security_df)
    create_security_comparison_charts(security_data, str(output_dir))

    # Dashboard resumo
    print("Gerando dashboard resumo...")
    create_summary_dashboard(
        pylint_df, bandit_df, agent_static_df, agent_security_df, str(output_dir)
    )

    # Relatório de comparação
    print("Gerando relatório de comparação...")
    generate_comparison_report(
        pylint_df, bandit_df, agent_static_df, agent_security_df, str(output_dir)
    )

    print(f"\nGráficos salvos em: {output_dir}")
    print("Gráficos gerados:")
    print("  - static_analysis_comparison.png")
    print("  - static_analysis_totals.png")
    print("  - security_analysis_comparison.png")
    print("  - security_vulnerability_types.png")
    print("  - summary_dashboard.png")
    print("  - comparison_report.json")
    print("  - comparison_report.txt")


if __name__ == "__main__":
    main()
