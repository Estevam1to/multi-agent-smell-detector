#!/usr/bin/env python3
"""
Script para gerar comparação final completa entre todas as ferramentas.
"""

import pandas as pd
import json


def generate_final_comparison():
    """Gera a comparação final entre todas as ferramentas."""

    pylint_df = pd.read_csv("results/code_tests_pylint.csv")
    bandit_df = pd.read_csv("results/code_tests_bandit.csv")
    agent_static_df = pd.read_csv("results/code_tests_agent_static.csv")
    agent_security_df = pd.read_csv("results/code_tests_agent_security.csv")

    print("🔍 RELATÓRIO FINAL DE COMPARAÇÃO - MULTI-AGENT vs FERRAMENTAS TRADICIONAIS")
    print("=" * 80)

    print("\n📊 RESUMO GERAL:")
    print(f"{'Ferramenta':<20} {'Categoria':<15} {'Total Issues':<12} {'Eficiência'}")
    print("-" * 65)
    print(f"{'Pylint':<20} {'Code Smells':<15} {len(pylint_df):<12} {'Baseline'}")
    print(
        f"{'Agente Estático':<20} {'Code Smells':<15} {len(agent_static_df):<12} {'+' + str(len(agent_static_df) - len(pylint_df))}"
    )
    print(f"{'Bandit':<20} {'Segurança':<15} {len(bandit_df):<12} {'Baseline'}")
    print(
        f"{'Agente Segurança':<20} {'Segurança':<15} {len(agent_security_df):<12} {str(len(agent_security_df) - len(bandit_df))}"
    )

    print("\n🐛 ANÁLISE ESTÁTICA - CODE SMELLS:")
    print("-" * 50)

    pylint_by_type = pylint_df["type"].value_counts()
    agent_static_by_type = agent_static_df["type"].value_counts()

    all_static_types = set(pylint_by_type.index) | set(agent_static_by_type.index)

    print(f"{'Tipo':<25} {'Pylint':<8} {'Agente':<8} {'Diferença'}")
    print("-" * 50)

    for tipo in all_static_types:
        pylint_count = pylint_by_type.get(tipo, 0)
        agent_count = agent_static_by_type.get(tipo, 0)
        diff = agent_count - pylint_count
        diff_str = f"{diff:+d}" if diff != 0 else "0"
        print(f"{tipo:<25} {pylint_count:<8} {agent_count:<8} {diff_str}")

    print("\n🔒 ANÁLISE DE SEGURANÇA:")
    print("-" * 40)

    bandit_by_severity = bandit_df["issue_severity"].value_counts()

    print("Bandit por Severidade:")
    for severity, count in bandit_by_severity.items():
        print(f"  {severity}: {count}")

    print(f"\nTotal Bandit: {len(bandit_df)}")
    print(f"Total Agente Segurança: {len(agent_security_df)}")
    print(f"Diferença: {len(agent_security_df) - len(bandit_df)}")

    print("\n📁 ANÁLISE POR ARQUIVO (Top 5):")
    print("-" * 40)

    # Code smells por arquivo
    pylint_by_file = pylint_df["file"].value_counts().head(5)
    agent_static_by_file = agent_static_df["file"].value_counts().head(5)

    print("Code Smells por arquivo:")
    all_files = set(pylint_by_file.index) | set(agent_static_by_file.index)

    for file_path in list(all_files)[:5]:
        filename = file_path.split("/")[-1]
        pylint_count = pylint_by_file.get(file_path, 0)
        agent_count = agent_static_by_file.get(file_path, 0)
        print(f"  {filename:<15}: Pylint={pylint_count}, Agente={agent_count}")

    bandit_by_file = bandit_df["file"].value_counts().head(5)
    agent_security_by_file = agent_security_df["file"].value_counts().head(5)

    print("\nVulnerabilidades por arquivo:")
    all_security_files = set(bandit_by_file.index) | set(agent_security_by_file.index)

    for file_path in list(all_security_files)[:5]:
        filename = file_path.split("/")[-1]
        bandit_count = bandit_by_file.get(file_path, 0)
        agent_count = agent_security_by_file.get(file_path, 0)
        print(f"  {filename:<15}: Bandit={bandit_count}, Agente={agent_count}")

    print("\n💡 INSIGHTS E CONCLUSÕES:")
    print("-" * 40)

    static_diff = len(agent_static_df) - len(pylint_df)
    security_diff = len(agent_security_df) - len(bandit_df)

    print("1. ANÁLISE ESTÁTICA:")
    if static_diff > 0:
        print(f"   ✅ Agente detectou +{static_diff} issues a mais que Pylint")
        print("   📈 Maior sensibilidade na detecção de code smells")
    else:
        print(f"   ⚠️  Agente detectou {abs(static_diff)} issues a menos que Pylint")

    print("\n2. ANÁLISE DE SEGURANÇA:")
    if security_diff > 0:
        print(f"   ⚠️  Agente detectou {security_diff} issues a mais que Bandit")
    else:
        print(f"   ✅ Agente foi mais conservador: {abs(security_diff)} issues a menos")

    print("\n3. QUALIDADE DAS DETECÇÕES:")
    print("   🔍 Agente estático encontrou tipos únicos (SQL Injection)")
    print("   🤖 Agentes podem ter maior contexto semântico")
    print("   📊 Ferramentas tradicionais são mais específicas")

    print("\n4. RECOMENDAÇÕES:")
    print("   🔄 Uso complementar: Agentes + Ferramentas tradicionais")
    print("   🎯 Agentes para análise semântica, ferramentas para sintática")
    print("   📝 Ajustar prompts dos agentes baseado nos gaps identificados")

    # Salva dados estruturados
    comparison_data = {
        "summary": {
            "pylint_total": len(pylint_df),
            "bandit_total": len(bandit_df),
            "agent_static_total": len(agent_static_df),
            "agent_security_total": len(agent_security_df),
            "static_difference": static_diff,
            "security_difference": security_diff,
        },
        "static_analysis": {
            "pylint_by_type": pylint_by_type.to_dict(),
            "agent_by_type": agent_static_by_type.to_dict(),
        },
        "security_analysis": {
            "bandit_by_severity": bandit_by_severity.to_dict(),
            "bandit_total": len(bandit_df),
            "agent_total": len(agent_security_df),
        },
    }

    with open("results/final_comparison_report.json", "w", encoding="utf-8") as f:
        json.dump(comparison_data, f, indent=2, ensure_ascii=False)

    print("\n💾 Relatório detalhado salvo em: results/final_comparison_report.json")
    print("📊 Gráficos disponíveis em: results/charts/")


if __name__ == "__main__":
    generate_final_comparison()
