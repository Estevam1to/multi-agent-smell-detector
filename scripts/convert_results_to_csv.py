#!/usr/bin/env python3
"""Script para converter resultados JSON dos agentes para CSV no formato do ground truth.

Este script lê os resultados JSON gerados pelos agentes e converte para
CSV no mesmo formato do ground truth, incluindo ranges para smells de método.
"""

import ast
import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def find_method_range(code: str, method_name: str) -> Optional[Tuple[int, int]]:
    """Encontra o range (start_line, end_line) de um método usando AST."""
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == method_name:
                start_line = node.lineno
                end_line = node.end_lineno if hasattr(node, 'end_lineno') and node.end_lineno else start_line
                return (start_line, end_line)
    except SyntaxError:
        pass
    return None


def normalize_smell_name(smell: str) -> str:
    """Normaliza nome do smell."""
    return smell.strip().lower()


def is_method_level_smell(smell: str) -> bool:
    """Verifica se o smell é de nível de método."""
    normalized = normalize_smell_name(smell)
    return normalized in ["long method", "complex method"]


def get_file_name_from_path(file_path: str) -> str:
    """Extrai nome do arquivo do caminho completo."""
    return Path(file_path).name


def process_detection(
    detection: Dict,
    base_dir: Path,
    file_cache: Dict[str, str]
) -> Optional[Dict]:
    """Processa uma detecção e converte para formato CSV."""
    file_path = detection.get("File", "")
    if not file_path:
        return None
    
    # Construir caminho completo se necessário
    if not Path(file_path).exists():
        dataset_dir = base_dir / "dataset"
        for py_file in dataset_dir.rglob(Path(file_path).name):
            file_path = str(py_file.resolve())
            break
    
    if not Path(file_path).exists():
        return None
    
    # Carregar código do arquivo
    if file_path not in file_cache:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_cache[file_path] = f.read()
        except Exception:
            return None
    
    code = file_cache[file_path]
    file_name = get_file_name_from_path(file_path)
    
    smell = detection.get("Smell", "")
    method = detection.get("Method", "").strip()
    line_no = detection.get("Line_no", detection.get("Line no", "")).strip()
    description = detection.get("Description", "")
    
    # Normalizar line_no
    if line_no in ["nan", "None", "null", ""]:
        line_no = ""
    
    is_method_smell = is_method_level_smell(smell)
    
    result = {
        "Source": "dataset",
        "File": file_name,
        "Method": method if method else "file_level",
        "Code_Smell": smell,
        "Line_no": "",
        "Start_line": "",
        "End_line": "",
        "Details": description,
    }
    
    if is_method_smell:
        # Para smells de método, usar start_line e end_line da detecção ou extrair
        start_line = detection.get("start_line", "")
        end_line = detection.get("end_line", "")
        
        if start_line and end_line:
            result["Start_line"] = str(start_line)
            result["End_line"] = str(end_line)
        elif method:
            # Tentar extrair do código
            range_result = find_method_range(code, method)
            if range_result:
                result["Start_line"] = str(range_result[0])
                result["End_line"] = str(range_result[1])
            else:
                # Se não encontrou, usar valores vazios
                result["Start_line"] = ""
                result["End_line"] = ""
    else:
        # Para smells de linha específica, usar Line_no
        result["Line_no"] = line_no if line_no else ""
    
    return result


def convert_json_to_csv(json_path: Path, csv_path: Path, base_dir: Path):
    """Converte arquivo JSON de resultados para CSV."""
    print(f"Lendo: {json_path}")
    
    # Ler JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extrair lista de detecções
    if isinstance(data, list):
        detections = data
    elif isinstance(data, dict):
        detections = data.get("code_smells", [])
    else:
        print("❌ Formato JSON inválido")
        return
    
    print(f"Total de detecções: {len(detections)}")
    
    # Processar detecções
    file_cache = {}
    csv_rows = []
    
    for i, detection in enumerate(detections, 1):
        if i % 100 == 0:
            print(f"Processando detecção {i}/{len(detections)}...")
        
        try:
            csv_row = process_detection(detection, base_dir, file_cache)
            if csv_row:
                csv_rows.append(csv_row)
        except Exception as e:
            print(f"⚠️  Erro ao processar detecção {i}: {e}")
    
    # Salvar CSV
    fieldnames = [
        "Source",
        "File",
        "Method",
        "Code_Smell",
        "Line_no",
        "Start_line",
        "End_line",
        "Details",
    ]
    
    print(f"Salvando: {csv_path}")
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
    
    print(f"✅ Convertido: {len(csv_rows)} linhas salvas em {csv_path}")


def main():
    """Converte resultados JSON para CSV."""
    base_dir = Path(__file__).parent.parent
    results_dir = base_dir / "results"
    
    print("=" * 80)
    print("CONVERSÃO DE RESULTADOS JSON PARA CSV")
    print("=" * 80)
    
    # Encontrar arquivos JSON de resultados (podem estar em results/ ou results/json/)
    json_dir = results_dir / "json"
    if not json_dir.exists():
        json_dir = results_dir
    
    json_files = [
        json_dir / "results_with_complete_prompts.json",
        json_dir / "results_simple_prompt.json",
    ]
    
    # Também verificar no diretório raiz de results
    for json_file in [
        results_dir / "results_with_complete_prompts.json",
        results_dir / "results_simple_prompt.json",
    ]:
        if json_file.exists() and json_file not in json_files:
            json_files.append(json_file)
    
    for json_path in json_files:
        if not json_path.exists():
            print(f"⚠️  Arquivo não encontrado: {json_path}")
            continue
        
        # Gerar nome do CSV e salvar em results/csv/
        csv_dir = results_dir / "csv"
        csv_dir.mkdir(exist_ok=True)
        csv_name = json_path.stem + ".csv"
        csv_path = csv_dir / csv_name
        
        print()
        print(f"Convertendo: {json_path.name}")
        convert_json_to_csv(json_path, csv_path, base_dir)
    
    print()
    print("=" * 80)
    print("CONCLUÍDO!")
    print("=" * 80)


if __name__ == "__main__":
    main()

