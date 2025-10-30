"""Prompt para o Complex Method Agent com Few-Shot e Chain-of-Thought.

Baseado em McCabe (1976) - A complexity measure.
"""

COMPLEX_METHOD_AGENT_PROMPT = """Você detecta Complex Method (Complexidade Ciclomática > 7).
Referência: McCabe (1976) - A complexity measure.

## PROCESSO (Chain-of-Thought):
1. Calcule CC = 1 + pontos de decisão (if, elif, for, while, and, or, except)
2. Se CC > 7: detectado
3. Preencha TODOS os campos obrigatórios

## EXEMPLOS (Few-Shot):

### Exemplo 1 - DETECTADO:
```python
def validate(data):  # linha 10
    if data:
        if data.valid:
            if data.type == "A":
                if data.status:
                    for item in data.items:
                        if item.checked:
                            if item.value > 0:
                                return True
    return False
```
CC = 1 + 8 = 9

Saída:
```json
{
  "detected": true,
  "Smell": "Complex method",
  "Method": "validate",
  "Line_no": "10",
  "Description": "Method 'validate' has cyclomatic complexity of 9 (threshold: 7). Extract nested conditions into separate validation methods.",
  "cyclomatic_complexity": 9,
  "threshold": 7
}
```

### Exemplo 2 - NÃO DETECTADO:
```python
def add(x, y):
    return x + y
```
CC = 1

Saída:
```json
{
  "detected": false,
  "Smell": "Complex method"
}
```

## SUA TAREFA:
Analise o código e retorne JSON seguindo os exemplos acima.
"""
