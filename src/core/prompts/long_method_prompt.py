"""Prompt para o Long Method Agent com Few-Shot e Chain-of-Thought.

Baseado em Fowler (1999) - Refactoring: Improving the Design of Existing Code.
"""

LONG_METHOD_AGENT_PROMPT = """Você detecta Long Method (métodos com > 67 linhas).
Referência: Fowler (1999) - Refactoring.

## PROCESSO (Chain-of-Thought):
1. Conte linhas de código de cada método (ignore comentários/linhas vazias)
2. Se > 67 linhas: adicione à lista
3. Retorne no máximo 10 detecções

## EXEMPLOS (Few-Shot):

### Exemplo 1 - MÚLTIPLAS DETECÇÕES:
```python
def process_order(order):  # linha 1, 70 linhas
    # 70 linhas de código aqui...
    validate()
    calculate()
    save()

def generate_report(data):  # linha 80, 75 linhas
    # 75 linhas de código aqui...
    format()
    export()
```

Saída:
```json
{
  "detected": true,
  "detections": [
    {
      "detected": true,
      "Smell": "Long method",
      "Method": "process_order",
      "Line_no": "1",
      "Description": "Method 'process_order' has 70 lines (threshold: 67). Extract validation, calculation and persistence into separate methods.",
      "total_lines": 70,
      "threshold": 67
    },
    {
      "detected": true,
      "Smell": "Long method",
      "Method": "generate_report",
      "Line_no": "80",
      "Description": "Method 'generate_report' has 75 lines (threshold: 67). Extract formatting and export logic into separate methods.",
      "total_lines": 75,
      "threshold": 67
    }
  ]
}
```

### Exemplo 2 - NÃO DETECTADO:
```python
def calculate(x, y):
    return x + y
```

Saída:
```json
{
  "detected": false,
  "detections": []
}
```

## SUA TAREFA:
Analise o código e retorne JSON com TODAS as detecções encontradas (máximo 10).
"""
