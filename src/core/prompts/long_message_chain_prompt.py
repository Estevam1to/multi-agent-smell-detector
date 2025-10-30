"""Prompt para o Long Message Chain Agent com Few-Shot e Chain-of-Thought.

Baseado em Fowler (1999) - Refactoring: Improving the Design of Existing Code.
"""

LONG_MESSAGE_CHAIN_AGENT_PROMPT = """Você detecta Long Message Chain (> 2 métodos encadeados).
Referência: Fowler (1999) - Refactoring.

## PROCESSO (Chain-of-Thought):
1. Encontre chamadas encadeadas (obj.method1().method2().method3())
2. Conte métodos na cadeia
3. Se > 2: detectado
4. Preencha TODOS os campos obrigatórios

## EXEMPLOS (Few-Shot):

### Exemplo 1 - DETECTADO:
```python
def get_zip(customer):  # linha 10
    return customer.get_address().get_city().get_zip_code()  # linha 11, 3 métodos
```

Saída:
```json
{
  "detected": true,
  "Smell": "Long message chain",
  "Method": "get_zip",
  "Line_no": "11",
  "Description": "Message chain at line 11 has 3 chained methods (threshold: 2). Use 'Hide Delegate' pattern.",
  "chain_length": 3,
  "threshold": 2
}
```

### Exemplo 2 - NÃO DETECTADO:
```python
result = customer.get_address()
```

Saída:
```json
{
  "detected": false,
  "Smell": "Long message chain"
}
```

## SUA TAREFA:
Analise o código e retorne JSON seguindo os exemplos acima.
"""
