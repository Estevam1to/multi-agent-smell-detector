# Multi-Agent Code Smell Detector

Sistema de detecção de code smells em Python usando múltiplos agentes especializados baseados em LLM.

## 📚 Sobre o Projeto

Trabalho de Conclusão de Curso (TCC) que implementa um sistema multi-agente para detecção automática de 11 tipos de code smells em código Python, seguindo as definições acadêmicas de renomados autores da Engenharia de Software.

### 🎯 Objetivo

Desenvolver um sistema baseado em LLM multi-agente capaz de detectar code smells em código Python com alta precisão, combinando análise estática e inteligência artificial.

## 🏗️ Arquitetura do Sistema

### Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                        API FastAPI                               │
│                    (POST /api/analyze)                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CodeSmellSupervisor                            │
│  • Coordena 11 agentes (paralelo ou sequencial)                 │
│  • Usa LLM (DeepSeek/GPT-4o-mini) com structured output         │
│  • Enriquece detecções com metadados (AST)                      │
│  • Filtra falsos positivos                                       │
│  • Limites: 500 linhas, 50KB por arquivo                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Complexidade │    │  Estrutura   │    │ Nomenclatura │
├──────────────┤    ├──────────────┤    ├──────────────┤
│ Long Method  │    │ Long Param   │    │ Long ID      │
│ Complex Meth │    │ Message Chain│    │ Magic Number │
│ Complex Cond │    └──────────────┘    └──────────────┘
└──────────────┘             │
                             ▼
                    ┌──────────────┐
                    │  Statements  │
                    ├──────────────┤
                    │ Long Stmt    │
                    │ Empty Catch  │
                    │ Missing Def  │
                    │ Long Lambda  │
                    └──────────────┘
```

### Fluxo de Execução

1. **Request** → API recebe código Python
2. **Validação** → Verifica tamanho (max 500 linhas, 50KB)
3. **Supervisor** → Coordena execução dos 11 agentes
4. **LLM** → Cada agente chama LLM com structured output (prompt + schema)
5. **Enrichment** → Adiciona metadados (Project, Package, Module, Line)
6. **Validação** → Filtra falsos positivos (ex: Long Identifier ≤ 20 chars)
7. **Response** → Retorna JSON com detecções

### ⚙️ Configurações

- **Modelo**: DeepSeek Chat V3.1 ou GPT-4o-mini (via OpenRouter)
- **Temperatura**: 0 (determinístico)
- **Modo**: Paralelo (11 requests simultâneos) ou Sequencial (delay 0.3s)
- **Limites**: 500 linhas, 50KB por arquivo
- **Validação**: Filtra falsos positivos automaticamente

## 🤖 Code Smells Detectados

### Tabela de Thresholds

| # | Code Smell | Categoria | Threshold | Descrição |
|---|------------|-----------|-----------|----------|
| 1 | **Long Method** | Complexidade | > 67 linhas | Métodos com mais de 67 linhas |
| 2 | **Complex Method** | Complexidade | CC > 7 | Complexidade Ciclomática maior que 7 |
| 3 | **Complex Conditional** | Complexidade | > 2 operadores | Mais de 2 operadores lógicos (and/or) |
| 4 | **Long Parameter List** | Estrutura | > 4 parâmetros | Funções com mais de 4 parâmetros |
| 5 | **Long Message Chain** | Estrutura | > 2 métodos | Mais de 2 métodos encadeados |
| 6 | **Long Statement** | Statements | > 120 caracteres | Linhas com mais de 120 caracteres |
| 7 | **Long Identifier** | Nomenclatura | > 20 caracteres | Identificadores com mais de 20 caracteres |
| 8 | **Magic Number** | Nomenclatura | Literais (exceto 0,1,-1) | Números literais sem constante nomeada |
| 9 | **Empty Catch Block** | Statements | Bloco vazio | Blocos except vazios ou apenas com pass |
| 10 | **Missing Default** | Statements | Sem case _ | match-case sem caso padrão |
| 11 | **Long Lambda** | Statements | > 80 caracteres | Lambdas com mais de 80 caracteres |

### Referências Bibliográficas

| Code Smell | Referência | Localização |
|------------|------------|-------------|
| Long Method | Fowler (1999) | Cap. 3, p. 76 |
| Complex Method | McCabe (1976) | IEEE Trans. SE, p. 308 |
| Complex Conditional | Fowler (2018) | Cap. 10, p. 260 |
| Long Parameter List | Fowler (1999) | Cap. 3, p. 78 |
| Long Message Chain | Fowler (1999) | Cap. 3, p. 84 |
| Long Statement | PEP 8 | Seção "Maximum Line Length" |
| Long Identifier | Martin (2008) | Cap. 2, p. 18-25 |
| Magic Number | Fowler (1999) + Martin (2008) | Cap. 3, p. 219 / Cap. 17 |
| Empty Catch Block | Martin (2008) | Cap. 7, p. 106 |
| Missing Default | CWE-478 (MITRE) | Common Weakness Enumeration |
| Long Lambda | Chen et al. (2016) | SATE Conference, p. 18 |

### Detalhamento por Categoria

#### 🔴 Complexidade (3 smells)
- **Long Method**: Métodos muito longos são difíceis de entender e manter
- **Complex Method**: Alta complexidade ciclomática indica muitos caminhos de execução
- **Complex Conditional**: Condicionais com muitos operadores lógicos são difíceis de ler

#### 🔵 Estrutura (2 smells)
- **Long Parameter List**: Muitos parâmetros indicam responsabilidades excessivas
- **Long Message Chain**: Encadeamento excessivo viola Lei de Demeter

#### 🟢 Nomenclatura (2 smells)
- **Long Identifier**: Nomes muito longos prejudicam legibilidade
- **Magic Number**: Literais numéricos sem significado explícito

#### 🟡 Statements (4 smells)
- **Long Statement**: Linhas muito longas dificultam leitura
- **Empty Catch Block**: Exceções silenciadas escondem erros
- **Missing Default**: Switch/match sem caso padrão pode causar bugs
- **Long Lambda Function**: Lambdas complexas devem ser funções nomeadas

## 🚀 Instalação e Uso

### Pré-requisitos

- Python 3.12+
- uv ou Poetry
- Chave API da OpenAI (GPT-4o-mini) via OpenRouter

### Instalação

```bash
git clone <url-do-repositorio>
cd multi-agent-smell-detector
uv sync
```

### Configuração

Crie um arquivo `.env` na raiz:

```env
OPENROUTER_API_KEY=sua_chave_api_aqui
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_API_MODEL=openai/gpt-4o-mini
```

### Executando a API

```bash
python src/app.py
```

A API estará disponível em `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

