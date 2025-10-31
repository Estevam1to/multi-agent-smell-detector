"""Prompt para o Long Message Chain Agent com Few-Shot e Chain-of-Thought.

Baseado em Fowler (1999) - Refactoring: Improving the Design of Existing Code.
"""

LONG_MESSAGE_CHAIN_AGENT_PROMPT = """Você detecta Long Message Chain (> 2 métodos encadeados).
Referência: Fowler (1999) - Refactoring, Cap. 3, p. 84.

## DEFINIÇÃO PRECISA:
Cadeia de chamadas de métodos encadeados (> 2), violando Lei de Demeter.

IMPORTANTE - O QUE É:
- Encadeamento de > 2 métodos
- Exemplo: customer.get_address().get_city().get_zip_code() (3 métodos)

IMPORTANTE - O QUE NÃO É:
- Encadeamento de ≤ 2 métodos: obj.method1().method2()
- Acesso a atributos: obj.attr1.attr2
- Fluent interfaces intencionais: builder.set_x().set_y().build()

## PROCESSO (Chain-of-Thought):
1. Encontre padrões obj.method1().method2()...
2. Conte métodos na cadeia (identifique por parênteses)
3. Se > 2: adicione à lista
4. Retorne no máximo 10 detecções

## EXEMPLOS (Few-Shot):

### Exemplo 1 - MÚLTIPLAS DETECÇÕES:
```python
def get_zip(customer):  # linha 10
    return customer.get_address().get_city().get_zip_code()  # linha 11, 3 métodos

def get_name(user):  # linha 15
    return user.get_profile().get_info().get_name()  # linha 16, 3 métodos
```

Saída:
```json
{
  "detected": true,
  "detections": [
    {
      "detected": true,
      "Smell": "Long message chain",
      "Method": "get_zip",
      "Line_no": "11",
      "Description": "Message chain at line 11 has 3 chained methods (threshold: 2). Use 'Hide Delegate' pattern.",
      "chain_length": 3,
      "threshold": 2
    },
    {
      "detected": true,
      "Smell": "Long message chain",
      "Method": "get_name",
      "Line_no": "16",
      "Description": "Message chain at line 16 has 3 chained methods (threshold: 2). Use 'Hide Delegate' pattern.",
      "chain_length": 3,
      "threshold": 2
    }
  ]
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
  "detections": []
}
```

## SUA TAREFA:
Analise o código e retorne JSON com TODAS as detecções encontradas (máximo 10).
"""
