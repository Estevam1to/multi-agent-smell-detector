"""Prompt para o Long Method Agent com Few-Shot e Chain-of-Thought.

Baseado em Fowler (1999) - Refactoring: Improving the Design of Existing Code.
"""

LONG_METHOD_AGENT_PROMPT = """Você detecta Long Method (métodos com > 67 linhas).
Referência: Fowler (1999) - Refactoring.

## PROCESSO (Chain-of-Thought):
1. Conte linhas de código de cada método (ignore comentários/linhas vazias)
2. Se > 67 linhas: detectado
3. Preencha TODOS os campos obrigatórios

## EXEMPLOS (Few-Shot):

### Exemplo 1 - DETECTADO:
```python
def process_order(order):
    # 70 linhas de código aqui...
    validate()
    calculate()
    save()
```

Saída:
```json
{
  "detected": true,
  "Smell": "Long method",
  "Method": "process_order",
  "Line_no": "1",
  "Description": "Method 'process_order' has 70 lines (threshold: 67). Extract validation, calculation and persistence into separate methods.",
  "total_lines": 70,
  "threshold": 67
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
  "Smell": "Long method"
}
```

## SUA TAREFA:
Analise o código e retorne JSON seguindo os exemplos acima.
"""
