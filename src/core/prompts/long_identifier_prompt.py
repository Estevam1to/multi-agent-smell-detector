"""Prompt para o Long Identifier Agent com Few-Shot e Chain-of-Thought.

Baseado em Martin (2008) - Clean Code: A Handbook of Agile Software Craftsmanship.
"""

LONG_IDENTIFIER_AGENT_PROMPT = """Você detecta Long Identifier (nomes com > 20 caracteres).
Referência: Martin (2008) - Clean Code.

## PROCESSO (Chain-of-Thought):
1. Conte caracteres de cada identificador (função, classe, variável)
2. Se > 20: adicione à lista de detecções
3. Retorne no máximo 10 detecções (as mais críticas)

## EXEMPLOS (Few-Shot):

### Exemplo 1 - MÚLTIPLAS DETECÇÕES:
```python
DESKTOP_ENVIRONMENT_CONFIG_NAME = "config"  # linha 5, 31 chars
AGGREGATED_PACKAGES_DEBOOTSTRAP = []  # linha 10, 31 chars
def calculate_price(x):  # 15 chars, OK
    pass
```

Saída:
```json
{
  "detected": true,
  "detections": [
    {
      "detected": true,
      "Smell": "Long identifier",
      "Method": "",
      "Line_no": "5",
      "Description": "Identifier 'DESKTOP_ENVIRONMENT_CONFIG_NAME' has 31 characters (threshold: 20). Rename to 'desktop_config_name'.",
      "identifier_name": "DESKTOP_ENVIRONMENT_CONFIG_NAME",
      "length": 31,
      "threshold": 20
    },
    {
      "detected": true,
      "Smell": "Long identifier",
      "Method": "",
      "Line_no": "10",
      "Description": "Identifier 'AGGREGATED_PACKAGES_DEBOOTSTRAP' has 31 characters (threshold: 20). Rename to 'packages_debootstrap'.",
      "identifier_name": "AGGREGATED_PACKAGES_DEBOOTSTRAP",
      "length": 31,
      "threshold": 20
    }
  ]
}
```

### Exemplo 2 - NÃO DETECTADO:
```python
def calc(x):
    pass
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
