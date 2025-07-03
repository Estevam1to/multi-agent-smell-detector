# Detecção e Revisão Automatizada de Code Smells e Security Smells Utilizando LLMs Multiagentes

## Resumo Executivo

Este documento apresenta os resultados de uma pesquisa sobre detecção e revisão automatizada de code smells e security smells utilizando Large Language Models (LLMs) multiagentes em comparação com ferramentas tradicionais de análise estática em código Python. O estudo analisou 10 arquivos de teste contendo diversos tipos de problemas de código, utilizando 4 abordagens diferentes: Pylint, Bandit, Agente Estático IA e Agente de Segurança IA.

## Metodologia

### 1. Conjunto de Dados
- **Arquivos analisados**: 10 arquivos Python (`teste_1.py` até `teste_10.py`)
- **Localização**: Pasta `code-tests/`
- **Características**: Arquivos contendo code smells e vulnerabilidades intencionalmente inseridas para teste

### 2. Ferramentas Utilizadas

#### 2.1 Ferramentas Tradicionais
- **Pylint**: Ferramenta de análise estática para detecção de code smells
- **Bandit**: Ferramenta especializada em detecção de vulnerabilidades de segurança

#### 2.2 Agentes de IA
- **Agente Estático**: LLM configurado para detectar code smells
- **Agente de Segurança**: LLM configurado para detectar vulnerabilidades de segurança

### 3. Processo de Análise

#### 3.1 Execução das Ferramentas
```bash
# 1. Análise com Bandit
python src/scripts/run_bandit_script.py code-tests/

# 2. Análise com Pylint
python src/scripts/run_pylint_script.py code-tests/

# 3. Análise com Agentes IA
python src/scripts/test_agents.py code-tests/

# 4. Comparação e geração de gráficos
python src/scripts/compare_agents_tools.py
python src/scripts/generate_charts.py
```

#### 3.2 Geração de Dados
Cada ferramenta gerou um arquivo CSV estruturado com os seguintes campos:
- **Arquivo**: Localização do problema
- **Tipo**: Categoria do problema detectado
- **Descrição**: Detalhamento do problema
- **Linha**: Localização específica no código
- **Severidade/Risco**: Nível de criticidade

## Resultados Quantitativos

### 1. Visão Geral dos Resultados

| Ferramenta | Total de Issues | Tipos Diferentes |
|------------|----------------|------------------|
| **Pylint** | 22 | 4 |
| **Bandit** | 61 | 8 |
| **Agente Estático** | 40 | 6 |
| **Agente Segurança** | 56 | 24 |

### 2. Análise Estática (Code Smells)

#### 2.1 Pylint - Distribuição por Tipo
```
Too Many Arguments: 9 (40.9%)
Too Many Branches: 6 (27.3%)
God Class: 5 (22.7%)
Long Method: 2 (9.1%)
```

#### 2.2 Agente Estático - Distribuição por Tipo
```
Long Method: 18 (45.0%)
God Class: 10 (25.0%)
Too Many Arguments: 7 (17.5%)
SQL Injection Vulnerability: 3 (7.5%)
Too Many Branches: 1 (2.5%)
Too Many Instance Attributes: 1 (2.5%)
```

#### 2.3 Comparação Análise Estática
- **Concordância em God Class**: Ambos detectaram este problema
- **Diferença em Long Method**: Agente detectou 9x mais (18 vs 2)
- **Diferença em Too Many Arguments**: Pylint detectou mais (9 vs 7)
- **Detecção Híbrida**: Agente também identificou vulnerabilidades de segurança

### 3. Análise de Segurança

#### 3.1 Bandit - Distribuição por Severidade
```
MEDIUM: 25 (41.0%)
LOW: 20 (32.8%)
HIGH: 16 (26.2%)
```

#### 3.2 Bandit - Distribuição por Tipo
```
blacklist: 23 (37.7%)
hardcoded_sql_expressions: 14 (23.0%)
hashlib: 11 (18.0%)
hardcoded_tmp_directory: 4 (6.6%)
subprocess_popen_with_shell_equals_true: 4 (6.6%)
outros: 5 (8.1%)
```

#### 3.3 Agente de Segurança - Distribuição por Tipo
```
SQL Injection: 15 (26.8%)
Path Traversal: 4 (7.1%)
Use of MD5 hash algorithm: 4 (7.1%)
Command Injection: 3 (5.4%)
Hardcoded credentials: 3 (5.4%)
outros: 27 (48.2%)
```

## Análise Qualitativa

### 1. Vantagens dos Agentes de IA

#### 1.1 Maior Diversidade de Detecção
- **24 tipos diferentes** de vulnerabilidades detectadas vs 8 do Bandit
- Capacidade de **detecção semântica** além de padrões sintáticos
- **Análise contextual** do código

#### 1.2 Explicações Detalhadas
```csv
"The class CryptoUtils has too many responsibilities. It handles random string generation, password hashing, data encryption/decryption, token generation/verification, file encryption/decryption, and downloading/verifying data. This violates the Single Responsibility Principle."
```

#### 1.3 Sugestões de Melhoria
```csv
"Break the class into multiple smaller classes, each with a single responsibility. For example, create separate classes for password hashing, data encryption, and token management."
```

### 2. Vantagens das Ferramentas Tradicionais

#### 2.1 Precisão e Consistência
- **Regras bem definidas** e testadas
- **Reprodutibilidade** garantida
- **Baixa taxa de falsos positivos**

