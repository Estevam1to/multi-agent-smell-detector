# Multi-Agent Code Smell Detector

Sistema de detecção de code smells em Python usando **múltiplos agentes especializados** baseados em LLM (Large Language Models).

## 📚 Sobre o Projeto

Este projeto é um **Trabalho de Conclusão de Curso (TCC)** que implementa um sistema multi-agente para detecção automática de 11 tipos de code smells em código Python, seguindo as definições acadêmicas de:

- **Martin Fowler** (1999, 2018) - Refactoring: Improving the Design of Existing Code
- **Robert C. Martin** (2008) - Clean Code: A Handbook of Agile Software Craftsmanship
- **Thomas McCabe** (1976) - A complexity measure
- **PEP 8** - Style Guide for Python Code
- **CWE-478** - Common Weakness Enumeration (MITRE)

### 🎯 Objetivo

Comparar a eficácia de um sistema baseado em **LLM multi-agente** com ferramentas tradicionais de análise estática, especificamente a ferramenta **DPy da Designite**.

---

## 🏗️ Arquitetura

### Sistema Multi-Agente

O sistema utiliza uma arquitetura de **supervisor + agentes especializados**:

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

---

## 🚀 Instalação e Uso

### Pré-requisitos

- Python 3.12+
- Poetry ou uv (gerenciador de pacotes)
- Chave API da Anthropic

### 1. Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd multi-agent-smell-detector

# Instale as dependências
uv sync
# ou
poetry install
```

### 2. Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
ANTHROPIC_API_KEY=sua_chave_api_aqui
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### 3. Executando a API

```bash
# Ative o ambiente virtual
source .venv/bin/activate

# Inicie o servidor
python src/app.py
```

A API estará disponível em `http://localhost:8000`

### 4. Documentação da API

Acesse `http://localhost:8000/docs` para visualizar a documentação interativa (Swagger UI).

---

## 📡 Uso da API

### Endpoint: POST /api/analyze

Analisa código Python para detectar code smells usando múltiplos agentes especializados.

**Parâmetros:**
- `python_code` (string, obrigatório): Código Python a ser analisado
- `file_path` (string, opcional): Caminho do arquivo
- `output_format` (string, opcional): Formato de saída ("default" ou "structured")
- `project_name` (string, opcional): Nome do projeto

**Resposta:**
- `total_smells_detected` (int): Total de code smells encontrados
- `agents_executed` (int): Número de agentes executados
- `code_smells` (list): Lista de code smells detectados
- `output_format` (string): Formato da resposta

---

## 🧪 Testes

### Sistema de Avaliação: LLM as a Judge

O projeto implementa um sistema inovador de **LLM as a Judge** para avaliar automaticamente a qualidade das detecções.

#### Executando os Testes

```bash
# Testes com LLM as a Judge
python tests/test_agents.py
```

#### Métricas Calculadas

- **Accuracy**: Taxa de acertos geral
- **Precision**: Precisão (VP / VP + FP)
- **Recall**: Revocação (VP / VP + FN)
- **F1-Score**: Média harmônica de precision e recall
- **Confusion Matrix**: TP, TN, FP, FN


---

## 📊 Estrutura do Projeto

