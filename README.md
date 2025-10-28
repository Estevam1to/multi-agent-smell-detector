# Multi-Agent Code Smell Detector

Sistema de detecção de code smells em Python usando múltiplos agentes especializados baseados em LLM.

## 📚 Sobre o Projeto

Trabalho de Conclusão de Curso (TCC) que implementa um sistema multi-agente para detecção automática de 11 tipos de code smells em código Python, seguindo as definições acadêmicas de:

- **Martin Fowler** (1999, 2018) - Refactoring: Improving the Design of Existing Code
- **Robert C. Martin** (2008) - Clean Code: A Handbook of Agile Software Craftsmanship
- **Thomas McCabe** (1976) - A complexity measure
- **PEP 8** - Style Guide for Python Code
- **CWE-478** - Common Weakness Enumeration (MITRE)

### 🎯 Objetivo

Comparar a eficácia de um sistema baseado em LLM multi-agente com ferramentas tradicionais de análise estática.

## 🏗️ Arquitetura

### Sistema Multi-Agente

```
┌─────────────────────────────────────────────────────────────┐
│                     API FastAPI                              │
│                   (Endpoint /analyze)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Supervisor Agent                            │
│         (Coordena execução paralela)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ├─────────────────────────────────────┐
                       │                                     │
        ┌──────────────▼────────┐              ┌────────────▼──────────┐
        │  Agentes Complexidade │              │  Agentes Estrutura    │
        ├───────────────────────┤              ├───────────────────────┤
        │ • Long Method         │              │ • Long Parameter List │
        │ • Complex Method      │              │ • Long Message Chain  │
        │ • Complex Conditional │              └───────────────────────┘
        └───────────────────────┘
                       │
        ┌──────────────▼────────┐              ┌────────────▼──────────┐
        │  Agentes Nomenclatura │              │  Agentes Statements   │
        ├───────────────────────┤              ├───────────────────────┤
        │ • Long Identifier     │              │ • Long Statement      │
        │ • Magic Number        │              │ • Empty Catch Block   │
        └───────────────────────┘              │ • Missing Default     │
                                               │ • Long Lambda Function│
                                               └───────────────────────┘
```

### 🤖 Agentes Implementados (11 total)

| # | Smell | Categoria | Threshold | Fonte |
|---|-------|-----------|-----------|-------|
| 1 | Long Method | Complexidade | > 67 linhas | Fowler (1999) |
| 2 | Long Parameter List | Estrutura | > 4 parâmetros | Fowler (1999) |
| 3 | Long Statement | Statements | > 80 caracteres | PEP 8 |
| 4 | Long Identifier | Nomenclatura | > 20 caracteres | Martin (2008) |
| 5 | Empty Catch Block | Statements | Bloco except vazio | Martin (2008) |
| 6 | Complex Method | Complexidade | CC > 7 | McCabe (1976) |
| 7 | Complex Conditional | Complexidade | > 2 operadores lógicos | Fowler (2018) |
| 8 | Missing Default | Statements | match-case sem default | CWE-478 |
| 9 | Long Lambda Function | Statements | > 80 caracteres | Chen et al. (2016) |
| 10 | Long Message Chain | Estrutura | > 2 métodos encadeados | Fowler (1999) |
| 11 | Magic Number | Nomenclatura | Literais sem constante | Fowler/Martin |

## 🚀 Instalação e Uso

### Pré-requisitos

- Python 3.12+
- Poetry ou uv
- Chave API da Anthropic

### Instalação

```bash
git clone <url-do-repositorio>
cd multi-agent-smell-detector

uv sync
```

### Configuração

Crie um arquivo `.env` na raiz:

```env
ANTHROPIC_API_KEY=sua_chave_api_aqui
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### Executando a API

```bash
source .venv/bin/activate
python src/app.py
```

A API estará disponível em `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

## 📡 Uso da API

### Endpoint: POST /api/analyze

**Parâmetros:**
- `python_code` (string, obrigatório): Código Python a ser analisado
- `file_path` (string, opcional): Caminho do arquivo
- `project_name` (string, opcional): Nome do projeto
- `use_structured_output` (bool, opcional): Usa supervisor V2 com structured output

