"""Análise em batch de múltiplos arquivos Python."""

import asyncio
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.supervisor import analyze_code

log_file = f"logs/batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file, encoding="utf-8"), logging.StreamHandler()],
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def analyze_folder(
    folder_path: str, output_file: str, project_name: str = "Code"
):
    """Analisa todos arquivos .py de uma pasta."""
    folder = Path(folder_path)

    if not folder.exists():
        print(f"Erro: Pasta {folder_path} não encontrada")
        return

    py_files = list(folder.rglob("*.py"))
    if not py_files:
        print(f"Nenhum arquivo .py encontrado em {folder_path}")
        return

    print(f"Encontrados {len(py_files)} arquivos Python\n")
    logger.info(f"Iniciando análise de {len(py_files)} arquivos")

    all_smells = []

    for i, file_path in enumerate(py_files, 1):
        print(f"[{i}/{len(py_files)}] {file_path.name}...", end=" ")

        try:
            code = file_path.read_text(encoding="utf-8")
            result = await analyze_code(
                code, str(file_path), project_name, parallel=True
            )
            smells = result["code_smells"]
            all_smells.extend(smells)
            print(f"✓ ({len(smells)} smells)")
        except Exception as e:
            print(f"✗ {type(e).__name__}: {e}")
            logger.error(f"Erro em {file_path}: {e}")

    Path(output_file).write_text(
        json.dumps(all_smells, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"\n{'=' * 60}")
    print("Análise concluída!")
    print(f"Total: {len(all_smells)} smells")
    print(f"Resultado: {output_file}")
    print(f"Log: {log_file}")
    print(f"{'=' * 60}")

    logger.info(f"Concluído: {len(all_smells)} smells")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Análise em batch de arquivos Python")
    parser.add_argument("folder", help="Pasta com arquivos Python")
    parser.add_argument(
        "-o", "--output", default="results/results.json", help="Arquivo de saída"
    )
    parser.add_argument("-p", "--project", default="Code", help="Nome do projeto")

    args = parser.parse_args()
    asyncio.run(analyze_folder(args.folder, args.output, args.project))
