"""Analisa múltiplos arquivos Python e gera JSON."""

import asyncio
import json
import logging
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.agents.supervisor.supervisor import analyze_code_with_supervisor_v2

logging.basicConfig(level=logging.INFO)


async def analyze_folder(
    folder_path: str, output_file: str, project_name: str = "Code"
):
    folder = Path(folder_path)

    if not folder.exists():
        print(f"Erro: Pasta {folder_path} não encontrada")
        return

    py_files = list(folder.rglob("*.py"))

    if not py_files:
        print(f"Nenhum arquivo .py encontrado em {folder_path}")
        return

    print(f"Encontrados {len(py_files)} arquivos Python")
    print("Analisando...\n")

    all_smells = []

    for i, file_path in enumerate(py_files, 1):
        print(f"[{i}/{len(py_files)}] {file_path.name}...", end=" ")

        try:
            code = file_path.read_text(encoding="utf-8")
            result = await analyze_code_with_supervisor_v2(code, str(file_path), project_name)

            smells = result["code_smells"]
            all_smells.extend(smells)
            print(f"✓ ({len(smells)} smells)")
        except (UnicodeDecodeError, SyntaxError, OSError) as e:
            print(f"✗ {type(e).__name__}: {e}")
            logging.debug(traceback.format_exc())
        except Exception as e:
            print(f"✗ Erro inesperado: {e}")
            logging.error(
                f"Unexpected error processing {file_path}: {traceback.format_exc()}"
            )

    Path(output_file).write_text(
        json.dumps(all_smells, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"\n{'=' * 60}")
    print("Análise concluída!")
    print(f"Total de smells: {len(all_smells)}")
    print(f"Resultado salvo em: {output_file}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analisa arquivos Python em batch")
    parser.add_argument("folder", help="Pasta com arquivos Python")
    parser.add_argument(
        "-o", "--output", default="results/results.json", help="Arquivo de saída"
    )
    parser.add_argument("-p", "--project", default="Code", help="Nome do projeto")

    args = parser.parse_args()

    asyncio.run(analyze_folder(args.folder, args.output, args.project))
