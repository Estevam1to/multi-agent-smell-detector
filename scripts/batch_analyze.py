"""
Analisa múltiplos arquivos Python em uma pasta e gera JSON de saída.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agents.supervisor import analyze_code_with_supervisor_v2
from utils.structured_formatter import StructuredFormatter


async def analyze_file(file_path: Path, project_name: str = "Code") -> List[Dict[str, Any]]:
    """Analisa um arquivo Python e retorna smells no formato estruturado."""
    code = file_path.read_text(encoding="utf-8")

    result = await analyze_code_with_supervisor_v2(code)

    if result["total_smells_detected"] == 0:
        return []

    formatter = StructuredFormatter(code, str(file_path))
    smells = result["code_smells"]

    for smell in smells:
        smell["File"] = str(file_path)
        smell["Project"] = project_name
        smell["Package"] = formatter.parser.get_package_name()
        smell["Module"] = formatter.parser.get_module_name()

        if "method_name" in smell:
            smell["Method"] = smell["method_name"]
        if "line_start" in smell and "line_end" in smell:
            smell["Line no"] = f"{smell['line_start']} - {smell['line_end']}"
        elif "line_number" in smell:
            smell["Line no"] = str(smell["line_number"])

        smell_type = smell.get("smell_type", "")
        smell["Smell"] = smell_type.replace("_", " ").title()

        smell["Description"] = smell.get("suggestion", "")

    return smells


async def analyze_folder(folder_path: str, output_file: str, project_name: str = "Code"):
    """Analisa todos os arquivos .py em uma pasta."""
    folder = Path(folder_path)

    if not folder.exists():
        print(f"Erro: Pasta {folder_path} não encontrada")
        return

    py_files = list(folder.rglob("*.py"))

    if not py_files:
        print(f"Nenhum arquivo .py encontrado em {folder_path}")
        return

    print(f"Encontrados {len(py_files)} arquivos Python")
    print(f"Analisando com supervisor V2 (structured output)...\n")

    all_smells = []

    for i, file_path in enumerate(py_files, 1):
        print(f"[{i}/{len(py_files)}] {file_path.name}...", end=" ")

        try:
            smells = await analyze_file(file_path, project_name)
            all_smells.extend(smells)
            print(f"✓ ({len(smells)} smells)")
        except Exception as e:
            print(f"✗ Erro: {e}")

    output_path = Path(output_file)
    output_path.write_text(json.dumps(all_smells, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"Análise concluída!")
    print(f"Total de smells: {len(all_smells)}")
    print(f"Resultado salvo em: {output_file}")
    print(f"{'='*60}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analisa arquivos Python em batch")
    parser.add_argument("folder", help="Pasta com arquivos Python")
    parser.add_argument("-o", "--output", default="results.json", help="Arquivo de saída")
    parser.add_argument("-p", "--project", default="Code", help="Nome do projeto")

    args = parser.parse_args()

    asyncio.run(analyze_folder(args.folder, args.output, args.project))
