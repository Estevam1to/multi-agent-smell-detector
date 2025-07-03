# Como Testar os Agentes e Criar CSV para Comparação

Este guia explica como testar os agentes de análise estática e segurança, gerar CSV e comparar com as ferramentas tradicionais (Pylint/Bandit).

## Scripts Disponíveis

### 1. `test_agents.py` - Testa os agentes
Executa os agentes nos arquivos Python e gera CSV com os resultados.

### 2. `compare_agents_tools.py` - Compara agentes vs ferramentas
Compara os resultados dos agentes com Pylint/Bandit.

## Passo a Passo Completo

### Passo 1: Gerar Resultados com Ferramentas Tradicionais

```bash
# Análise estática com Pylint
python src/scripts/run_pylint_script.py code-tests/ -o results/pylint_results.csv

# Análise de segurança com Bandit  
python src/scripts/run_bandit_script.py code-tests/ -o results/bandit_results.csv
```

### Passo 2: Testar os Agentes

```bash
# Testar ambos os agentes
python src/scripts/test_agents.py code-tests/ \
    --static-csv results/agent_code_smells.csv \
    --security-csv results/agent_vulnerabilities.csv \
    --combined-json results/agent_combined.json

# Testar apenas o agente estático
python src/scripts/test_agents.py code-tests/ --agent static \
    --static-csv results/agent_static_only.csv

# Testar apenas o agente de segurança
python src/scripts/test_agents.py code-tests/ --agent security \
    --security-csv results/agent_security_only.csv
```

### Passo 3: Comparar Resultados

```bash
# Comparar análise estática (Agente vs Pylint)
python src/scripts/compare_agents_tools.py \
    --static-agent results/agent_code_smells.csv \
    --static-pylint results/pylint_results.csv \
    -o results/static_comparison.json

# Comparar análise de segurança (Agente vs Bandit)
python src/scripts/compare_agents_tools.py \
    --security-agent results/agent_vulnerabilities.csv \
    --security-bandit results/bandit_results.csv \
    -o results/security_comparison.json

# Comparar ambos
python src/scripts/compare_agents_tools.py \
    --static-agent results/agent_code_smells.csv \
    --static-pylint results/pylint_results.csv \
    --security-agent results/agent_vulnerabilities.csv \
    --security-bandit results/bandit_results.csv \
    -o results/full_comparison.json
```

## Estrutura dos CSV Gerados

### CSV dos Agentes
```csv
file,agent,type,description,risk,suggestion,code,line
code-tests/teste_1.py,static_analyzer,God Class,Class has too many responsibilities,Violates SRP,Break into smaller classes,class UserManager:,3
```

### CSV do Pylint
```csv
file,type,message_id,description,risk,line,column,symbol,obj
code-tests/teste_1.py,God Class,R0902,Too many instance attributes,Classes with too many responsibilities,3,0,too-many-instance-attributes,UserManager
```

### CSV do Bandit
```csv
file,type,test_id,description,severity,confidence,line,code
code-tests/teste_3.py,Hardcoded Password,B106,Possible hardcoded password,LOW,MEDIUM,15,password = "admin123"
```

## Exemplos de Análise

### Exemplo 1: Testar um arquivo específico
```bash
# Testar arquivo específico
python src/scripts/test_agents.py code-tests/teste_1.py \
    --static-csv results/teste1_agent.csv

# Comparar com Pylint
python src/scripts/run_pylint_script.py code-tests/teste_1.py \
    -o results/teste1_pylint.csv

python src/scripts/compare_agents_tools.py \
    --static-agent results/teste1_agent.csv \
    --static-pylint results/teste1_pylint.csv \
    -o results/teste1_comparison.json
```

### Exemplo 2: Análise completa do projeto
```bash
# 1. Gerar todos os resultados
python src/scripts/run_pylint_script.py src/ -o results/src_pylint.csv
python src/scripts/run_bandit_script.py src/ -o results/src_bandit.csv
python src/scripts/test_agents.py src/ \
    --static-csv results/src_agent_static.csv \
    --security-csv results/src_agent_security.csv

# 2. Comparar tudo
python src/scripts/compare_agents_tools.py \
    --static-agent results/src_agent_static.csv \
    --static-pylint results/src_pylint.csv \
    --security-agent results/src_agent_security.csv \
    --security-bandit results/src_bandit.csv \
    -o results/src_full_comparison.json
```

## Interpretando os Resultados

### Relatório de Comparação JSON
```json
{
  "static_analysis": {
    "summary": {
      "agent_total": 15,
      "pylint_total": 22,
      "difference": -7
    },
    "by_type": {
      "god_class": {"agent": 3, "pylint": 5},
      "long_method": {"agent": 2, "pylint": 2}
    }
  },
  "security_analysis": {
    "summary": {
      "agent_total": 8,
      "bandit_total": 61,
      "difference": -53
    }
  }
}
```

### Métricas de Avaliação

1. **Precisão**: Quantos problemas reais os agentes encontram
2. **Recall**: Quantos dos problemas totais os agentes detectam
3. **F1-Score**: Média harmônica entre precisão e recall

### Análise de Gaps

- **Agente encontra mais**: Possível sobre-detecção ou sensibilidade maior
- **Ferramenta encontra mais**: Possível sub-detecção ou gaps no agente
- **Tipos diferentes**: Agentes podem focar em aspectos diferentes

## Troubleshooting

### Problema: Agente não retorna JSON válido
```bash
# Verificar se a API key está configurada
echo $GOOGLE_API_KEY

# Testar com arquivo menor
python src/scripts/test_agents.py code-tests/teste_1.py --agent static
```

### Problema: Erro de importação dos agentes
```bash
# Verificar se as dependências estão instaladas
uv sync

# Testar importação manualmente
python -c "from src.agents.static_analizer_agent import static_agent"
```

### Problema: CSV vazio
- Verificar se os agentes estão retornando resultados válidos
- Verificar se os arquivos de entrada existem
- Conferir logs de erro durante a execução

## Próximos Passos

1. **Validação Manual**: Revisar manualmente alguns resultados para verificar qualidade
2. **Métricas**: Calcular precisão, recall e F1-score
3. **Otimização**: Ajustar prompts dos agentes baseado nos resultados
4. **Automação**: Integrar em pipeline de CI/CD
