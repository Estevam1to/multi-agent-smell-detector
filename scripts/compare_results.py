"""Compara resultados JSON do sistema com outras ferramentas."""

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List


def normalize_smell_key(smell: Dict) -> str:
    file = smell.get("File", "")

    file_name = Path(file).name if file else ""

    smell_type = smell.get("Smell", smell.get("smell_type", "")).lower()
    line_no = smell.get("Line no", "")

    return f"{file_name}::{smell_type}::{line_no}"


def load_json(file_path: str) -> List[Dict]:
    return json.loads(Path(file_path).read_text(encoding="utf-8"))


def calculate_metrics(
    system_keys: set, other_keys: set, total_system: int, total_other: int
) -> dict:
    true_positives = system_keys & other_keys
    false_positives = system_keys - other_keys
    false_negatives = other_keys - system_keys

    precision = len(true_positives) / total_system if total_system > 0 else 0
    recall = len(true_positives) / total_other if total_other > 0 else 0
    f1 = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def print_metrics(metrics: dict, total_system: int, total_other: int):
    print("=" * 80)
    print("COMPARAÇÃO DE RESULTADOS")
    print("=" * 80)
    print(f"\nTotal - Sistema: {total_system}")
    print(f"Total - Outra ferramenta: {total_other}")
    print(f"\nTrue Positives (Concordância): {len(metrics['true_positives'])}")
    print(f"False Positives (Só no Sistema): {len(metrics['false_positives'])}")
    print(
        f"False Negatives (Só na outra ferramenta): {len(metrics['false_negatives'])}"
    )
    print(f"\n{'=' * 80}")
    print(f"Precision: {metrics['precision']:.2%}")
    print(f"Recall: {metrics['recall']:.2%}")
    print(f"F1-Score: {metrics['f1']:.2%}")
    print(f"{'=' * 80}")


def print_by_type(system_smells: List[Dict], other_smells: List[Dict]):
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
    print("-" * 80)
    print(f"{'Tipo':<30} {'Sistema':>12} {'Outro':>12} {'Diferença':>12}")
    print("-" * 80)

    for smell_type in all_types:
        sys_count = system_by_type[smell_type]
        other_count = other_by_type[smell_type]
        diff = sys_count - other_count
        diff_str = f"{diff:+d}" if diff != 0 else "0"
        print(f"{smell_type:<30} {sys_count:>12} {other_count:>12} {diff_str:>12}")

    print("=" * 80)


def save_discrepancies(metrics: dict):
    if metrics["false_positives"] or metrics["false_negatives"]:
        discrepancies = {
            "false_positives": list(metrics["false_positives"]),
            "false_negatives": list(metrics["false_negatives"]),
            "metrics": {
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1_score": metrics["f1"],
            },
        }

        output_file = "results/discrepancies.json"
        Path(output_file).write_text(
            json.dumps(discrepancies, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"\nDiscrepâncias salvas em: {output_file}")


def compare_results(system_file: str, other_file: str):
    system_smells = load_json(system_file)
    other_smells = load_json(other_file)

    system_keys = {normalize_smell_key(s) for s in system_smells}
    other_keys = {normalize_smell_key(s) for s in other_smells}

    metrics = calculate_metrics(
        system_keys, other_keys, len(system_smells), len(other_smells)
    )

    print_metrics(metrics, len(system_smells), len(other_smells))
    print_by_type(system_smells, other_smells)
    save_discrepancies(metrics)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compara resultados JSON")
    parser.add_argument("system", help="JSON do sistema")
    parser.add_argument("other", help="JSON da outra ferramenta")

    args = parser.parse_args()

    compare_results(args.system, args.other)