```
multi-agent-smell-detector/
│
├── src/
│   ├── agents/                           # Agentes especializados
│   │   ├── prompts/                      # Prompts para cada agente
│   │   │   ├── long_method_prompt.py
│   │   │   ├── complex_method_prompt.py
│   │   │   └── ... (11 prompts)
│   │   │
│   │   ├── specialized/                  # Agentes organizados por categoria
│   │   │   ├── complexity/               # Long Method, Complex Method, etc.
│   │   │   ├── structure/                # Long Parameter List, Message Chain
│   │   │   ├── naming/                   # Long Identifier, Magic Number
│   │   │   └── statements/               # Long Statement, Empty Catch, etc.
│   │   │
│   │   └── supervisor/                   # Supervisor que coordena agentes
│   │       └── supervisor_agent.py
│   │
│   ├── routers/                          # Endpoints da API
│   │   └── analysis.py
│   │
│   ├── schemas/                          # Schemas Pydantic
│   │   └── state.py
│   │
│   ├── utils/                            # Utilitários
│   │   ├── code_parser.py                # Parser de código Python
│   │   └── structured_formatter.py       # Formatador para saída estruturada
│   │
│   ├── config/                           # Configurações
│   │   ├── settings.py
│   │   └── logs.py
│   │
│   └── app.py                            # Aplicação FastAPI
│
├── tests/                                # Testes e avaliação
│   ├── test_cases/                       # Casos de teste
│   │   └── smell_examples.py             # 12 exemplos de code smells
│   │
│   ├── llm_judge.py                      # LLM as a Judge
│   └── test_agents.py                    # Executa testes
│
├── .env                                  # Variáveis de ambiente
├── pyproject.toml                        # Dependências
└── README.md                             # Este arquivo
```

---

## 🔬 Metodologia de Pesquisa (TCC)

### 1. Fundamentação Teórica

O projeto baseia-se em:

- **Code Smells**: Conceito introduzido por Fowler (1999)
- **Clean Code**: Princípios de Martin (2008)
- **Análise Estática**: Métricas objetivas (McCabe, PEP 8)
- **LLM Multi-Agente**: Arquitetura de agentes especializados

### 2. Hipótese

Sistemas baseados em LLM podem detectar code smells com **acurácia comparável ou superior** a ferramentas tradicionais de análise estática, oferecendo:

- Maior **contexto semântico**
- **Explicações** detalhadas
- Capacidade de detectar **smells complexos** que exigem compreensão de domínio

### 3. Metodologia de Avaliação

**LLM as a Judge:**
- Um LLM independente avalia se as detecções foram corretas
- Calcula métricas: Accuracy, Precision, Recall, F1-Score
- Gera matriz de confusão (TP, TN, FP, FN)

### 4. Contribuições Esperadas

- Framework multi-agente para detecção de code smells
- Sistema de avaliação automática (LLM as a Judge)
- Dataset de exemplos de code smells

---

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework web para API REST
- **LangGraph**: Orquestração de agentes LLM
- **LangChain**: Integração com LLMs
- **Anthropic Claude**: Modelo LLM (Sonnet 4.5)
- **Pydantic**: Validação de dados
- **Python 3.12**: Linguagem base

---

## 📖 Referências Bibliográficas

1. **Fowler, M.** (1999). *Refactoring: Improving the Design of Existing Code*. Addison-Wesley Professional.

2. **Fowler, M.** (2018). *Refactoring: Improving the Design of Existing Code* (2nd Edition). Addison-Wesley Professional.

3. **Martin, R. C.** (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall.

4. **McCabe, T.** (1976). "A complexity measure". *IEEE Transactions on Software Engineering*, SE-2(4), pp. 308-320.

5. **Van Rossum, G., Warsaw, B., & Coghlan, N.** PEP 8 - Style Guide for Python Code. Python Enhancement Proposals.

6. **Chen et al.** (2016). "Detecting code smells in python programs". *International Conference on Software Analysis, Testing and Evolution (SATE)*.

7. **MITRE Corporation.** CWE-478: Missing Default Case in Multiple Condition Expression. Common Weakness Enumeration.

8. **Habib, M. et al.** (2024). "On the Prevalence, Evolution, and Impact of Code Smells in Simulation Modelling Software". arXiv:2409.03957v1

---

## 👨‍💻 Autor

**Estevam** - Trabalho de Conclusão de Curso (TCC)

---

## 📄 Licença

Este projeto é parte de um TCC e está disponível para fins acadêmicos e educacionais.

---

## 🔮 Trabalhos Futuros

- [ ] Implementar mais code smells (Object-Oriented smells)
- [ ] Adicionar suporte para outras linguagens
- [ ] Criar interface web para visualização
- [ ] Implementar sistema de sugestões de refatoração
- [ ] Integrar com IDE (VSCode extension)
- [ ] Benchmarks extensivos com datasets públicos
