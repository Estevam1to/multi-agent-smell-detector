# Exemplo Completo: Como Testar os Agentes e Criar CSV para Comparação

Este é um exemplo prático completo de como usar todos os scripts para testar os agentes e comparar com as ferramentas tradicionais.

## Exemplo: Análise do arquivo teste_1.py

### 1. Gerar resultados com ferramentas tradicionais

```bash
# Análise estática com Pylint
python src/scripts/run_pylint_script.py code-tests/teste_1.py -o results/teste1_pylint.csv

# Análise de segurança com Bandit (se houver vulnerabilidades)
python src/scripts/run_bandit_script.py code-tests/teste_1.py -o results/teste1_bandit.csv
```

### 2. Testar os agentes

```bash
# Testar agente estático
python src/scripts/test_agents.py code-tests/teste_1.py --agent static \
    --static-csv results/teste1_agent_static.csv

# Testar agente de segurança  
python src/scripts/test_agents.py code-tests/teste_1.py --agent security \
    --security-csv results/teste1_agent_security.csv

# Testar ambos os agentes
python src/scripts/test_agents.py code-tests/teste_1.py \
    --static-csv results/teste1_agent_static.csv \
    --security-csv results/teste1_agent_security.csv \
    --combined-json results/teste1_agent_combined.json
```

### 3. Comparar resultados

```bash
# Comparar análise estática
python src/scripts/compare_agents_tools.py \
    --static-agent results/teste1_agent_static.csv \
    --static-pylint results/teste1_pylint.csv \
    -o results/teste1_static_comparison.json

# Comparar análise de segurança (se houver resultados)
python src/scripts/compare_agents_tools.py \
    --security-agent results/teste1_agent_security.csv \
    --security-bandit results/teste1_bandit.csv \
    -o results/teste1_security_comparison.json
```

## Resultados do Exemplo

### Pylint encontrou:
- 1 God Class (R0902)
- 3 Too Many Arguments (R0913)
- **Total: 4 issues**

### Agente Estático encontrou:
- 1 God Class
- 1 Long Method
- 1 Too Many Branches  
- **Total: 3 issues**

### Comparação:
- **God Class**: Ambos encontraram (✓)
- **Too Many Arguments**: Apenas Pylint encontrou (Gap do agente)
- **Long Method/Too Many Branches**: Apenas agente encontrou (Sensibilidade diferente)

## Exemplo: Análise de Todo o Diretório code-tests

```bash
# 1. Gerar todos os resultados
python src/scripts/run_pylint_script.py code-tests/ -o results/all_pylint.csv
python src/scripts/run_bandit_script.py code-tests/ -o results/all_bandit.csv
python src/scripts/test_agents.py code-tests/ \
    --static-csv results/all_agent_static.csv \
    --security-csv results/all_agent_security.csv \
    --combined-json results/all_agent_combined.json

# 2. Comparar tudo
python src/scripts/compare_agents_tools.py \
    --static-agent results/all_agent_static.csv \
    --static-pylint results/all_pylint.csv \
    --security-agent results/all_agent_security.csv \
    --security-bandit results/all_bandit.csv \
    -o results/all_comparison.json
```

## Scripts Utilizados

1. **`run_pylint_script.py`**: Gera CSV com code smells do Pylint
2. **`run_bandit_script.py`**: Gera CSV com vulnerabilidades do Bandit  
3. **`test_agents.py`**: Testa agentes e gera CSV
4. **`compare_agents_tools.py`**: Compara agentes vs ferramentas

## Estrutura dos Resultados

```
results/
├── teste1_pylint.csv           # Resultados Pylint
├── teste1_bandit.csv           # Resultados Bandit
├── teste1_agent_static.csv     # Resultados agente estático
├── teste1_agent_security.csv   # Resultados agente segurança
├── teste1_agent_combined.json  # Resultados combinados agentes
├── teste1_static_comparison.json    # Comparação estática
└── teste1_security_comparison.json  # Comparação segurança
```

## Interpretação dos Resultados

### CSV dos Agentes
```csv
file,agent,type,description,risk,suggestion,code,line
code-tests/teste_1.py,static_analyzer,God Class,Class has too many responsibilities,Violates SRP,Break into smaller classes,class UserManager:,3
```

### Relatório de Comparação
```json
{
  "static_analysis": {
    "summary": {
      "agent_total": 3,
      "pylint_total": 4, 
      "difference": -1
    },
    "by_type": {
      "god_class": {"agent": 1, "pylint": 1},
      "too_many_arguments": {"agent": 0, "pylint": 3}
    }
  }
}
```

## Próximos Passos

1. **Analisar gaps**: Por que o agente não detectou "Too Many Arguments"?
2. **Validar detecções únicas**: As detecções exclusivas do agente são válidas?
3. **Ajustar prompts**: Melhorar instruções dos agentes baseado nos resultados
4. **Métricas**: Calcular precisão, recall e F1-score com validação manual
