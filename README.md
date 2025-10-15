# Multi-Agent Code Smell Detector

Sistema de detecção de code smells usando múltiplos agentes especializados baseados em LangGraph e Anthropic Claude.

## Agentes Implementados

### 1. Long Method Agent

**Baseado em**: Martin Fowler - "Refactoring: Improving the Design of Existing Code" (1999), Capítulo 3, página 64.

**Critérios de Detecção**:
- **ALTA SEVERIDADE**: Métodos com > 50 linhas de código
- **MÉDIA SEVERIDADE**: Métodos com 30-50 linhas de código  
- **BAIXA SEVERIDADE**: Métodos com 20-30 linhas de código

**Arquivo**: `src/agents/long_method_agent.py`
**Exemplo**: `examples/long_method_examples.py`

### 2. Long Parameter List Agent

**Baseado em**: Martin Fowler - "Refactoring: Improving the Design of Existing Code" (1999), Capítulo 3, página 65.

**Critérios de Detecção**:
- **ALTA SEVERIDADE**: Métodos com > 5 parâmetros
- **MÉDIA SEVERIDADE**: Métodos com 4-5 parâmetros
- **BAIXA SEVERIDADE**: Métodos com 3-4 parâmetros (contexto-dependente)

**Arquivo**: `src/agents/long_parameter_list_agent.py`
**Exemplo**: `examples/long_parameter_list_examples.py`

## Arquitetura

### Tecnologias Utilizadas

- **LangGraph**: Framework para construção de agentes com fluxos complexos
- **Anthropic Claude**: Modelo de linguagem para análise de código
- **FastAPI**: API REST para exposição dos serviços
- **Pydantic**: Validação e serialização de dados

### Estrutura do Projeto

```
src/
├── agents/                     # Agentes especializados
│   ├── __init__.py
│   ├── long_method_agent.py
│   └── long_parameter_list_agent.py
├── config/                     # Configurações
│   ├── __init__.py
│   ├── logs.py
│   └── settings.py
├── routers/                    # Endpoints da API
│   ├── __init__.py
│   └── analysis.py
├── schemas/                    # Modelos de dados
│   ├── __init__.py
│   └── requests.py
└── app.py                      # Aplicação principal

examples/                       # Exemplos para teste
├── long_method_examples.py
└── long_parameter_list_examples.py
```

## Como Usar

### 1. Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
ANTHROPIC_API_KEY=sua_chave_anthropic_aqui
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

### 2. Instalação das Dependências

```bash
pip install fastapi langchain-anthropic langgraph pydantic uvicorn
```

### 3. Executar a API

```bash
cd src
python app.py
```

A API estará disponível em `http://localhost:8000`

### 4. Endpoints Disponíveis

#### POST `/api/v1/analyze`

Analisa código Python em busca de code smells.

**Request Body**:
```json
{
    "code": "def long_method():\n    # ... código muito longo ...",
    "file_name": "exemplo.py"
}
```

**Response**:
```json
{
    "success": true,
    "message": "Análise concluída. 2 code smell(s) detectado(s) por 2/2 agente(s).",
    "results": [
        {
            "agent_name": "LongMethodAgent",
            "status": "sucesso",
            "code_smells": [
                {
                    "type": "LONG_METHOD",
                    "severity": "ALTA",
                    "method_name": "very_long_method",
                    "lines_of_code": 65,
                    "line_start": 10,
                    "line_end": 75,
                    "description": "Método excessivamente longo...",
                    "impact": "Dificulta compreensão...",
                    "refactoring_suggestions": [...]
                }
            ]
        }
    ],
    "summary": {
        "total_code_smells": 2,
        "agents_executados": 2,
        "agents_com_sucesso": 2
    }
}
```

#### GET `/api/v1/health`

Verifica o status de saúde da API.

## Exemplos de Uso

### Testando o Long Method Agent

```python
# Use o código em examples/long_method_examples.py
with open('examples/long_method_examples.py', 'r') as f:
    code = f.read()

# POST para /api/v1/analyze
{
    "code": code,
    "file_name": "long_method_examples.py"
}
```

### Testando o Long Parameter List Agent

```python
# Use o código em examples/long_parameter_list_examples.py
with open('examples/long_parameter_list_examples.py', 'r') as f:
    code = f.read()

# POST para /api/v1/analyze
{
    "code": code,
    "file_name": "long_parameter_list_examples.py"
}
```

## Filosofia dos Agentes

### Long Method Agent

Baseado na filosofia de Martin Fowler: "The programs that live best and longest are those with short methods."

O agente detecta métodos que violam o princípio da responsabilidade única e sugere refatorações como:
- Extract Method
- Replace Temp with Query
- Decompose Conditional

### Long Parameter List Agent

Baseado na observação de Fowler sobre a evolução da programação orientada a objetos: "Com objetos você não precisa passar tudo que o método precisa; você passa apenas objetos suficientes para que o método possa obter o que precisa."

O agente identifica padrões problemáticos como:
- Data Clumps (dados que sempre andam juntos)
- Primitive Obsession (uso excessivo de tipos primitivos)
- Flag Arguments (parâmetros booleanos que controlam comportamento)

## Extensibilidade

Para adicionar novos agentes:

1. Crie um novo arquivo em `src/agents/novo_agent.py`
2. Implemente as funções `create_novo_agent()` e `novo_agent_analyze()`
3. Adicione o agente ao `__init__.py` dos agentes
4. Integre no router `src/routers/analysis.py`
5. Crie exemplos em `examples/novo_agent_examples.py`

## Referências

- Fowler, M. (1999). "Refactoring: Improving the Design of Existing Code". Addison-Wesley.
- LangGraph Documentation: https://langchain-ai.github.io/langgraph/
- Anthropic Claude API: https://docs.anthropic.com/
