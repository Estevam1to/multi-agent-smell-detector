"""
Script para comparar resultados com a ferramenta DPy da Designite.

Este script permite comparar as detecções do Multi-Agent Smell Detector
com os resultados da ferramenta DPy (Designite Python).
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from supervisor import analyze_code_with_supervisor


class DPyComparator:
    """
    Comparador entre Multi-Agent Smell Detector e DPy.

    Permite comparar resultados de detecção de code smells entre
    nossa ferramenta e a DPy da Designite.
    """

    # Mapeamento entre nossos smells e os da DPy
    SMELL_MAPPING = {
        "long_method": "Long Method",
        "long_parameter_list": "Long Parameter List",
        "long_statement": "Long Statement",
        "long_identifier": "Long Identifier",
        "empty_catch_block": "Empty Catch Block",
        "complex_method": "Complex Method",
        "complex_conditional": "Complex Conditional",
        "missing_default": "Missing Default",
        "long_lambda_function": "Long Lambda Function",
        "long_message_chain": "Long Message Chain",
        "magic_number": "Magic Number",
    }

    def __init__(self):
        """Inicializa o comparador."""
        pass

    async def analyze_with_our_tool(self, code: str) -> Dict:
        """
        Analisa código com nossa ferramenta.

        Args:
            code: Código Python a ser analisado

        Returns:
            Dicionário com resultados
        """
        return await analyze_code_with_supervisor(code)

    def load_dpy_results(self, dpy_file: Path) -> Dict:
        """
        Carrega resultados da DPy de um arquivo JSON.

        Args:
            dpy_file: Caminho para arquivo JSON da DPy

        Returns:
            Dicionário com resultados da DPy
        """
        with open(dpy_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def compare_results(
        self, our_results: Dict, dpy_results: Dict
    ) -> Dict:
        """
        Compara resultados entre as duas ferramentas.

        Args:
            our_results: Resultados da nossa ferramenta
            dpy_results: Resultados da DPy

        Returns:
            Dicionário com comparação
        """
        comparison = {
            "our_tool": {
                "total_smells": our_results["total_smells_detected"],
                "smells_by_type": {},
            },
            "dpy": {
                "total_smells": 0,
                "smells_by_type": {},
            },
            "agreement": {
                "matching_smells": 0,
                "only_our_tool": [],
                "only_dpy": [],
            },
            "metrics": {},
        }

        # Conta smells por tipo da nossa ferramenta
        for smell in our_results["code_smells"]:
            smell_type = smell["smell_type"]
            comparison["our_tool"]["smells_by_type"][smell_type] = (
                comparison["our_tool"]["smells_by_type"].get(smell_type, 0) + 1
            )

        # Processa resultados da DPy (formato pode variar)
        # Este é um exemplo genérico - ajuste conforme formato real da DPy
        if "smells" in dpy_results:
            for smell in dpy_results["smells"]:
                smell_type = smell.get("type", "unknown")
                comparison["dpy"]["smells_by_type"][smell_type] = (
                    comparison["dpy"]["smells_by_type"].get(smell_type, 0) + 1
                )
                comparison["dpy"]["total_smells"] += 1

        # Calcula concordância
        our_types = set(comparison["our_tool"]["smells_by_type"].keys())
        dpy_types = set(comparison["dpy"]["smells_by_type"].keys())

        matching = our_types & dpy_types
        comparison["agreement"]["matching_smells"] = len(matching)
        comparison["agreement"]["only_our_tool"] = list(our_types - dpy_types)
        comparison["agreement"]["only_dpy"] = list(dpy_types - our_types)

        # Calcula métricas
        total_unique = len(our_types | dpy_types)
        if total_unique > 0:
            comparison["metrics"]["jaccard_similarity"] = len(matching) / total_unique
        else:
            comparison["metrics"]["jaccard_similarity"] = 0

        return comparison

    async def run_comparative_analysis(
        self, code_file: Path, dpy_results_file: Path = None
    ) -> Dict:
        """
        Executa análise comparativa completa.

        Args:
            code_file: Arquivo com código Python
            dpy_results_file: Arquivo com resultados da DPy (opcional)

        Returns:
            Dicionário com análise comparativa
        """
        # Lê o código
        with open(code_file, "r", encoding="utf-8") as f:
            code = f.read()

        print(f"\nAnalisando arquivo: {code_file}")
        print("=" * 80)

        # Analisa com nossa ferramenta
        print("\n1. Analisando com Multi-Agent Smell Detector...")
        our_results = await self.analyze_with_our_tool(code)

        print(f"   ✓ Detectados {our_results['total_smells_detected']} code smells")

        # Se houver arquivo DPy, compara
        if dpy_results_file and dpy_results_file.exists():
            print("\n2. Carregando resultados da DPy...")
            dpy_results = self.load_dpy_results(dpy_results_file)
            print(f"   ✓ Carregado")

            print("\n3. Comparando resultados...")
            comparison = self.compare_results(our_results, dpy_results)

            print(f"\n{'=' * 80}")
            print("RESULTADOS DA COMPARAÇÃO")
            print("=" * 80)

            print(f"\nNossa ferramenta: {comparison['our_tool']['total_smells']} smells")
            print(f"DPy:              {comparison['dpy']['total_smells']} smells")
            print(
                f"\nSmells em comum:  {comparison['agreement']['matching_smells']}"
            )
            print(
                f"Apenas nossa:     {len(comparison['agreement']['only_our_tool'])}"
            )
            print(f"Apenas DPy:       {len(comparison['agreement']['only_dpy'])}")

            print(
                f"\nJaccard Similarity: {comparison['metrics']['jaccard_similarity']:.2%}"
            )

            return comparison
        else:
            print(
                "\n⚠ Arquivo de resultados DPy não fornecido - exibindo apenas nossos resultados"
            )
            return {"our_tool": our_results}


async def main():
    """Função principal."""
    print("\n" + "=" * 80)
    print("COMPARAÇÃO: Multi-Agent Smell Detector vs DPy (Designite)")
    print("=" * 80)

    comparator = DPyComparator()

    # Exemplo de uso
    # Para usar: python compare_with_dpy.py <arquivo.py> [<dpy_results.json>]
    if len(sys.argv) < 2:
        print("\nUso: python compare_with_dpy.py <arquivo.py> [<dpy_results.json>]")
        print("\nExemplo sem DPy:")
        print("  python compare_with_dpy.py meu_codigo.py")
        print("\nExemplo com DPy:")
        print("  python compare_with_dpy.py meu_codigo.py dpy_results.json")
        return

    code_file = Path(sys.argv[1])
    dpy_file = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    if not code_file.exists():
        print(f"\n❌ Erro: Arquivo não encontrado: {code_file}")
        return

    # Executa análise comparativa
    results = await comparator.run_comparative_analysis(code_file, dpy_file)

    # Salva resultados
    output_file = Path("comparison_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Resultados salvos em: {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
