# Script Bandit para Análise de Segurança

Este script executa o Bandit e gera um CSV com vulnerabilidades de segurança encontradas em código Python.

## Sobre o Bandit

O Bandit é uma ferramenta projetada para encontrar problemas comuns de segurança em código Python. Ele analisa o código AST (Abstract Syntax Tree) e procura por padrões conhecidos que podem representar vulnerabilidades.

## Uso

### Analisar um arquivo específico:
```bash
python src/scripts/run_bandit_script.py arquivo.py -o results/security_results.csv
```

### Analisar um diretório inteiro:
```bash
python src/scripts/run_bandit_script.py src/ -o results/security_src.csv
```

### Analisar arquivos de teste:
```bash
python src/scripts/run_bandit_script.py code-tests/ -o results/security_tests.csv
```

## Formato do CSV

O CSV gerado contém as seguintes colunas:

- **file**: Caminho do arquivo onde a vulnerabilidade foi encontrada
- **test_id**: ID do teste do Bandit (ex: B311, B324)
- **test_name**: Nome do teste (ex: blacklist, hashlib)
- **issue_severity**: Severidade (LOW, MEDIUM, HIGH)
- **issue_confidence**: Confiança (LOW, MEDIUM, HIGH)
- **issue_text**: Descrição da vulnerabilidade
- **line_number**: Número da linha onde foi encontrada
- **line_range**: Intervalo de linhas afetadas
- **code**: Código problemático
- **severity_description**: Descrição detalhada da severidade
- **confidence_description**: Descrição detalhada da confiança
- **more_info**: Link para mais informações

## Exemplo de Saída

```csv
file,test_id,test_name,issue_severity,issue_confidence,issue_text,line_number,line_range,code,severity_description,confidence_description,more_info
code-tests/teste_8.py,B324,hashlib,HIGH,HIGH,Use of weak MD5 hash for security. Consider usedforsecurity=False,31,31-31,"return hashlib.md5(password.encode()).hexdigest()",High risk security vulnerability that requires immediate attention,High confidence - very likely a real security issue,https://bandit.readthedocs.io/en/1.8.3/plugins/b324_hashlib.html
```

## Tipos de Vulnerabilidades Detectadas

### Severidade HIGH (Alta)
- **hashlib**: Uso de algoritmos de hash fracos (MD5, SHA1)
- **hardcoded_password**: Senhas codificadas no código
- **sql_injection**: Possíveis vulnerabilidades de SQL injection

### Severidade MEDIUM (Média)
- **hardcoded_sql_expressions**: Expressões SQL codificadas
- **subprocess_popen_with_shell_equals_true**: Uso inseguro de subprocess
- **yaml_load**: Uso inseguro do yaml.load()

### Severidade LOW (Baixa)
- **blacklist**: Uso de funções potencialmente inseguras
- **hardcoded_tmp_directory**: Diretórios temporários codificados
- **random**: Uso de geradores pseudo-aleatórios para segurança

## Resultados dos Testes

### Análise dos Code-Tests
O script foi testado nos arquivos de `code-tests/` e encontrou:

- **61 vulnerabilidades total**
- **16 HIGH** (alta severidade)
- **25 MEDIUM** (média severidade) 
- **20 LOW** (baixa severidade)

### Distribuição por Tipo
- **blacklist**: 23 ocorrências
- **hardcoded_sql_expressions**: 14 ocorrências
- **hashlib**: 11 ocorrências (uso de MD5/SHA1)
- **hardcoded_tmp_directory**: 4 ocorrências
- **subprocess_popen_with_shell_equals_true**: 4 ocorrências
- **hardcoded_password_string**: 2 ocorrências
- **set_bad_file_permissions**: 2 ocorrências
- **yaml_load**: 1 ocorrência

### Análise do Código Fonte
O script também foi testado no código fonte (`src/`) e encontrou:

- **9 vulnerabilidades total**
- **1 HIGH** (alta severidade)
- **8 LOW** (baixa severidade)

## Interpretação dos Resultados

### Níveis de Severidade
- **HIGH**: Requer atenção imediata, pode comprometer a segurança
- **MEDIUM**: Deve ser corrigido, representa risco moderado
- **LOW**: Deve ser revisado, risco baixo mas pode ser melhorado

### Níveis de Confiança
- **HIGH**: Muito provável que seja um problema real
- **MEDIUM**: Provavelmente um problema real
- **LOW**: Pode ser um falso positivo

## Integração com CI/CD

O script pode ser facilmente integrado em pipelines de CI/CD:

```bash
# Falha se vulnerabilidades HIGH forem encontradas
python src/scripts/run_bandit_script.py src/ -o results/security_check.csv
if grep -q "HIGH" results/security_check.csv; then
    echo "Vulnerabilidades de alta severidade encontradas!"
    exit 1
fi
```
