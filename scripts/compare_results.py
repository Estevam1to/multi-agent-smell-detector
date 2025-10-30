"""Compara resultados JSON do sistema com outras ferramentas."""

import json
from pathlib import Path
from typing import Dict, List
from collections import defaultdict


def normalize_smell_key(smell: Dict) -> str:
    file = smell.get("File", "")
    # Normalizar path: pegar apenas o nome do arquivo
    from pathlib import Path
    file_name = Path(file).name if file else ""
    
    smell_type = smell.get("Smell", smell.get("smell_type", "")).lower()
    method = smell.get("Method", smell.get("method_name", ""))
    line_no = smell.get("Line no", "")
    
    # Usar file_name + smell_type + line_no para melhor matching
    return f"{file_name}::{smell_type}::{line_no}"


def load_json(file_path: str) -> List[Dict]:
    return json.loads(Path(file_path).read_text(encoding="utf-8"))


def compare_results(system_file: str, other_file: str):
    """
    Compara dois arquivos JSON com resultados de detecção de code smells.

    Args:
        system_file: Caminho para o JSON com resultados do sistema
        other_file: Caminho para o JSON com resultados de outra ferramenta

    Formato esperado dos arquivos JSON:
        Lista de objetos com campos: File, Smell (ou smell_type), Method (ou method_name)

    Saída:
        Imprime métricas (precision, recall, F1-score) e detalhamento por tipo.
        Salva discrepâncias em 'discrepancies.json' se houver.
    """

    system_smells = load_json(system_file)
    other_smells = load_json(other_file)

    system_keys = {normalize_smell_key(s) for s in system_smells}
    other_keys = {normalize_smell_key(s) for s in other_smells}

    true_positives = system_keys & other_keys
    false_positives = system_keys - other_keys
    false_negatives = other_keys - system_keys

    total_system = len(system_smells)
    total_other = len(other_smells)

    precision = len(true_positives) / total_system if total_system > 0 else 0
    recall = len(true_positives) / total_other if total_other > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print("="*80)
    print("COMPARAÇÃO DE RESULTADOS")
    print("="*80)
    print(f"\nTotal - Sistema: {total_system}")
    print(f"Total - Outra ferramenta: {total_other}")
    print(f"\nTrue Positives (Concordância): {len(true_positives)}")
    print(f"False Positives (Só no Sistema): {len(false_positives)}")
    print(f"False Negatives (Só na outra ferramenta): {len(false_negatives)}")
    print(f"\n{'='*80}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    print(f"F1-Score: {f1:.2%}")
    print(f"{'='*80}")

    system_by_type = defaultdict(int)
    other_by_type = defaultdict(int)

    for smell in system_smells:
        smell_type = smell.get("Smell", smell.get("smell_type", "unknown"))
        system_by_type[smell_type] += 1

    for smell in other_smells:
        smell_type = smell.get("Smell", smell.get("smell_type", "unknown"))
        other_by_type[smell_type] += 1

    all_types = sorted(set(system_by_type.keys()) | set(other_by_type.keys()))

    print("\nDETALHAMENTO POR TIPO:")
    print("-"*80)
    print(f"{'Tipo':<30} {'Sistema':>12} {'Outro':>12} {'Diferença':>12}")
    print("-"*80)

    for smell_type in all_types:
        sys_count = system_by_type[smell_type]
        other_count = other_by_type[smell_type]
        diff = sys_count - other_count
        diff_str = f"{diff:+d}" if diff != 0 else "0"
        print(f"{smell_type:<30} {sys_count:>12} {other_count:>12} {diff_str:>12}")

    print("="*80)

    if false_positives or false_negatives:
        discrepancies = {
            "false_positives": list(false_positives),
            "false_negatives": list(false_negatives),
            "metrics": {
                "precision": precision,
                "recall": recall,
                "f1_score": f1
            }
        }

        output_file = "results/discrepancies.json"
        Path(output_file).write_text(
            json.dumps(discrepancies, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"\nDiscrepâncias salvas em: {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compara resultados JSON")
    parser.add_argument("system", help="JSON do sistema")
    parser.add_argument("other", help="JSON da outra ferramenta")

    args = parser.parse_args()

    compare_results(args.system, args.other)
