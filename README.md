# Detecção e Revisão Automatizada de Code Smells e Security Smells com LLMs Multiagentes

Este projeto implementa agentes especializados para detecção e revisão automatizada de code smells e security smells em código Python utilizando Large Language Models (LLMs) multiagentes e ferramentas de análise estática. Os agentes podem detectar problemas de qualidade de código, vulnerabilidades de segurança e fornecer sugestões de melhoria.

## Visão Geral

O projeto consiste em dois agentes principais:

1. **Agente Analisador Estático**: Detecta code smells como God Classes, métodos longos, código morto e complexidade ciclomática.

2. **Agente de Segurança**: Identifica vulnerabilidades de segurança como Remote Code Execution (RCE), SQL injection e exposição de dados sensíveis.

Adicionalmente, existe um agente de workflow que coordena os dois agentes anteriores e gera relatórios combinados.

## Estrutura do Projeto

```
/multi-agent-smell-detector
├── README.md
├── pyproject.toml
├── docs/                 # 📚 Complete project documentation
│   ├── README.md         # Documentation index
│   ├── RESULTADOS_TCC.md # Main TCC results document
│   ├── DETALHAMENTO_TECNICO.md # Technical implementation details  
│   ├── ANALISE_ESTATISTICA.md # Statistical analysis
│   └── EXEMPLO_COMPLETO.md # Complete usage examples
├── src/
│   ├── agents/
│   │   ├── static_analizer_agent.py
│   │   ├── security_agent.py
│   │   └── workflow_agent.py
│   ├── scripts/
│   │   ├── run_bandit_script.py
│   │   ├── run_pylint_script.py
│   │   ├── test_agents.py
│   │   ├── compare_agents_tools.py
│   │   ├── generate_charts.py
│   │   └── final_comparison.py
│   ├── tools/
│   │   ├── analyzer_code_tool.py
│   │   └── bandit_tool.py
│   └── config/
│       └── settings.py
├── code-tests/           # Test files with intentional code smells
├── results/              # Analysis results and comparisons
│   ├── *.csv             # Generated CSV files
│   └── charts/           # Generated visualizations and reports
└── env sample            # Environment variables template
```

## Requisitos

- Python 3.10+
- Pylint 3.0+
- Bandit
- LangChain e dependências do Google Generative AI

## Instalação

```bash
# Instalar dependências
uv sync

# Ou usando pip
pip install -r requirements.txt
```

## Uso

### Início Rápido - Processo Completo
```bash
# 1. Análise com Bandit (vulnerabilidades)
python src/scripts/run_bandit_script.py code-tests/ -o results/bandit_results.csv

# 2. Análise com Pylint (code smells)
python src/scripts/run_pylint_script.py code-tests/ -o results/pylint_results.csv

# 3. Análise com Agentes IA
python src/scripts/test_agents.py code-tests/ --static-csv results/agent_static.csv --security-csv results/agent_security.csv

# 4. Comparação e gráficos
python src/scripts/compare_agents_tools.py
python src/scripts/generate_charts.py
```

### Uso dos Agentes Python
Você pode usar os agentes diretamente no seu código Python:

```python
# Exemplo de uso do Agente Analisador Estático
from src.agents.static_analizer_agent import static_agent

response = static_agent.invoke({
    "messages": [
        {"role": "user", "content": "seu_codigo_python_aqui"}
    ]
})
print(response["messages"][-1].content)
```

```python
# Exemplo de uso do Agente de Segurança
from src.agents.security_agent import security_agent

response = security_agent.invoke({
    "messages": [
        {"role": "user", "content": "seu_codigo_python_aqui"}
    ]
})
print(response["messages"][-1].content)
```

```python
# Exemplo de uso do Agente de Workflow
from src.agents.workflow_agent import app

response = app.invoke({
    "messages": [
        {"role": "user", "content": "seu_codigo_python_aqui"}
    ]
})
print(response)
```

## Tecnologias Utilizadas

- **LangGraph**: Framework para orquestração de agentes LLM
- **PydanticAI**: Framework para definição de agentes e suas interfaces
- **Pylint**: Ferramenta de análise estática para Python
- **Bandit**: Ferramenta de análise de segurança para Python
- **Gemini** e **Claude**: Modelos LLM utilizados pelos agentes

## Organização dos Resultados

Todos os resultados de análise são automaticamente salvos na pasta `results/`:
- Arquivos `*.csv`: Resultados das análises (Pylint, Bandit, Agentes)
- Pasta `charts/`: Visualizações e relatórios comparativos
- `comparison_report.json`: Relatório detalhado de comparação

## Exemplos de Saída

### Agente Analisador Estático

O agente de análise estática retorna um JSON com code smells detectados:

```json
{
    "code_smells": [
        {
            "type": "God Class",
            "description": "Classe com muitos atributos e responsabilidades",
            "risk": "Dificulta a manutenção e viola o princípio da responsabilidade única",
            "suggestion": "Dividir em múltiplas classes com responsabilidades específicas",
            "code": "class UserManager:",
            "line": 4
        }
    ]
}
```

### Agente de Segurança

O agente de segurança retorna um JSON com vulnerabilidades detectadas:

```json
{
    "vulnerabilities": [
        {
            "type": "Execução de Comando com Shell=True",
            "description": "Uso inseguro de subprocess com shell=True",
            "risk": "Pode permitir injeção de comandos do sistema se a entrada não for sanitizada",
            "suggestion": "Substituir por shell=False e passar argumentos como lista",
            "code": "result = subprocess.run(pylint_cmd, shell=True, capture_output=True, text=True)",
            "line": 35
        }
    ]
}
```

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

## 📚 Documentação

Este projeto inclui documentação abrangente para uso acadêmico e prático sobre "Detecção e Revisão Automatizada de Code Smells e Security Smells Utilizando LLMs Multiagentes":

- **[📋 Índice Completo da Documentação](docs/README.md)** - Comece aqui para navegação
- **[🎓 Resultados do TCC (RESULTADOS_TCC.md)](docs/RESULTADOS_TCC.md)** - Documento acadêmico principal com metodologia, resultados e conclusões
- **[⚙️ Detalhes Técnicos (DETALHAMENTO_TECNICO.md)](docs/DETALHAMENTO_TECNICO.md)** - Arquitetura de implementação e detalhes de código
- **[📊 Análise Estatística (ANALISE_ESTATISTICA.md)](docs/ANALISE_ESTATISTICA.md)** - Validação estatística e rigor científico
- **[📖 Exemplos Completos (EXEMPLO_COMPLETO.md)](docs/EXEMPLO_COMPLETO.md)** - Guia passo a passo de uso

### Resumo dos Principais Resultados
- **Pylint**: 22 code smells detectados
- **Bandit**: 61 vulnerabilidades detectadas  
- **Agente Estático IA**: 40 problemas detectados (82% mais que Pylint)
- **Agente Segurança IA**: 56 vulnerabilidades detectadas
- **Descoberta Principal**: Agentes de IA e ferramentas tradicionais são **complementares**, não substitutos
