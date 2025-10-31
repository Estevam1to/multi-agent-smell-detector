"""Prompt para o Complex Conditional Agent com Few-Shot e Chain-of-Thought.

Baseado em Fowler (2018) - Refactoring, 2nd Edition.
"""

COMPLEX_CONDITIONAL_AGENT_PROMPT = """Você detecta Complex Conditional (condicionais com > 2 operadores lógicos and/or).
Referência: Fowler (2018) - Refactoring, 2nd Edition.

## DEFINIÇÃO PRECISA:
Uma instrução CONDICIONAL (if, elif, while) com número excessivo de operadores lógicos (and, or).

IMPORTANTE - O QUE É:
- Expressões em if, elif, while com múltiplos and/or
- Exemplo: if (a and b and c and d): ...

IMPORTANTE - O QUE NÃO É:
- Atribuições de variáveis (x = a and b)
- Chamadas de função (func(a, b, c))
- Operações aritméticas
- Nomes de variáveis longos

## PROCESSO (Chain-of-Thought):
2. Identifique APENAS linhas com if, elif, while
3. Conte operadores and/or na condição
4. Se > 2: adicione à lista
5. Retorne no máximo 10 detecções

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

### Exemplo 2 - NÃO DETECTADO (atribuição, não condicional):
```python
AGGREGATED_PACKAGES = util.merge_lists(a, b, "add")
x = value1 and value2 and value3
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
APENAS detecte em if, elif, while - NÃO em atribuições ou chamadas de função.
"""
