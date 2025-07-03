# Detalhamento Técnico: Detecção e Revisão Automatizada de Code Smells e Security Smells com LLMs Multiagentes

## Arquitetura do Sistema

### 1. Estrutura Geral

```
multi-agent-smell-detector/
├── src/
│   ├── agents/                  # Agentes de IA
│   │   ├── static_analizer_agent.py
│   │   ├── security_agent.py
│   │   └── workflow_agent.py
│   ├── tools/                   # Ferramentas auxiliares
│   │   ├── analyzer_code_tool.py
│   │   └── bandit_tool.py
│   ├── config/                  # Configurações
│   │   └── settings.py
│   └── scripts/                 # Scripts de automação
│       ├── run_bandit_script.py
│       ├── run_pylint_script.py
│       ├── test_agents.py
│       ├── compare_agents_tools.py
│       └── generate_charts.py
├── code-tests/                  # Arquivos de teste
└── results/                     # Resultados gerados
```

## Configuração dos Agentes de IA

### 1. Agente de Análise Estática

#### 1.1 Prompt System
```python
STATIC_ANALYZER_PROMPT = """
Você é um especialista em análise estática de código Python com foco em detectar code smells.
Analise o código fornecido e identifique problemas de qualidade como:

CODE SMELLS A DETECTAR:
1. God Class (classe com muitas responsabilidades)
2. Long Method (métodos muito longos)
3. Too Many Arguments (muitos parâmetros)
4. Too Many Branches (muitas condicionais)
5. Too Many Instance Attributes (muitos atributos)
6. Duplicate Code (código duplicado)
7. Dead Code (código não utilizado)
8. Feature Envy (inveja de funcionalidade)

CRITÉRIOS DE AVALIAÇÃO:
- God Class: > 7 métodos ou > 200 linhas
- Long Method: > 20 linhas
- Too Many Arguments: > 5 parâmetros
- Too Many Branches: > 10 condicionais
- Too Many Instance Attributes: > 7 atributos

Para cada problema encontrado, forneça:
- Tipo exato do code smell
- Descrição clara do problema
- Localização (linha)
- Nível de risco
- Sugestão de refatoração
"""
```

#### 1.2 Configuração Técnica
```python
class StaticAnalyzerAgent:
    def __init__(self):
        self.model = "gpt-4"
        self.temperature = 0.1  # Baixa para maior consistência
        self.max_tokens = 2000
        self.timeout = 30
```

### 2. Agente de Segurança

#### 2.1 Prompt System
```python
SECURITY_AGENT_PROMPT = """
Você é um especialista em segurança de aplicações Python.
Analise o código fornecido e identifique vulnerabilidades de segurança:

VULNERABILIDADES A DETECTAR:
1. SQL Injection
2. Command Injection
3. Path Traversal
4. XSS (Cross-Site Scripting)
5. Hardcoded Credentials
6. Weak Cryptography
7. Insecure Random
8. Sensitive Data Exposure
9. Input Validation Issues
10. Insecure Deserialization

CRITÉRIOS RIGOROSOS:
- Examine concatenação de strings em queries SQL
- Verifique uso de funções exec(), eval(), os.system()
- Analise manipulação de paths sem validação
- Identifique credenciais em texto plano
- Verifique algoritmos criptográficos fracos
- Examine geradores de números aleatórios

Para cada vulnerabilidade, forneça:
- Tipo específico da vulnerabilidade
- Impacto potencial
- Código afetado
- Recomendação de correção
"""
```

#### 2.2 Configuração de Severidade
```python
SEVERITY_MAPPING = {
    'SQL Injection': 'HIGH',
    'Command Injection': 'HIGH',
    'Path Traversal': 'MEDIUM',
    'Hardcoded Credentials': 'HIGH',
    'Weak Cryptography': 'MEDIUM',
    'XSS': 'MEDIUM',
    'Sensitive Data Exposure': 'MEDIUM'
}
```

## Scripts de Automação

### 1. Script Bandit (`run_bandit_script.py`)

