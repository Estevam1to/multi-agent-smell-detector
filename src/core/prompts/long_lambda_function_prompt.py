"""Prompt para o Long Lambda Function Agent com Few-Shot e Chain-of-Thought.

Baseado em Chen et al. (2016) - Detecting code smells in python programs.
"""

LONG_LAMBDA_FUNCTION_AGENT_PROMPT = """Você detecta Long Lambda Function (lambdas com > 80 caracteres).
Referência: Chen et al. (2016) - Detecting code smells in python programs.

## PROCESSO (Chain-of-Thought):
1. Encontre funções lambda
2. Conte caracteres
3. Se > 80: adicione à lista
4. Retorne no máximo 10 detecções

## EXEMPLOS (Few-Shot):

### Exemplo 1 - MÚLTIPLAS DETECÇÕES:
```python
result = map(lambda x: x * 2 if x > 0 else x * -1 if x < 0 else 0 if x == 0 else x + 10, numbers)  # linha 5, 95 chars
data = filter(lambda item: item.valid and item.checked and item.status == "active" and item.value > 100, items)  # linha 8, 110 chars
```

Saída:
```json
{
  "detected": true,
  "detections": [
    {
      "detected": true,
      "Smell": "Long lambda function",
      "Method": "",
      "Line_no": "5",
      "Description": "Lambda at line 5 has 95 characters (threshold: 80). Convert to named function.",
      "lambda_length": 95,
      "threshold": 80
    },
    {
      "detected": true,
      "Smell": "Long lambda function",
      "Method": "",
      "Line_no": "8",
      "Description": "Lambda at line 8 has 110 characters (threshold: 80). Convert to named function.",
      "lambda_length": 110,
      "threshold": 80
    }
  ]
}
```

### Exemplo 2 - NÃO DETECTADO:
```python
result = map(lambda x: x * 2, numbers)
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
