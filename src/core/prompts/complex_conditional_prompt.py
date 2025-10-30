"""Prompt para o Complex Conditional Agent com Few-Shot e Chain-of-Thought.

Baseado em Fowler (2018) - Refactoring, 2nd Edition.
"""

COMPLEX_CONDITIONAL_AGENT_PROMPT = """Você detecta Complex Conditional (condicionais com > 2 operadores lógicos and/or).
Referência: Fowler (2018) - Refactoring, 2nd Edition.

## PROCESSO (Chain-of-Thought):
1. Conte operadores and/or em cada condicional
2. Se > 2: adicione à lista
3. Retorne no máximo 10 detecções

## EXEMPLOS (Few-Shot):

### Exemplo 1 - MÚLTIPLAS DETECÇÕES:
```python
def check_eligibility(user):  # linha 10
    if user.age > 18 and user.verified and user.balance > 100 and user.active:  # linha 11, 3 ands
        return True

def validate_order(order):  # linha 15
    if order.paid and order.shipped and order.confirmed and order.valid:  # linha 16, 3 ands
        return True
```

Saída:
```json
{
  "detected": true,
  "detections": [
    {
      "detected": true,
      "Smell": "Complex conditional",
      "Method": "check_eligibility",
      "Line_no": "11",
      "Description": "Conditional at line 11 has 3 logical operators (threshold: 2). Extract into named boolean variables.",
      "logical_operators": 3,
      "threshold": 2
    },
    {
      "detected": true,
      "Smell": "Complex conditional",
      "Method": "validate_order",
      "Line_no": "16",
      "Description": "Conditional at line 16 has 3 logical operators (threshold: 2). Extract into named boolean variables.",
      "logical_operators": 3,
      "threshold": 2
    }
  ]
}
```

### Exemplo 2 - NÃO DETECTADO:
```python
if user.active and user.verified:
    process()
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
