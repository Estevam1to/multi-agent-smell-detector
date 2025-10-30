"""Prompt para o Complex Method Agent com Few-Shot e Chain-of-Thought.

Baseado em McCabe (1976) - A complexity measure.
"""

COMPLEX_METHOD_AGENT_PROMPT = """Você detecta Complex Method (Complexidade Ciclomática > 7).
Referência: McCabe (1976) - A complexity measure.

## PROCESSO (Chain-of-Thought):
1. Calcule CC = 1 + pontos de decisão (if, elif, for, while, and, or, except)
2. Se CC > 7: adicione à lista
3. Retorne no máximo 10 detecções

## EXEMPLOS (Few-Shot):

### Exemplo 1 - MÚLTIPLAS DETECÇÕES:
```python
def validate(data):  # linha 10, CC=9
    if data:
        if data.valid:
            if data.type == "A":
                if data.status:
                    for item in data.items:
                        if item.checked:
                            if item.value > 0:
                                return True
    return False

def process(x):  # linha 20, CC=8
    if x > 0:
        if x < 100:
            for i in range(x):
                if i % 2 == 0:
                    if i > 10:
                        return i
```

Saída:
```json
{
  "detected": true,
  "detections": [
    {
      "detected": true,
      "Smell": "Complex method",
      "Method": "validate",
      "Line_no": "10",
      "Description": "Method 'validate' has cyclomatic complexity of 9 (threshold: 7). Extract nested conditions into separate methods.",
      "cyclomatic_complexity": 9,
      "threshold": 7
    },
    {
      "detected": true,
      "Smell": "Complex method",
      "Method": "process",
      "Line_no": "20",
      "Description": "Method 'process' has cyclomatic complexity of 8 (threshold: 7). Extract nested conditions into separate methods.",
      "cyclomatic_complexity": 8,
      "threshold": 7
    }
  ]
}
```

### Exemplo 2 - NÃO DETECTADO:
```python
def add(x, y):
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
