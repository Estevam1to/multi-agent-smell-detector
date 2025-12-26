#!/usr/bin/env python3
"""Script genérico para rodar análise com qualquer modelo LLM."""

import asyncio
import json
import sys
import time
import os
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Configurações de modelos disponíveis
MODELS = {
    "claude-sonnet": {
        "id": "anthropic/claude-sonnet-4",
        "company": "anthropic",
        "name": "claude-sonnet-4.5",
        "input_price": 3.00 / 1_000_000,  # $3/M
        "output_price": 15.00 / 1_000_000,  # $15/M
    },
    "gpt-4o-mini": {
        "id": "openai/gpt-4o-mini",
        "company": "openai",
        "name": "gpt-4o-mini",
        "input_price": 0.15 / 1_000_000,  # $0.15/M
        "output_price": 0.60 / 1_000_000,  # $0.60/M
    },
    "deepseek-v3": {
        "id": "deepseek/deepseek-v3.2",
        "company": "deepseek",
        "name": "deepseek-v3.2",
        "input_price": 0.224 / 1_000_000,  # $0.224/M
        "output_price": 0.32 / 1_000_000,  # $0.32/M
    },
}


def calculate_cost(prompt_tokens, completion_tokens, model_config):
    return (
        prompt_tokens * model_config["input_price"]
        + completion_tokens * model_config["output_price"]
    )


async def run_analysis(model_key: str, prompt_type: str = "complete"):
    """Executa análise com o modelo especificado."""
    
    if model_key not in MODELS:
        print(f"Modelo '{model_key}' não encontrado!")
        print(f"Modelos disponíveis: {', '.join(MODELS.keys())}")
        sys.exit(1)
    
    model_config = MODELS[model_key]
    
    # Configurar variável de ambiente ANTES de importar settings
    os.environ["OPENROUTER_API_MODEL"] = model_config["id"]
    
    # Importar após configurar a variável de ambiente
    from config.settings import settings
    # Sobrescrever o modelo no settings já carregado
    settings.__dict__["OPENROUTER_API_MODEL"] = model_config["id"]
    
    from core.supervisor import analyze_code
    
    base_dir = Path(__file__).parent.parent
    
    # Criar pasta de resultados: results/empresa/modelo/
    results_dir = base_dir / "results" / model_config["company"] / model_config["name"]
    results_dir.mkdir(parents=True, exist_ok=True)
    
    dataset_dir = base_dir / "dataset"
    py_files = [f for f in dataset_dir.rglob("*.py") if "ground_truth" not in str(f)]

    print("=" * 80)
    print(f"ANÁLISE COM {model_key.upper()}")
    print(f"Modelo: {model_config['id']}")
    print(f"Prompt: {prompt_type}")
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
                code, str(file_path), "Dataset", parallel=True, prompt_type=prompt_type
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
                f"   OK {len(detections)} smells | {execution_time:.1f}s | {token_usage.get('total_tokens', 0):,} tokens"
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
            print(f"   ERRO: {e}")

    # Salvar resultados
    total_cost = calculate_cost(
        total_token_usage["prompt_tokens"],
        total_token_usage["completion_tokens"],
        model_config,
    )

    # Nome do arquivo baseado no tipo de prompt
    suffix = "complete" if prompt_type == "complete" else "simple"
    
    output_file = results_dir / f"results_{suffix}_prompts.json"
    output_file.write_text(
        json.dumps(all_smells, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    summary = {
        "model": model_config["id"],
        "model_name": model_key,
        "prompt_type": prompt_type,
        "analysis_timestamp": datetime.now().isoformat(),
        "total_files_analyzed": len(py_files),
        "total_smells_detected": len(all_smells),
        "token_usage": total_token_usage,
        "total_cost_usd": round(total_cost, 4),
        "pricing": {
            "input_per_million": model_config["input_price"] * 1_000_000,
            "output_per_million": model_config["output_price"] * 1_000_000,
        },
    }

    stats_file = results_dir / f"token_usage_{suffix}_prompts.json"
    stats_file.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    metrics_file = results_dir / f"file_metrics_{suffix}_prompts.json"
    metrics_file.write_text(
        json.dumps(file_metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print("\n" + "=" * 80)
    print("ANÁLISE CONCLUÍDA!")
    print("=" * 80)
    print(f"\nModelo: {model_config['id']}")
    print(f"Total de smells: {len(all_smells)}")
    print(f"Tokens totais: {total_token_usage['total_tokens']:,}")
    print(f"Custo total: ${total_cost:.4f}")
    print(f"\nArquivos salvos em: {results_dir}")
    
    return summary


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python run_with_model.py <modelo> [prompt_type]")
        print(f"Modelos disponíveis: {', '.join(MODELS.keys())}")
        print("Tipos de prompt: complete (padrão), simple")
        sys.exit(1)
    
    model = sys.argv[1]
    prompt_type = sys.argv[2] if len(sys.argv) > 2 else "complete"
    
    asyncio.run(run_analysis(model, prompt_type))