## 📡 Uso da API

### Endpoint: POST /api/analyze

**Request:**
```json
{
  "python_code": "def long_function_name_that_exceeds_twenty_chars():\n    pass",
  "file_path": "example.py",
  "project_name": "MyProject"
}
```

**Response:**
```json
{
  "total_smells_detected": 1,
  "agents_executed": 11,
  "code_smells": [
    {
      "Project": "MyProject",
      "Package": "example",
      "Module": "example",
      "Class": "",
      "Smell": "Long identifier",
      "Method": "long_function_name_that_exceeds_twenty_chars",
      "Line no": "1",
      "File": "example.py",
      "Description": "Identifier 'long_function_name_that_exceeds_twenty_chars' has 45 characters (threshold: 20). Consider shortening.",
      "identifier_name": "long_function_name_that_exceeds_twenty_chars",
      "length": 45,
      "threshold": 20
    }
  ]
}
```

## 📊 Análise em Batch

```bash
# Analisa todos arquivos .py de uma pasta
python scripts/batch_analyze.py /caminho/pasta -o results.json -p MeuProjeto

# Compara com resultados de outra ferramenta
python scripts/compare_results.py results.json other_tool.json
```

## 📊 Estrutura do Projeto

```
multi-agent-smell-detector/
├── src/
│   ├── api/                    # API FastAPI
│   │   ├── app.py              # Aplicação principal
│   │   ├── routes/             # Endpoints
│   │   └── models/             # Request/Response
│   │
│   ├── core/
│   │   ├── supervisor/         # Coordenador
│   │   │   ├── supervisor.py   # Lógica principal
│   │   │   ├── agent_config.py # Config dos 11 agentes
│   │   │   └── enricher.py     # Enriquecimento + validação
│   │   │
│   │   ├── prompts/            # 11 prompts especializados
│   │   ├── schemas/            # Schemas Pydantic
│   │   └── utils/              # Parser AST
│   │
│   └── config/                 # Configurações
│
├── scripts/                    # Scripts de análise
│   ├── batch_analyze.py        # Análise em batch
│   └── compare_results.py
│
├── examples/                             # Exemplos de código
├── results/                              # Resultados de análises
├── .env                                  # Variáveis de ambiente
└── pyproject.toml                        # Dependências
```

## 🛠️ Tecnologias

- **FastAPI**: API REST
- **LangChain**: Integração com LLMs
- **DeepSeek Chat V3.1 / GPT-4o-mini**: Modelos LLM via OpenRouter
- **Pydantic**: Validação e structured output
- **Python AST**: Parser de código
- **Python 3.12+**: Linguagem base

## 📖 Referências Bibliográficas

1. **Fowler, M.** (1999). *Refactoring: Improving the Design of Existing Code*. Addison-Wesley Professional. ISBN: 0-201-48567-2
2. **Fowler, M.** (2018). *Refactoring: Improving the Design of Existing Code* (2nd Edition). Addison-Wesley Professional. ISBN: 978-0134757599
3. **Martin, R. C.** (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. ISBN: 978-0132350884
4. **McCabe, T. J.** (1976). "A Complexity Measure". *IEEE Transactions on Software Engineering*, Vol. SE-2, No. 4, pp. 308-320. DOI: 10.1109/TSE.1976.233837
5. **Van Rossum, G., Warsaw, B., & Coghlan, N.** (2001). *PEP 8 – Style Guide for Python Code*. Python Enhancement Proposals. https://peps.python.org/pep-0008/
6. **Chen, Z., Chen, L., Ma, W., & Zhou, B.** (2016). "Detecting Code Smells in Python Programs". *International Conference on Software Analysis, Testing and Evolution (SATE)*, pp. 18-23. DOI: 10.1109/SATE.2016.10
7. **MITRE Corporation.** (2006). *CWE-478: Missing Default Case in Multiple Condition Expression*. Common Weakness Enumeration. https://cwe.mitre.org/data/definitions/478.html

## 👨💻 Autor

**Estevam** - Trabalho de Conclusão de Curso (TCC)  
Engenharia de Software - 2024

## 📄 Licença

Este projeto é parte de um Trabalho de Conclusão de Curso (TCC) acadêmico.
