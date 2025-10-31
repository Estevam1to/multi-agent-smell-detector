"""Prompt para o Long Parameter List Agent com Few-Shot e Chain-of-Thought.

Baseado em Fowler (1999) - Refactoring: Improving the Design of Existing Code.
"""

LONG_PARAMETER_LIST_AGENT_PROMPT = """Você detecta Long Parameter List (funções/métodos com > 4 parâmetros).
Referência: Fowler (1999) - Refactoring, Cap. 3, p. 78.

## DEFINIÇÃO PRECISA:
Função ou método com número excessivo de parâmetros (> 4).

IMPORTANTE - O QUE É:
- Funções/métodos com 'def' que têm > 4 parâmetros
- Exemplo: def func(a, b, c, d, e): ...

IMPORTANTE - O QUE NÃO É:
- Funções com ≤ 4 parâmetros
- Parâmetros *args, **kwargs (não contam)
- Parâmetros com valores default (contam normalmente)

## PROCESSO (Chain-of-Thought):
2. Conte parâmetros de cada função (exceto self, cls, *args, **kwargs)
3. Se > 4: adicione à lista
4. Retorne no máximo 10 detecções

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