#### 1.1 Funcionalidades Principais
```python
def run_bandit_analysis(target_path, output_file=None, format_type='csv'):
    """
    Executa análise Bandit e converte para CSV estruturado
    
    Args:
        target_path: Arquivo ou diretório para análise
        output_file: Arquivo de saída CSV
        format_type: Formato de saída (csv, json)
    """
    
    # Comando Bandit com flags específicas
    cmd = [
        'bandit', 
        '-f', 'json',           # Formato JSON para parsing
        '-ll',                  # Nível de confiança LOW
        '--skip', 'B101',       # Pula assert_used
        target_path
    ]
    
    # Processamento e conversão para CSV
    return convert_bandit_to_csv(bandit_output, output_file)
```

#### 1.2 Estrutura CSV Gerada
```csv
file,test_id,test_name,issue_severity,issue_confidence,issue_text,line_number,line_range,code,severity_description,confidence_description,more_info
```

### 2. Script Pylint (`run_pylint_script.py`)

#### 2.1 Configuração Específica
```python
def run_pylint_analysis(target_path, output_file=None):
    """
    Executa Pylint focado em code smells
    """
    
    # Filtros específicos para code smells
    PYLINT_FILTERS = [
        'R0902',  # too-many-instance-attributes
        'R0903',  # too-few-public-methods
        'R0904',  # too-many-public-methods
        'R0911',  # too-many-return-statements
        'R0912',  # too-many-branches
        'R0913',  # too-many-arguments
        'R0914',  # too-many-locals
        'R0915',  # too-many-statements
        'C0302',  # too-many-lines
    ]
    
    cmd = [
        'pylint',
        '--output-format=json',
        '--disable=all',
        f'--enable={",".join(PYLINT_FILTERS)}',
        target_path
    ]
```

### 3. Script dos Agentes (`test_agents.py`)

#### 3.1 Processamento Paralelo
```python
async def analyze_with_agents(file_path, agents=['static', 'security']):
    """
    Executa análise com múltiplos agentes em paralelo
    """
    tasks = []
    
    if 'static' in agents:
        tasks.append(static_agent.analyze(file_path))
    
    if 'security' in agents:
        tasks.append(security_agent.analyze(file_path))
    
    # Execução paralela
    results = await asyncio.gather(*tasks)
    
    return combine_results(results)
```

#### 3.2 Estrutura de Resposta dos Agentes
```python
AGENT_RESPONSE_SCHEMA = {
    "issues": [
        {
            "type": "God Class",
            "description": "Detailed description...",
            "risk": "High/Medium/Low",
            "suggestion": "Refactoring suggestion...",
            "code": "Affected code snippet...",
            "line": 42
        }
    ]
}
```

## Processo de Comparação

### 1. Script de Comparação (`compare_agents_tools.py`)

#### 1.1 Algoritmo de Matching
```python
def compare_static_analysis(agent_df, pylint_df):
    """
    Compara resultados entre agente e Pylint
    """
    
    # Normalização de tipos
    type_mapping = {
        'God Class': ['too-many-public-methods', 'too-many-instance-attributes'],
        'Long Method': ['too-many-statements', 'too-many-lines'],
        'Too Many Arguments': ['too-many-arguments'],
        'Too Many Branches': ['too-many-branches']
    }
    
    # Comparação por arquivo e linha
    matches = find_matches(agent_df, pylint_df, type_mapping)
    
    return {
        'matches': matches,
        'agent_only': find_agent_only(agent_df, pylint_df),
        'tool_only': find_tool_only(agent_df, pylint_df)
    }
```

### 2. Métricas Calculadas

#### 2.1 Métricas Quantitativas
```python
def calculate_metrics(comparison_result):
    """
    Calcula métricas de comparação
    """
    
    metrics = {
        'precision': matches / (matches + false_positives),
        'recall': matches / (matches + false_negatives),
        'f1_score': 2 * (precision * recall) / (precision + recall),
        'coverage': unique_issues_found / total_possible_issues
    }
    
    return metrics
```

## Geração de Visualizações

### 1. Script de Gráficos (`generate_charts.py`)

#### 1.1 Configuração dos Gráficos
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração global
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_comparison_charts(data):
    """
    Gera conjunto completo de visualizações
    """
    
    # 1. Dashboard geral
    create_summary_dashboard(data)
    
    # 2. Comparação estática
    create_static_comparison(data['static'])
    
    # 3. Comparação de segurança  
    create_security_comparison(data['security'])
    
    # 4. Distribuição de tipos
    create_type_distribution(data)