**Resposta:**
- `total_smells_detected` (int): Total de code smells encontrados
- `agents_executed` (int): Número de agentes executados (11)
- `code_smells` (list): Lista de code smells detectados

## 📊 Análise em Batch

Para analisar múltiplos arquivos e comparar com outras ferramentas:

```bash
# Analisa todos arquivos .py de uma pasta
python scripts/batch_analyze.py /caminho/pasta -o results.json -p MeuProjeto

# Compara com resultados de outra ferramenta
python scripts/compare_results.py results.json other_tool.json
```

Ver `scripts/README.md` para mais detalhes.

## 📊 Estrutura do Projeto

```
multi-agent-smell-detector/
│
├── src/
│   ├── agents/
│   │   ├── prompts/                      # Prompts para cada agente
│   │   ├── specialized/                  # Agentes organizados por categoria
│   │   │   ├── complexity/
│   │   │   ├── structure/
│   │   │   ├── naming/
│   │   │   └── statements/
│   │   └── supervisor/                   # Supervisor que coordena agentes
│   │
│   ├── schemas/                          # Schemas Pydantic
│   │   ├── state.py
│   │   └── agent_response.py
│   │
│   ├── utils/                            # Utilitários
│   │   └── code_parser.py                # Parser de código Python
│   │
│   ├── routers/                          # Endpoints da API
│   ├── config/                           # Configurações
│   └── app.py                            # Aplicação FastAPI
│
├── scripts/                              # Scripts de análise
│   ├── batch_analyze.py
│   ├── compare_results.py
│   └── README.md
│
├── .env
├── pyproject.toml
└── README.md
```

## 🔬 Metodologia de Pesquisa (TCC)

### 1. Fundamentação Teórica

- **Code Smells**: Conceito introduzido por Fowler (1999)
- **Clean Code**: Princípios de Martin (2008)
- **Análise Estática**: Métricas objetivas (McCabe, PEP 8)
- **LLM Multi-Agente**: Arquitetura de agentes especializados

### 2. Hipótese

Sistemas baseados em LLM podem detectar code smells com acurácia comparável ou superior a ferramentas tradicionais de análise estática, oferecendo:

- Maior contexto semântico
- Explicações detalhadas
- Capacidade de detectar smells complexos que exigem compreensão de domínio

### 3. Metodologia de Avaliação

- Análise comparativa com ferramentas de análise estática
- Cálculo de métricas: Precision, Recall, F1-Score
- Avaliação qualitativa das explicações geradas

### 4. Contribuições Esperadas

- Framework multi-agente para detecção de code smells
- Comparação empírica LLM vs Análise Estática
- Dataset de exemplos de code smells

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework web para API REST
- **LangGraph**: Orquestração de agentes LLM
- **LangChain**: Integração com LLMs
- **Anthropic Claude**: Modelo LLM (Sonnet 4.5)
- **Pydantic**: Validação de dados
- **Python 3.12**: Linguagem base

## 📖 Referências Bibliográficas

1. **Fowler, M.** (1999). *Refactoring: Improving the Design of Existing Code*. Addison-Wesley Professional.
2. **Fowler, M.** (2018). *Refactoring: Improving the Design of Existing Code* (2nd Edition). Addison-Wesley Professional.
3. **Martin, R. C.** (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall.
4. **McCabe, T.** (1976). "A complexity measure". *IEEE Transactions on Software Engineering*, SE-2(4), pp. 308-320.
5. **Van Rossum, G., Warsaw, B., & Coghlan, N.** PEP 8 - Style Guide for Python Code.
6. **Chen et al.** (2016). "Detecting code smells in python programs". *International Conference on Software Analysis, Testing and Evolution (SATE)*.
7. **MITRE Corporation.** CWE-478: Missing Default Case in Multiple Condition Expression.

## 👨‍💻 Autor

**Estevam** - Trabalho de Conclusão de Curso (TCC)
