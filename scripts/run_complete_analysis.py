#!/usr/bin/env python3
"""Script completo para rodar análise com ambos os tipos de prompt em sequência.
Evita múltiplas execuções e economiza tokens."""

import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Importa a função de análise
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from core.supervisor import analyze_code

base_dir = Path(__file__).parent.parent
results_dir = base_dir / "results"
results_dir.mkdir(parents=True, exist_ok=True)


# Preços atualizados para DeepSeek V3.2 Exp
# Fonte: https://openrouter.ai/models/deepseek/deepseek-v3.2-exp
INPUT_TOKEN_PRICE = 0.21 / 1_000_000  # $0.21 por milhão de tokens de input
OUTPUT_TOKEN_PRICE = 0.32 / 1_000_000  # $0.32 por milhão de tokens de output


def calculate_cost(prompt_tokens, completion_tokens):
    """Calcula custo em USD baseado no uso de tokens."""
    input_cost = prompt_tokens * INPUT_TOKEN_PRICE
    output_cost = completion_tokens * OUTPUT_TOKEN_PRICE
    return input_cost + output_cost


def get_file_metrics(file_path):
    """Obtém métricas do arquivo (tamanho, linhas, etc)."""
    try:
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")
            lines = content.count("\n") + 1
            chars = len(content)
            return {
                "lines": lines,
                "chars": chars,
                "file_size_bytes": file_path.stat().st_size,
            }
    except Exception as e:
        print(f"Erro ao ler arquivo {file_path}: {e}")
    return {"lines": 0, "chars": 0, "file_size_bytes": 0}


