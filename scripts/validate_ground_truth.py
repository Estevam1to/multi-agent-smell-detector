#!/usr/bin/env python3
"""
Validador do Ground Truth Manual
Valida se cada detecção realmente corresponde a um smell válido no código.
"""

import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class GroundTruthValidator:
    """Validador principal do ground truth."""
    
    def __init__(self, ground_truth_path: str, dataset_path: str):
        self.ground_truth_path = ground_truth_path
        self.dataset_path = Path(dataset_path)
        self.results = {
            'valid': [],
            'invalid': [],
            'warnings': [],
            'stats': defaultdict(int)
        }
        self.file_cache = {}
        
    def load_ground_truth(self):
        """Carrega o ground truth do JSON."""
        with open(self.ground_truth_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_file_content(self, file_path: str) -> Optional[List[str]]:
        """Carrega conteúdo do arquivo (com cache)."""
        if file_path not in self.file_cache:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.file_cache[file_path] = f.readlines()
            except Exception as e:
                return None
        return self.file_cache[file_path]
    
    def find_method(self, file_path: str, method_name: str) -> Optional[Tuple[int, int]]:
        """Encontra início e fim de um método. Retorna (linha_inicio, linha_fim)."""
        lines = self.get_file_content(file_path)
        if not lines:
            return None
        
        start_line = None
        indent_level = None
        
        for i, line in enumerate(lines, 1):
            # Procurar definição do método
            if f"def {method_name}(" in line or f"def {method_name}:" in line:
                start_line = i
                indent_level = len(line) - len(line.lstrip())
                break
        
        if start_line is None:
            return None
        
        # Encontrar fim do método (próxima linha com mesmo ou menor indentação)
        for i in range(start_line, len(lines)):
            line = lines[i]
            if i == start_line:
                continue
            current_indent = len(line) - len(line.lstrip())
            if line.strip() and current_indent <= indent_level and not line.strip().startswith('#'):
                return (start_line, i - 1)
        
        return (start_line, len(lines))
    
    def validate_magic_number(self, detection: Dict) -> Dict:
        """Valida Magic Number."""
        file_path = detection['File']
        line_no = detection.get('Line no', '').strip()
        details = detection.get('Details', '')
        method = detection.get('Method', '').strip()
        
        if not line_no:
            return {'status': 'invalid', 'reason': 'Linha não especificada'}
        
        try:
            line_num = int(line_no)
        except ValueError:
            return {'status': 'invalid', 'reason': f'Linha inválida: {line_no}'}
        
        lines = self.get_file_content(file_path)
        if not lines or line_num < 1 or line_num > len(lines):
            return {'status': 'invalid', 'reason': f'Linha {line_num} não existe'}
        
        line_content = lines[line_num - 1]
        
        # Extrair número do Details
        match = re.search(r'Magic number ([\d.eE+-]+)', details)
        if not match:
            return {'status': 'warning', 'reason': 'Não foi possível extrair número do Details'}
        
        expected_number = match.group(1)
        
        # Verificar se o número está na linha
        # Padrões: número isolado, em expressões, etc.
        number_patterns = [
            rf'\b{re.escape(expected_number)}\b',
            rf'{re.escape(expected_number)}',
        ]
        
        found = False
        for pattern in number_patterns:
            if re.search(pattern, line_content):
                found = True
                break
        
        if not found:
            return {'status': 'invalid', 'reason': f'Número {expected_number} não encontrado na linha {line_num}'}
        
        # Ignorar 0, 1, -1
        try:
            num_value = float(expected_number)
            if num_value in [0, 1, -1]:
                return {'status': 'warning', 'reason': f'Número {expected_number} é trivial (0, 1, ou -1)'}
        except:
            pass
        
        return {'status': 'valid'}
    
    def validate_long_method(self, detection: Dict) -> Dict:
        """Valida Long Method."""
        file_path = detection['File']
        method = detection.get('Method', '').strip()
        details = detection.get('Details', '')
        
        if not method:
            return {'status': 'invalid', 'reason': 'Método não especificado'}
        
        method_range = self.find_method(file_path, method)
        if not method_range:
            return {'status': 'invalid', 'reason': f'Método "{method}" não encontrado'}
        
        start_line, end_line = method_range
        actual_lines = end_line - start_line + 1
        
        # Extrair número de linhas do Details
        match = re.search(r'has (\d+) lines', details)
        if not match:
            return {'status': 'warning', 'reason': 'Não foi possível extrair número de linhas do Details'}
        
        expected_lines = int(match.group(1))
        
        # Verificar se realmente tem mais de 67 linhas
        if actual_lines <= 67:
            return {'status': 'invalid', 'reason': f'Método tem apenas {actual_lines} linhas (threshold: 67)'}
        
        # Verificar se o número de linhas está correto
        if abs(actual_lines - expected_lines) > 5:  # Tolerância de 5 linhas
            return {'status': 'warning', 'reason': f'Discrepância: esperado {expected_lines}, encontrado {actual_lines}'}
        
        return {'status': 'valid'}
    
    def validate_long_message_chain(self, detection: Dict) -> Dict:
        """Valida Long Message Chain."""
        file_path = detection['File']
        line_no = detection.get('Line no', '').strip()
        details = detection.get('Details', '')
        method = detection.get('Method', '').strip()
        
        if not line_no:
            return {'status': 'invalid', 'reason': 'Linha não especificada'}
        
        try:
            line_num = int(line_no)
        except ValueError:
            return {'status': 'invalid', 'reason': f'Linha inválida: {line_no}'}
        
        lines = self.get_file_content(file_path)
        if not lines or line_num < 1 or line_num > len(lines):
            return {'status': 'invalid', 'reason': f'Linha {line_num} não existe'}
        
        line_content = lines[line_num - 1]
        
        # Contar pontos (métodos encadeados)
        dots = line_content.count('.')
        
        # Extrair número esperado do Details
        match = re.search(r'has (\d+) chained methods', details)
        if match:
            expected_chains = int(match.group(1))
            # Para ter N métodos encadeados, precisa de N-1 pontos
            # Ex: obj.met1.met2.met3 = 3 métodos, 2 pontos
            # Mas o threshold é > 2 métodos, então precisa >= 3 métodos = >= 2 pontos
            # Na verdade, se tem 3 métodos encadeados, tem 2 pontos
            # Se tem > 2 métodos encadeados, precisa >= 2 pontos
            if dots < 2:
                return {'status': 'invalid', 'reason': f'Apenas {dots} ponto(s) encontrado(s), esperado >= 2 para cadeia'}
        else:
            # Se não tem informação, verificar se tem pelo menos 2 pontos
            if dots < 2:
                return {'status': 'invalid', 'reason': f'Apenas {dots} ponto(s) encontrado(s)'}
        
        return {'status': 'valid'}
    
    def validate_long_lambda(self, detection: Dict) -> Dict:
        """Valida Long Lambda Function."""
        file_path = detection['File']
        line_no = detection.get('Line no', '').strip()
        details = detection.get('Details', '')
        
        if not line_no:
            return {'status': 'invalid', 'reason': 'Linha não especificada'}
        
        try:
            line_num = int(line_no)
        except ValueError:
            return {'status': 'invalid', 'reason': f'Linha inválida: {line_no}'}
        
        lines = self.get_file_content(file_path)
        if not lines or line_num < 1 or line_num > len(lines):
            return {'status': 'invalid', 'reason': f'Linha {line_num} não existe'}
        
        line_content = lines[line_num - 1]
        
        # Verificar se há lambda
        if 'lambda' not in line_content.lower():
            return {'status': 'invalid', 'reason': 'Não há lambda na linha'}
        
        # Extrair comprimento do Details
        match = re.search(r'has (\d+) characters', details)
        if not match:
            return {'status': 'warning', 'reason': 'Não foi possível extrair comprimento do Details'}
        
        expected_chars = int(match.group(1))
        
        # Encontrar a expressão lambda e calcular comprimento
        # Procurar por lambda ... : ...
        lambda_match = re.search(r'lambda[^:]*:[^,)]*', line_content)
        if lambda_match:
            lambda_expr = lambda_match.group(0)
            actual_chars = len(lambda_expr)
            
            if actual_chars <= 80:
                return {'status': 'invalid', 'reason': f'Lambda tem apenas {actual_chars} caracteres (threshold: 80)'}
            
            if abs(actual_chars - expected_chars) > 10:
                return {'status': 'warning', 'reason': f'Discrepância: esperado {expected_chars}, encontrado {actual_chars}'}
        else:
            return {'status': 'warning', 'reason': 'Não foi possível extrair expressão lambda'}
        
        return {'status': 'valid'}
    
    def validate(self, detection: Dict) -> Dict:
        """Valida uma detecção baseado no tipo de smell."""
        smell_type = detection.get('Smell', '')
        file_path = detection['File']
        
        # Verificar se arquivo existe
        if not os.path.exists(file_path):
            return {
                'status': 'invalid',
                'reason': f'Arquivo não encontrado: {file_path}',
                'detection': detection
            }
        
        # Validadores por tipo
        validators = {
            'Magic Number': self.validate_magic_number,
            'Long Method': self.validate_long_method,
            'Long Message Chain': self.validate_long_message_chain,
            'Long Lambda Function': self.validate_long_lambda,
            # Adicionar outros validadores aqui
        }
        
        validator = validators.get(smell_type)
        if not validator:
            return {
                'status': 'warning',
                'reason': f'Validador não implementado para: {smell_type}',
                'detection': detection
            }
        
        result = validator(detection)
        result['detection'] = detection
        result['smell_type'] = smell_type
        return result
    
    def validate_all(self):
        """Valida todas as detecções do ground truth."""
        ground_truth = self.load_ground_truth()
        
        print(f"Validando {len(ground_truth)} detecções...")
        
        for i, detection in enumerate(ground_truth, 1):
            result = self.validate(detection)
            status = result['status']
            # Mapear 'warning' para 'warnings'
            if status == 'warning':
                status = 'warnings'
            self.results[status].append(result)
            self.results['stats'][status] += 1
            
            if i % 50 == 0:
                print(f"  Processadas: {i}/{len(ground_truth)}")
    
    def generate_report(self) -> str:
        """Gera relatório de validação."""
        report = []
        report.append("=" * 80)
        report.append("RELATÓRIO DE VALIDAÇÃO DO GROUND TRUTH")
        report.append("=" * 80)
        
        total = sum(self.results['stats'].values())
        report.append(f"\nTotal de detecções: {total}")
        report.append(f"✓ Válidas: {self.results['stats']['valid']}")
        report.append(f"❌ Inválidas: {self.results['stats']['invalid']}")
        report.append(f"⚠️  Avisos: {self.results['stats']['warnings']}")
        
        # Detalhes de inválidas
        if self.results['invalid']:
            report.append("\n" + "=" * 80)
            report.append("DETECÇÕES INVÁLIDAS (primeiras 20):")
            report.append("=" * 80)
            for result in self.results['invalid'][:20]:
                det = result['detection']
                file_name = det['File'].split('/')[-1]
                report.append(f"\n{file_name} | {result['smell_type']} | {result.get('reason', 'N/A')}")
        
        return "\n".join(report)


def main():
    base_dir = Path(__file__).parent.parent
    ground_truth_path = base_dir / "results" / "ground_truth_manual.json"
    dataset_path = base_dir / "dataset"
    
    validator = GroundTruthValidator(str(ground_truth_path), str(dataset_path))
    validator.validate_all()
    
    report = validator.generate_report()
    print(report)
    
    # Salvar relatório
    report_path = base_dir / "results" / "validation_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✓ Relatório salvo em: {report_path}")


if __name__ == "__main__":
    main()

