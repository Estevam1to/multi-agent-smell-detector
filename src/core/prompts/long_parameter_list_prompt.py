"""Prompt para o Long Parameter List Agent com Few-Shot e Chain-of-Thought.

Baseado em Fowler (1999) - Refactoring: Improving the Design of Existing Code.
"""

LONG_PARAMETER_LIST_AGENT_PROMPT = """Você detecta Long Parameter List (métodos com > 4 parâmetros).
Referência: Fowler (1999) - Refactoring.

## PROCESSO (Chain-of-Thought):
1. Conte parâmetros de cada método
2. Se > 4: adicione à lista
3. Retorne no máximo 10 detecções

## EXEMPLOS (Few-Shot):

### Exemplo 1 - MÚLTIPLAS DETECÇÕES:
```python
def create_user(name, email, age, address, phone, country):  # linha 5, 6 params
    pass

def update_order(id, status, date, amount, customer):  # linha 10, 5 params
    pass
```

Saída:
```json
{
  "detected": true,
  "detections": [
    {
      "detected": true,
      "Smell": "Long parameter list",
      "Method": "create_user",
      "Line_no": "5",
      "Description": "Method 'create_user' has 6 parameters (threshold: 4). Consider introducing a User parameter object.",
      "parameter_count": 6,
      "threshold": 4
    },
    {
      "detected": true,
      "Smell": "Long parameter list",
      "Method": "update_order",
      "Line_no": "10",
      "Description": "Method 'update_order' has 5 parameters (threshold: 4). Consider introducing an Order parameter object.",
      "parameter_count": 5,
      "threshold": 4
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
