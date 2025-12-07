#!/usr/bin/env python3
"""Script para rodar análise apenas com prompts completos."""

import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from core.supervisor import analyze_code

base_dir = Path(__file__).parent.parent
results_dir = base_dir / "results" / "json"
results_dir.mkdir(parents=True, exist_ok=True)

# Preços DeepSeek V3.2 Exp
INPUT_TOKEN_PRICE = 0.21 / 1_000_000
OUTPUT_TOKEN_PRICE = 0.32 / 1_000_000


def calculate_cost(prompt_tokens, completion_tokens):
    return prompt_tokens * INPUT_TOKEN_PRICE + completion_tokens * OUTPUT_TOKEN_PRICE


async def main():
    """Executa análise apenas com prompts completos."""
    dataset_dir = base_dir / "dataset"
    py_files = [f for f in dataset_dir.rglob("*.py") if "ground_truth" not in str(f)]

    print("=" * 80)
    print("ANÁLISE COM PROMPTS COMPLETOS")
    print("=" * 80)
    print(f"\nEncontrados {len(py_files)} arquivos Python")
    print(f"Resultados serão salvos em: {results_dir}")
    print("\nIniciando em 3 segundos...")
    time.sleep(3)

    all_smells = []
    total_token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    file_metrics = []

    for i, file_path in enumerate(py_files, 1):
        print(f"\n[{i}/{len(py_files)}] Analisando: {file_path.name}")

        try:
            code = file_path.read_text(encoding="utf-8")
            start_time = time.time()

            result = await analyze_code(
                    code, str(file_path), "Dataset", parallel=True, prompt_type="complete"
            )

            execution_time = time.time() - start_time

            detections = result.get("code_smells", [])
            token_usage = result.get("token_usage", {})

            all_smells.extend(detections)

            total_token_usage["prompt_tokens"] += token_usage.get("prompt_tokens", 0)
            total_token_usage["completion_tokens"] += token_usage.get(
                "completion_tokens", 0
            )
            total_token_usage["total_tokens"] += token_usage.get("total_tokens", 0)

            print(
                f"   ✓ {len(detections)} smells | {execution_time:.1f}s | {token_usage.get('total_tokens', 0):,} tokens"
            )

            file_metrics.append(
                {
                    "file_path": str(file_path),
                    "file_name": file_path.name,
                    "smells_detected": len(detections),
                    "execution_time_seconds": round(execution_time, 2),
                    "token_usage": token_usage,
                }
            )

        except Exception as e:
            print(f"   ✗ Erro: {e}")

    # Salvar resultados
    total_cost = calculate_cost(
        total_token_usage["prompt_tokens"], total_token_usage["completion_tokens"]
    )

    output_file = results_dir / "results_with_complete_prompts.json"
    output_file.write_text(
        json.dumps(all_smells, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    summary = {
        "prompt_type": "complete",
        "analysis_timestamp": datetime.now().isoformat(),
        "total_files_analyzed": len(py_files),
        "total_smells_detected": len(all_smells),
        "token_usage": total_token_usage,
        "total_cost_usd": round(total_cost, 4),
    }

    stats_file = results_dir / "token_usage_complete_prompts.json"
    stats_file.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    metrics_file = results_dir / "file_metrics_complete_prompt.json"
    metrics_file.write_text(
        json.dumps(file_metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print("\n" + "=" * 80)
    print("ANÁLISE CONCLUÍDA!")
    print("=" * 80)
    print(f"\nTotal de smells: {len(all_smells)}")
    print(f"Tokens totais: {total_token_usage['total_tokens']:,}")
    print(f"Custo total: ${total_cost:.4f}")
    print(f"\nArquivos salvos em: {results_dir}")


if __name__ == "__main__":
    asyncio.run(main())