```

#### 1.2 Tipos de Gráficos Gerados

1. **Summary Dashboard**: Visão geral com 4 subplots
2. **Bar Charts**: Comparação quantitativa
3. **Pie Charts**: Distribuição por tipos
4. **Heatmaps**: Correlação entre ferramentas

## Configurações de Ambiente

### 1. Dependências (`pyproject.toml`)

```toml
[tool.poetry.dependencies]
python = "^3.10"
openai = "^1.0.0"
bandit = "^1.7.5"
pylint = "^3.0.0"
matplotlib = "^3.7.0"
seaborn = "^0.12.0"
pandas = "^2.0.0"
asyncio = "^3.4.3"
```

### 2. Variáveis de Ambiente

```bash
# Configuração da API OpenAI
export OPENAI_API_KEY="your-api-key"
export OPENAI_MODEL="gpt-4"

# Configurações dos agentes
export AGENT_TEMPERATURE="0.1"
export AGENT_MAX_TOKENS="2000"
export AGENT_TIMEOUT="30"
```

## Validação e Qualidade

### 1. Testes Unitários

```python
def test_agent_response_format():
    """Valida formato da resposta dos agentes"""
    response = static_agent.analyze("sample_code.py")
    assert 'issues' in response
    assert all(required_fields in issue for issue in response['issues'])

def test_csv_generation():
    """Valida geração correta de CSV"""
    csv_data = convert_agent_to_csv(agent_response)
    assert len(csv_data) > 0
    assert all(column in csv_data.columns for column in REQUIRED_COLUMNS)
```

### 2. Validação de Dados

```python
def validate_csv_structure(csv_file):
    """
    Valida estrutura dos arquivos CSV gerados
    """
    df = pd.read_csv(csv_file)
    
    required_columns = ['file', 'type', 'description', 'line']
    missing_columns = set(required_columns) - set(df.columns)
    
    if missing_columns:
        raise ValueError(f"Colunas faltantes: {missing_columns}")
    
    return True
```

## Otimizações Implementadas

### 1. Cache de Resultados

```python
import functools
import hashlib

@functools.lru_cache(maxsize=128)
def analyze_file_cached(file_content_hash, agent_type):
    """Cache de análises por hash do arquivo"""
    return agent.analyze(file_content)
```

### 2. Processamento Batch

```python
def process_files_batch(file_list, batch_size=5):
    """
    Processa arquivos em lotes para otimizar API calls
    """
    for i in range(0, len(file_list), batch_size):
        batch = file_list[i:i+batch_size]
        yield process_batch(batch)
```

### 3. Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    """Decorator para limitar chamadas à API"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(60/calls_per_minute)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## Métricas de Performance

### 1. Tempo de Execução

```
Bandit: ~2.3s para 10 arquivos
Pylint: ~4.1s para 10 arquivos  
Agente Estático: ~15.2s para 10 arquivos
Agente Segurança: ~18.7s para 10 arquivos
```

### 2. Uso de Recursos

```
Bandit: ~50MB RAM, 0.2 CPU cores
Pylint: ~80MB RAM, 0.3 CPU cores
Agentes: ~200MB RAM, 0.1 CPU cores (+ API latency)
```

### 3. Custos de API (GPT-4)

```
Custo médio por arquivo: $0.015
Total para 10 arquivos: $0.15
Tokens médios por análise: ~1,200 input + 800 output
```

## Lições Aprendidas

### 1. Desafios Técnicos

1. **Variabilidade de Respostas**: LLMs podem gerar respostas diferentes
2. **Parsing de Saída**: Necessário estruturação rigorosa das respostas
3. **Rate Limiting**: APIs têm limites que impactam performance
4. **Qualidade dos Prompts**: Crucial para resultados consistentes

### 2. Otimizações Futuras

1. **Fine-tuning**: Treinar modelos específicos para análise de código
2. **Cache Inteligente**: Usar embeddings para detectar código similar
3. **Processamento Incremental**: Analisar apenas mudanças no código
4. **Ensemble Methods**: Combinar múltiplos agentes para maior precisão

---

*Este documento técnico complementa o RESULTADOS_TCC.md com detalhes de implementação e configuração do sistema de detecção e revisão automatizada de code smells e security smells utilizando LLMs multiagentes.*