#### 2.2 Performance
- **Velocidade** de execução superior
- **Menor consumo de recursos**
- **Escalabilidade** para grandes bases de código

#### 2.3 Integração
- **Ampla adoção** na indústria
- **Integração nativa** com IDEs
- **Pipelines de CI/CD** estabelecidos

## Descobertas Importantes

### 1. Complementaridade das Abordagens

#### 1.1 Detecção Híbrida do Agente Estático
O agente estático detectou **3 vulnerabilidades SQL Injection** mesmo sendo focado em code smells, demonstrando:
- **Capacidade de análise transversal**
- **Compreensão semântica** do código
- **Detecção de problemas relacionados**

#### 1.2 Sensibilidade Diferente
- **Long Method**: Agente detectou 18 vs Pylint 2
- **God Class**: Agente detectou 10 vs Pylint 5
- Indica **thresholds diferentes** e **critérios de avaliação** distintos

### 2. Padrões de Detecção

#### 2.1 Vulnerabilidades Comuns Detectadas
Ambas as ferramentas de segurança detectaram:
- **MD5/SHA1 usage**: Algoritmos fracos de hash
- **SQL Injection**: Expressões SQL hardcoded
- **Command Injection**: Execução insegura de comandos

#### 2.2 Diferenças na Categorização
- **Bandit**: Foco em padrões específicos (blacklist, hashlib)
- **Agente**: Categorização semântica (SQL Injection, Path Traversal)

## Implicações para a Prática

### 1. Estratégia Híbrida Recomendada

#### 1.1 Ferramentas Tradicionais para:
- **Validação inicial** e checks básicos
- **Pipelines automatizados** de CI/CD
- **Análise de performance** em grandes codebases

#### 1.2 Agentes de IA para:
- **Revisão de código detalhada**
- **Análise semântica complexa**
- **Treinamento e educação** de desenvolvedores

### 2. Configuração Otimizada

#### 2.1 Pipeline Sequencial
```
1. Pylint/Bandit → Detecção rápida de problemas óbvios
2. Agentes IA → Análise profunda e sugestões
3. Revisão humana → Validação final
```

#### 2.2 Thresholds Ajustados
- **Agente Estático**: Ajustar sensibilidade para Long Method
- **Agente Segurança**: Validar detecções específicas
- **Ferramentas**: Manter configuração padrão

## Limitações do Estudo

### 1. Escopo Limitado
- **10 arquivos** apenas
- **Ambiente controlado** com problemas intencionais
- **Ausência de validação manual** completa

### 2. Variabilidade dos LLMs
- **Dependência do modelo** específico usado
- **Variabilidade nas respostas** entre execuções
- **Necessidade de prompts otimizados**

### 3. Contexto Temporal
- **Versões específicas** das ferramentas
- **Evolução constante** dos LLMs
- **Necessidade de reavaliação** periódica

## Conclusões

### 1. Principais Achados

1. **Complementaridade**: Agentes de IA e ferramentas tradicionais são **complementares**, não substitutos
2. **Diversidade**: Agentes detectaram **3x mais tipos** de problemas de segurança
3. **Explicabilidade**: Agentes forneceram **contexto e sugestões** superiores
4. **Performance**: Ferramentas tradicionais mantêm **vantagem em velocidade**

### 2. Contribuições

1. **Framework de comparação** estruturado para análise de código
2. **Metodologia reproduzível** para avaliação de ferramentas
3. **Insights sobre complementaridade** de abordagens tradicionais e IA
4. **Base para desenvolvimento** de soluções híbridas

### 3. Trabalhos Futuros

1. **Validação em larga escala** com projetos reais
2. **Desenvolvimento de métricas** específicas para LLMs
3. **Otimização de prompts** para diferentes tipos de análise
4. **Integração nativa** de agentes em ferramentas existentes

## Anexos

### A. Estrutura dos Dados Gerados

#### A.1 Formato CSV Padrão
```csv
file,agent,type,description,risk,suggestion,code,line
```

#### A.2 Estrutura de Diretórios
```
results/
├── code_tests_bandit.csv        # Resultados Bandit
├── code_tests_pylint.csv        # Resultados Pylint  
├── code_tests_agent_static.csv  # Resultados Agente Estático
├── code_tests_agent_security.csv # Resultados Agente Segurança
└── charts/                      # Visualizações e relatórios
    ├── comparison_report.json
    ├── comparison_report.txt
    ├── static_analysis_comparison.png
    ├── security_analysis_comparison.png
    └── summary_dashboard.png
```

### B. Scripts Desenvolvidos

1. **`run_bandit_script.py`**: Automação da análise Bandit
2. **`run_pylint_script.py`**: Automação da análise Pylint
3. **`test_agents.py`**: Execução dos agentes de IA
4. **`compare_agents_tools.py`**: Comparação quantitativa
5. **`generate_charts.py`**: Geração de visualizações

### C. Gráficos Gerados

1. **Summary Dashboard**: Visão geral comparativa
2. **Static Analysis Comparison**: Comparação Pylint vs Agente Estático
3. **Security Analysis Comparison**: Comparação Bandit vs Agente Segurança
4. **Vulnerability Types**: Distribuição de tipos de vulnerabilidades

---

*Este documento foi gerado como parte da pesquisa de TCC sobre "Detecção e Revisão Automatizada de Code Smells e Security Smells Utilizando LLMs Multiagentes".*
