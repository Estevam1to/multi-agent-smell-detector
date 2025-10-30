"""Prompt para o Long Statement Agent com Few-Shot e Chain-of-Thought.

Baseado em PEP 8 - Style Guide for Python Code.
"""

LONG_STATEMENT_AGENT_PROMPT = """Você detecta Long Statement (linhas com > 120 caracteres).
Referência: PEP 8 - Style Guide for Python Code (adaptado).

## PROCESSO (Chain-of-Thought):
1. Conte caracteres de cada linha
2. Se > 120: adicione à lista de detecções
3. Retorne no máximo 10 detecções (as linhas mais longas)

## EXEMPLOS (Few-Shot):

### Exemplo 1 - MÚLTIPLAS DETECÇÕES:
```python
x = 1  # linha 1, 5 chars, OK
result = some_function(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10)  # linha 2, 90 chars
data = {"key1": "value1", "key2": "value2", "key3": "value3", "key4": "value4", "key5": "value5"}  # linha 3, 100 chars
```

Saída:
```json
{
  "detected": true,
  "detections": [
    {
      "detected": true,
      "Smell": "Long statement",
      "Method": "",
      "Line_no": "2",
      "Description": "Line 2 has 150 characters (threshold: 120). Break into multiple lines.",
      "line_length": 150,
      "threshold": 120
    },
    {
      "detected": true,
      "Smell": "Long statement",
      "Method": "",
      "Line_no": "3",
      "Description": "Line 3 has 130 characters (threshold: 120). Break into multiple lines.",
      "line_length": 130,
      "threshold": 120
    }
  ]
}
```

### Exemplo 2 - NÃO DETECTADO:
```python
x = 1
y = 2
```

Saída:
```json
{
  "detected": false,
  "detections": []
}
```

## SUA TAREFA:
Analise o código e retorne JSON com TODAS as detecções encontradas.
"""
