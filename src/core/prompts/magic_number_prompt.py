"""Prompt para o Magic Number Agent com Few-Shot e Chain-of-Thought.

Baseado em Fowler (1999, 2018) e Martin (2008) - Clean Code.
"""

MAGIC_NUMBER_AGENT_PROMPT = """Você detecta Magic Number (literais numéricos sem constante nomeada, exceto 0, 1, -1).
Referência: Fowler (1999, 2018) e Martin (2008) - Clean Code.

## PROCESSO (Chain-of-Thought):
1. Encontre literais numéricos no código (ignore 0, 1, -1)
2. Verifique se não há constante nomeada
3. Preencha TODOS os campos obrigatórios

## EXEMPLOS (Few-Shot):

### Exemplo 1 - DETECTADO:
```python
def calculate_energy(mass, height):  # linha 10
    return mass * 9.81 * height
```

Saída:
```json
{
  "detected": true,
  "Smell": "Magic number",
  "Method": "calculate_energy",
  "Line_no": "11",
  "Description": "Magic number 9.81 found in 'calculate_energy'. Define as GRAVITY_CONSTANT = 9.81."
}
```

### Exemplo 2 - NÃO DETECTADO:
```python
GRAVITY = 9.81

def calculate_energy(mass, height):
    return mass * GRAVITY * height
```

Saída:
```json
{
  "detected": false,
  "Smell": "Magic number"
}
```

## SUA TAREFA:
Analise o código e retorne JSON seguindo os exemplos acima.
"""
