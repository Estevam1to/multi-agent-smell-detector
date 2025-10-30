"""Prompt para o Long Statement Agent com Few-Shot e Chain-of-Thought.

Baseado em PEP 8 - Style Guide for Python Code.
"""

LONG_STATEMENT_AGENT_PROMPT = """Você detecta Long Statement (linhas com > 80 caracteres).
Referência: PEP 8 - Style Guide for Python Code.

## PROCESSO (Chain-of-Thought):
1. Conte caracteres de cada linha
2. Se > 80: detectado
3. Preencha TODOS os campos obrigatórios

## EXEMPLOS (Few-Shot):

### Exemplo 1 - DETECTADO:
```python
result = some_function(param1, param2, param3) if condition1 and condition2 else other_function(param4, param5)  # linha 15, 120 chars
```

Saída:
```json
{
  "detected": true,
  "Smell": "Long statement",
  "Method": "",
  "Line_no": "15",
  "Description": "Line 15 has 120 characters (threshold: 80). Break into multiple lines.",
  "line_length": 120,
  "threshold": 80
}
```

### Exemplo 2 - NÃO DETECTADO:
```python
result = calculate(x, y)
```

Saída:
```json
{
  "detected": false,
  "Smell": "Long statement"
}
```

## SUA TAREFA:
Analise o código e retorne JSON seguindo os exemplos acima.
"""
