"""
Testes unitários para os agentes de detecção de code smells.

Usa LLM as a Judge para avaliar a qualidade das detecções.
"""

import asyncio
import json
import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from llm_judge import get_judge
from supervisor import analyze_code_with_supervisor
from test_cases.smell_examples import ALL_EXAMPLES


async def run_single_test(example: dict) -> dict:
    """
    Executa um teste único.

    Args:
        example: Dicionário com exemplo de code smell

    Returns:
        Resultado do teste
    """
    print(f"\n{'='*80}")
    print(f"Testando: {example['smell_type']}")
    print(f"{'='*80}")

    # Executa a análise
    result = await analyze_code_with_supervisor(example["code"])

    # Encontra a resposta do agente específico para este smell
    agent_name = example["smell_type"]
    agent_response = None

    for smell in result["code_smells"]:
        if agent_name in smell["smell_type"]:
            agent_response = smell["findings"]
            break

    # Se não encontrou resposta específica, usa os resultados gerais
    if agent_response is None:
        agent_response = f"Total de smells detectados: {result['total_smells_detected']}"
        if result["code_smells"]:
            agent_response += f"\nSmells encontrados: {[s['smell_type'] for s in result['code_smells']]}"

    print(f"\nResposta do sistema: {agent_response[:200]}...")

    # Prepara metadados
    metadata = {k: v for k, v in example.items() if k not in ["code", "smell_type", "expected_detection"]}

    return {
        "name": example["smell_type"],
        "code": example["code"],
        "smell_type": example["smell_type"],
        "agent_response": agent_response,
        "expected_detection": example["expected_detection"],
        "metadata": metadata,
        "raw_result": result,
    }


async def run_all_tests():
    """Executa todos os testes e gera relatório."""
    print("\n" + "="*80)
    print("INICIANDO TESTES COM LLM AS A JUDGE")
    print("="*80)

    # Executa todos os testes
    test_results = []
    for example in ALL_EXAMPLES:
        result = await run_single_test(example)
        test_results.append(result)

    print("\n" + "="*80)
    print("AVALIANDO RESULTADOS COM LLM JUDGE")
    print("="*80)

    # Avalia com LLM Judge
    judge = get_judge()
    evaluation = await judge.evaluate_test_suite(test_results)

    # Imprime resultados
    print("\n" + "="*80)
    print("RESULTADOS DA AVALIAÇÃO")
    print("="*80)

    print(f"\nTotal de testes: {evaluation['total_tests']}")

    print("\n### MÉTRICAS ###")
    print(f"Accuracy:  {evaluation['metrics']['accuracy']:.2%}")
    print(f"Precision: {evaluation['metrics']['precision']:.2%}")
    print(f"Recall:    {evaluation['metrics']['recall']:.2%}")
    print(f"F1-Score:  {evaluation['metrics']['f1_score']:.2%}")

    print("\n### MATRIZ DE CONFUSÃO ###")
    cm = evaluation['confusion_matrix']
    print(f"True Positives:  {cm['true_positives']}")
    print(f"True Negatives:  {cm['true_negatives']}")
    print(f"False Positives: {cm['false_positives']}")
    print(f"False Negatives: {cm['false_negatives']}")
    print(f"Errors:          {cm['errors']}")

    print("\n### DETALHES POR TESTE ###")
    for eval_result in evaluation['detailed_evaluations']:
        print(f"\n{eval_result['test_name']}: {eval_result['verdict']} (confidence: {eval_result['confidence']:.2f})")
        print(f"  Reasoning: {eval_result['reasoning'][:150]}...")

    # Salva resultados em JSON
    output_file = Path(__file__).parent / "test_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(evaluation, f, indent=2, ensure_ascii=False)

    print(f"\nResultados completos salvos em: {output_file}")

    return evaluation


if __name__ == "__main__":
    asyncio.run(run_all_tests())
