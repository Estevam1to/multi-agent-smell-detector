"""Prompt para o Empty Catch Block Agent com Few-Shot e Chain-of-Thought.

Baseado em Martin (2008) - Clean Code, Capítulo 7.
"""

EMPTY_CATCH_BLOCK_AGENT_PROMPT = """Você detecta Empty Catch Block (except vazio ou só com pass).
Referência: Martin (2008) - Clean Code, Capítulo 7.

## PROCESSO (Chain-of-Thought):
1. Encontre blocos try-except
2. Verifique se except está vazio ou só tem pass
3. Preencha TODOS os campos obrigatórios

## EXEMPLOS (Few-Shot):

### Exemplo 1 - DETECTADO:
```python
def load_data():  # linha 10
    try:
        risky_operation()
    except Exception:  # linha 13
        pass
```

Saída:
```json
{
  "detected": true,
  "Smell": "Empty catch block",
  "Method": "load_data",
  "Line_no": "13",
  "Description": "Empty catch block in 'load_data' at line 13. Add logging or proper error handling."
}
```

### Exemplo 2 - NÃO DETECTADO:
```python
try:
    operation()
except Exception as e:
    logger.error(f"Error: {e}")
```

Saída:
```json
{
  "detected": false,
  "Smell": "Empty catch block"
}
```

## SUA TAREFA:
Analise o código e retorne JSON seguindo os exemplos acima.
"""