async def analyze_with_metrics(prompt_type, py_files):
    """
    Analisa arquivos coletando métricas detalhadas.

    Args:
        prompt_type: "complete" ou "simple" - tipo de prompt a usar
        py_files: Lista de arquivos Python para analisar

    Returns:
        Tuple com (all_smells, summary, file_metrics)
    """
    print(f"\n{'=' * 80}")
    print(f"ANÁLISE COM PROMPTS {prompt_type.upper()}")
    print(f"{'=' * 80}")

    all_smells = []
    total_token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    file_metrics = []

    for i, file_path in enumerate(py_files, 1):
        print(
            f"[{i}/{len(py_files)}] {file_path.relative_to(base_dir / 'dataset')}...",
            end=" ",
        )

        file_info = get_file_metrics(file_path)

        start_time = time.time()

        try:
            code = file_path.read_text(encoding="utf-8")
            result = await analyze_code(
                code, str(file_path), "Dataset", parallel=True, prompt_type=prompt_type
            )

            execution_time = time.time() - start_time

            smells = result["code_smells"]
            all_smells.extend(smells)

            usage = result.get("token_usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)

            total_token_usage["prompt_tokens"] += prompt_tokens
            total_token_usage["completion_tokens"] += completion_tokens
            total_token_usage["total_tokens"] += total_tokens

            cost = calculate_cost(prompt_tokens, completion_tokens)

            file_metrics.append(
                {
                    "file_path": str(file_path),
                    "file_name": file_path.name,
                    "relative_path": str(file_path.relative_to(base_dir / "dataset")),
                    "lines": file_info["lines"],
                    "chars": file_info["chars"],
                    "file_size_bytes": file_info["file_size_bytes"],
                    "smells_detected": len(smells),
                    "execution_time_seconds": round(execution_time, 2),
                    "execution_time_minutes": round(execution_time / 60, 3),
                    "token_usage": {
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": total_tokens,
                    },
                    "cost_usd": round(cost, 6),
                    "cost_input_usd": round(prompt_tokens * INPUT_TOKEN_PRICE, 6),
                    "cost_output_usd": round(completion_tokens * OUTPUT_TOKEN_PRICE, 6),
                    "tokens_per_line": round(total_tokens / file_info["lines"], 2)
                    if file_info["lines"] > 0
                    else 0,
                    "tokens_per_smell": round(total_tokens / len(smells), 2)
                    if len(smells) > 0
                    else 0,
                    "cost_per_smell": round(cost / len(smells), 6)
                    if len(smells) > 0
                    else 0,
                }
            )

            print(
                f"✓ ({len(smells)} smells, {total_tokens:,} tokens, {execution_time:.1f}s, ${cost:.4f})"
            )

        except Exception as e:
            execution_time = time.time() - start_time
            print(f"✗ {type(e).__name__}: {e}")

            file_metrics.append(
                {
                    "file_path": str(file_path),
                    "file_name": file_path.name,
                    "relative_path": str(file_path.relative_to(base_dir / "dataset")),
                    "lines": file_info["lines"],
                    "chars": file_info["chars"],
                    "file_size_bytes": file_info["file_size_bytes"],
                    "smells_detected": 0,
                    "execution_time_seconds": round(execution_time, 2),
                    "execution_time_minutes": round(execution_time / 60, 3),
                    "error": str(e),
                    "token_usage": {
                        "prompt_tokens": 0,
                        "completion_tokens": 0,
                        "total_tokens": 0,
                    },
                    "cost_usd": 0,
                }
            )

    total_cost = calculate_cost(
        total_token_usage["prompt_tokens"], total_token_usage["completion_tokens"]
    )

    total_execution_time = sum(
        fm.get("execution_time_seconds", 0) for fm in file_metrics
    )
    avg_execution_time = total_execution_time / len(file_metrics) if file_metrics else 0

    summary = {
        "prompt_type": prompt_type,
        "analysis_timestamp": datetime.now().isoformat(),
        "total_files_analyzed": len(py_files),
        "total_smells_detected": len(all_smells),
        "total_execution_time_seconds": round(total_execution_time, 2),
        "total_execution_time_minutes": round(total_execution_time / 60, 2),
        "average_execution_time_seconds": round(avg_execution_time, 2),
        "average_execution_time_minutes": round(avg_execution_time / 60, 3),
        "token_usage": total_token_usage,
        "average_tokens_per_file": round(
            total_token_usage["total_tokens"] / len(py_files) if py_files else 0, 2
        ),
        "total_cost_usd": round(total_cost, 2),
        "average_cost_per_file": round(
            total_cost / len(py_files) if py_files else 0, 6
        ),
        "cost_input_usd": round(
            total_token_usage["prompt_tokens"] * INPUT_TOKEN_PRICE, 2
        ),
        "cost_output_usd": round(
            total_token_usage["completion_tokens"] * OUTPUT_TOKEN_PRICE, 2
        ),
        "average_tokens_per_smell": round(
            total_token_usage["total_tokens"] / len(all_smells) if all_smells else 0, 2
        ),
        "average_cost_per_smell": round(
            total_cost / len(all_smells) if all_smells else 0, 6
        ),
    }

    return all_smells, summary, file_metrics


async def main():
    """Executa análise completa com ambos os tipos de prompt."""
    dataset_dir = base_dir / "dataset"

    py_files = [f for f in dataset_dir.rglob("*.py") if "ground_truth" not in str(f)]

    print("=" * 80)
    print("ANÁLISE COMPLETA RQ5 - Prompts Completos e Simples")
    print("=" * 80)
    print(f"\nEncontrados {len(py_files)} arquivos Python")
    print(f"Resultados serão salvos em: {results_dir}")
    print("\nEste script executará:")
    print("  1. Análise com PROMPTS COMPLETOS (elaborados)")
    print("  2. Análise com PROMPTS SIMPLES")
    print("\nIniciando em 3 segundos...")
    time.sleep(3)

    # ============================================================
    # FASE 1: PROMPTS COMPLETOS
    # ============================================================
    print("\n" + "=" * 80)
    print("FASE 1: PROMPTS COMPLETOS")
    print("=" * 80)

    (
        complete_smells,
        complete_summary,
        complete_file_metrics,
    ) = await analyze_with_metrics("complete", py_files)

    output_file_complete = results_dir / "results_with_complete_prompts.json"
    output_file_complete.write_text(
        json.dumps(complete_smells, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    stats_file_complete = results_dir / "token_usage_complete_prompts.json"
    stats_file_complete.write_text(
        json.dumps(complete_summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    metrics_file_complete = results_dir / "file_metrics_complete_prompt.json"
    metrics_file_complete.write_text(
        json.dumps(complete_file_metrics, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"\n{'=' * 80}")
    print("FASE 1 CONCLUÍDA - Prompts Completos")
    print(f"{'=' * 80}")
    print(f"   • Total de smells: {len(complete_smells)}")
    print(
        f"   • Tempo total: {complete_summary['total_execution_time_minutes']:.1f} minutos"
    )
    print(f"   • Tokens totais: {complete_summary['token_usage']['total_tokens']:,}")
    print(f"   • Custo total: ${complete_summary['total_cost_usd']:.2f}")
    print("\n   Arquivos salvos:")
    print(f"   • {output_file_complete.name}")
    print(f"   • {stats_file_complete.name}")
    print(f"   • {metrics_file_complete.name}")

    # ============================================================
    # FASE 2: PROMPTS SIMPLES
    # ============================================================
    print("\n" + "=" * 80)
    print("FASE 2: PROMPTS SIMPLES")
    print("=" * 80)
    print("Aguardando 5 segundos antes de iniciar...")
    time.sleep(5)

    simple_smells, simple_summary, simple_file_metrics = await analyze_with_metrics(
        "simple", py_files
    )

    # Salvar resultados dos prompts simples
    output_file_simple = results_dir / "results_simple_prompt.json"
    output_file_simple.write_text(
        json.dumps(simple_smells, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    stats_file_simple = results_dir / "token_usage_simple_prompt.json"
    stats_file_simple.write_text(
        json.dumps(simple_summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    metrics_file_simple = results_dir / "file_metrics_simple_prompt.json"
    metrics_file_simple.write_text(
        json.dumps(simple_file_metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"\n{'=' * 80}")
    print("FASE 2 CONCLUÍDA - Prompts Simples")
    print(f"{'=' * 80}")
    print(f"   • Total de smells: {len(simple_smells)}")
    print(
        f"   • Tempo total: {simple_summary['total_execution_time_minutes']:.1f} minutos"
    )
    print(f"   • Tokens totais: {simple_summary['token_usage']['total_tokens']:,}")
    print(f"   • Custo total: ${simple_summary['total_cost_usd']:.2f}")
    print("\n   Arquivos salvos:")
    print(f"   • {output_file_simple.name}")
    print(f"   • {stats_file_simple.name}")
    print(f"   • {metrics_file_simple.name}")

    # ============================================================
    # RESUMO FINAL
    # ============================================================
    total_cost = complete_summary["total_cost_usd"] + simple_summary["total_cost_usd"]
    total_time = (
        complete_summary["total_execution_time_minutes"]
        + simple_summary["total_execution_time_minutes"]
    )
    total_tokens = (
        complete_summary["token_usage"]["total_tokens"]
        + simple_summary["token_usage"]["total_tokens"]
    )

    print(f"\n{'=' * 80}")
    print("ANÁLISE COMPLETA CONCLUÍDA!")
    print(f"{'=' * 80}")
    print("\nRESUMO GERAL:")
    print(f"   • Arquivos analisados: {len(py_files)}")
    print(f"   • Tempo total: {total_time:.1f} minutos")
    print(f"   • Tokens totais: {total_tokens:,}")
    print(f"   • Custo total: ${total_cost:.2f}")
    print("\nCOMPARAÇÃO:")
    print("   • Prompts Completos:")
    print(f"     - Smells: {len(complete_smells)}")
    print(f"     - Tokens: {complete_summary['token_usage']['total_tokens']:,}")
    print(f"     - Custo: ${complete_summary['total_cost_usd']:.2f}")
    print("   • Prompts Simples:")
    print(f"     - Smells: {len(simple_smells)}")
    print(f"     - Tokens: {simple_summary['token_usage']['total_tokens']:,}")
    print(f"     - Custo: ${simple_summary['total_cost_usd']:.2f}")
    print("\nARQUIVOS GERADOS:")
    print("\n   Prompts Completos:")
    print(f"     • {output_file_complete.name}")
    print(f"     • {stats_file_complete.name}")
    print(f"     • {metrics_file_complete.name}")
    print("   Prompts Simples:")
    print(f"     • {output_file_simple.name}")
    print(f"     • {stats_file_simple.name}")
    print(f"     • {metrics_file_simple.name}")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
