#!/usr/bin/env python3
"""Script para gerar novo ground truth com ranges de métodos.

Este script analisa os arquivos Python do dataset e gera um CSV
com formato unificado incluindo ranges (start_line, end_line) para
smells de método e Line_no para smells de linha específica.
"""

import ast
import csv
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


def find_method_range_simple(code_lines: List[str], method_name: str) -> Optional[Tuple[int, int]]:
    """Encontra range de método usando busca simples (fallback)."""
    start_line = None
    indent_level = None
    
    for i, line in enumerate(code_lines, 1):
        if f"def {method_name}(" in line or f"def {method_name}:" in line:
            start_line = i
            indent_level = len(line) - len(line.lstrip())
            break
    
    if start_line is None:
        return None
    
    # Encontrar fim do método
    for i in range(start_line, len(code_lines)):
        line = code_lines[i]
        if i == start_line:
            continue
        current_indent = len(line) - len(line.lstrip())
        if line.strip() and current_indent <= indent_level and not line.strip().startswith('#'):
            return (start_line, i - 1)
    
    return (start_line, len(code_lines))


def extract_line_number(details: str) -> str:
    """Extrai número da linha do campo Details."""
    if not details:
        return ""
    
    patterns = [
        r"at line (\d+)",
        r"Line (\d+)",
        r"line (\d+)",
        r"Line (\d+) has",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, details, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return ""


def normalize_smell_name(smell: str) -> str:
    """Normaliza nome do smell."""
    return smell.strip().lower()


def is_method_level_smell(smell: str) -> bool:
    """Verifica se o smell é de nível de método."""
    normalized = normalize_smell_name(smell)
    return normalized in ["long method", "complex method"]


def build_file_path(source: str, file_name: str, base_dir: Path) -> str:
    """Constrói caminho completo do arquivo."""
    dataset_dir = base_dir / "dataset"
    for py_file in dataset_dir.rglob(file_name):
        return str(py_file.resolve())
    return ""


def process_ground_truth_row(
    row: Dict,
    base_dir: Path,
    file_cache: Dict[str, List[str]]
) -> Optional[Dict]:
    """Processa uma linha do ground truth e adiciona ranges."""
    source = str(row.get("Source", "")).strip()
    file_name = str(row.get("File", "")).strip()
    lineon = str(row.get("Lineon", "")).strip()
    code_smell = str(row.get("Code Smell", "")).strip()
    details = str(row.get("Details", "")).strip()
    
    # Construir caminho do arquivo
    file_path = build_file_path(source, file_name, base_dir)
    if not file_path or not Path(file_path).exists():
        print(f"⚠️  Arquivo não encontrado: {file_name}")
        return None
    
    # Carregar código do arquivo
    if file_path not in file_cache:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_cache[file_path] = f.readlines()
        except Exception as e:
            print(f"⚠️  Erro ao ler {file_path}: {e}")
            return None
    
    code_lines = file_cache[file_path]
    code = ''.join(code_lines)
    
    # Determinar se é smell de método ou linha específica
    is_method_smell = is_method_level_smell(code_smell)
    method = "" if lineon == "file_level" else lineon
    
    result = {
        "Source": source,
        "File": file_name,
        "Method": method,
        "Code_Smell": code_smell,
        "Line_no": "",
        "Start_line": "",
        "End_line": "",
        "Details": details,
    }
    
    if is_method_smell:
        # Para smells de método, extrair range
        if method:
            # Tentar AST primeiro
            range_result = find_method_range(code, method)
            if not range_result:
                # Fallback para busca simples
                range_result = find_method_range_simple(code_lines, method)
            
            if range_result:
                result["Start_line"] = str(range_result[0])
                result["End_line"] = str(range_result[1])
            else:
                print(f"⚠️  Método '{method}' não encontrado em {file_name}")
                return None
        else:
            print(f"⚠️  Método vazio para smell de método em {file_name}")
            return None
    else:
        # Para smells de linha específica, extrair Line_no
        line_no = extract_line_number(details)
        result["Line_no"] = line_no if line_no else ""
    
    return result


def main():
    """Gera novo ground truth com ranges."""
    base_dir = Path(__file__).parent.parent
    old_gt_path = base_dir / "dataset" / "ground_truth" / "ground_truth_manual.csv"
    new_gt_path = base_dir / "dataset" / "ground_truth" / "ground_truth_with_ranges.csv"
    
    if not old_gt_path.exists():
        print(f"❌ Ground truth antigo não encontrado: {old_gt_path}")
        return
    
    print("=" * 80)
    print("GERAÇÃO DE NOVO GROUND TRUTH COM RANGES")
    print("=" * 80)
    print(f"Lendo: {old_gt_path}")
    print(f"Gerando: {new_gt_path}")
    print()
    
    # Ler ground truth antigo
    rows = []
    with open(old_gt_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"Total de linhas no ground truth antigo: {len(rows)}")
    
    # Processar cada linha
    file_cache = {}
    new_rows = []
    errors = []
    
    for i, row in enumerate(rows, 1):
        if i % 50 == 0:
            print(f"Processando linha {i}/{len(rows)}...")
        
        try:
            new_row = process_ground_truth_row(row, base_dir, file_cache)
            if new_row:
                new_rows.append(new_row)
            else:
                errors.append(f"Linha {i}: {row.get('File', '?')} - {row.get('Code Smell', '?')}")
        except Exception as e:
            errors.append(f"Linha {i}: Erro - {e}")
    
    # Salvar novo ground truth
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
    
    with open(new_gt_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_rows)
    
    print()
    print("=" * 80)
    print("CONCLUÍDO!")
    print("=" * 80)
    print(f"✅ Total de linhas processadas: {len(new_rows)}")
    print(f"⚠️  Erros/ignorados: {len(errors)}")
    print(f"📄 Arquivo gerado: {new_gt_path}")
    
    if errors:
        print("\n⚠️  Erros encontrados:")
        for error in errors[:10]:  # Mostrar apenas os primeiros 10
            print(f"   - {error}")
        if len(errors) > 10:
            print(f"   ... e mais {len(errors) - 10} erros")


if __name__ == "__main__":
    main()

