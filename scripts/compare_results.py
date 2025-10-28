"""
Compara resultados JSON do sistema com DPy.
"""

import json
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict


def normalize_smell_key(smell: Dict) -> str:
    """Cria chave única para um smell baseado em arquivo, tipo e método."""
    file = smell.get("File", "")
    smell_type = smell.get("Smell", smell.get("smell_type", "")).lower()
    method = smell.get("Method", smell.get("method_name", ""))

    return f"{file}::{smell_type}::{method}"


def load_json(file_path: str) -> List[Dict]:
    """Carrega arquivo JSON."""
    return json.loads(Path(file_path).read_text(encoding="utf-8"))


def compare_results(system_file: str, dpy_file: str):
    """Compara resultados do sistema com DPy."""

    system_smells = load_json(system_file)
    dpy_smells = load_json(dpy_file)

    system_keys = {normalize_smell_key(s) for s in system_smells}
    dpy_keys = {normalize_smell_key(s) for s in dpy_smells}

    true_positives = system_keys & dpy_keys
    false_positives = system_keys - dpy_keys
    false_negatives = dpy_keys - system_keys

    total_system = len(system_smells)
    total_dpy = len(dpy_smells)

    precision = len(true_positives) / total_system if total_system > 0 else 0
    recall = len(true_positives) / total_dpy if total_dpy > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print("="*80)
    print("COMPARAÇÃO DE RESULTADOS")
    print("="*80)
    print(f"\nTotal - Sistema: {total_system}")
    print(f"Total - DPy: {total_dpy}")
    print(f"\nTrue Positives (Concordância): {len(true_positives)}")
    print(f"False Positives (Só no Sistema): {len(false_positives)}")
    print(f"False Negatives (Só no DPy): {len(false_negatives)}")
    print(f"\n{'='*80}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    print(f"F1-Score: {f1:.2%}")
    print(f"{'='*80}")

    # Detalhamento por tipo de smell
    system_by_type = defaultdict(int)
    dpy_by_type = defaultdict(int)

    for smell in system_smells:
        smell_type = smell.get("Smell", smell.get("smell_type", "unknown"))
        system_by_type[smell_type] += 1

    for smell in dpy_smells:
        smell_type = smell.get("Smell", smell.get("smell_type", "unknown"))
        dpy_by_type[smell_type] += 1

    all_types = sorted(set(system_by_type.keys()) | set(dpy_by_type.keys()))

    print("\nDETALHAMENTO POR TIPO:")
    print("-"*80)
    print(f"{'Tipo':<30} {'Sistema':>12} {'DPy':>12} {'Diferença':>12}")
    print("-"*80)

    for smell_type in all_types:
        sys_count = system_by_type[smell_type]
        dpy_count = dpy_by_type[smell_type]
        diff = sys_count - dpy_count
        diff_str = f"{diff:+d}" if diff != 0 else "0"
        print(f"{smell_type:<30} {sys_count:>12} {dpy_count:>12} {diff_str:>12}")

    print("="*80)

    # Salva discrepâncias
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

        output_file = "discrepancies.json"
        Path(output_file).write_text(
            json.dumps(discrepancies, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"\nDiscrepâncias salvas em: {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compara resultados JSON")
    parser.add_argument("system", help="JSON do sistema")
    parser.add_argument("dpy", help="JSON do DPy")

    args = parser.parse_args()

    compare_results(args.system, args.dpy)
