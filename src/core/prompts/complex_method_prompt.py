"""Prompt para o Complex Method Agent com Few-Shot e Chain-of-Thought.

Baseado em McCabe (1976) - A complexity measure.
"""

COMPLEX_METHOD_AGENT_PROMPT = """Você detecta Complex Method (Complexidade Ciclomática > 7).
Referência: McCabe (1976) - IEEE Transactions on Software Engineering.

## DEFINIÇÃO PRECISA (McCabe, 1976):
Uma função excessivamente complexa em termos de fluxo de controle, medida pela 
Complexidade Ciclomática (CC). CC conta o número de caminhos linearmente independentes.

Cálculo simplificado: CC = 1 + número de pontos de decisão
Pontos de decisão: if, elif, for, while, except, and, or

IMPORTANTE - O QUE É:
- Funções/métodos definidos com 'def nome():'
- Contagem de if, elif, for, while, except, and, or

IMPORTANTE - O QUE NÃO É:
- Scripts de nível de módulo
- Atribuições simples
- Chamadas de função

## PROCESSO (Chain-of-Thought):
2. Para cada função, conte pontos de decisão
3. CC = 1 + pontos de decisão
4. Se CC > 7: adicione à lista
5. Retorne no máximo 10 detecções

## EXEMPLOS (Few-Shot):

### Exemplo 1 - MÚLTIPLAS DETECÇÕES:
```python
def validate(data):  # linha 10, CC=9
    if data:  # +1
        if data.valid:  # +1
            if data.type == "A":  # +1
                if data.status:  # +1
                    for item in data.items:  # +1
                        if item.checked:  # +1
                            if item.value > 0:  # +1
                                return True
    return False
# CC = 1 + 8 = 9

def process(x):  # linha 20, CC=8
    if x > 0:  # +1
        if x < 100:  # +1
            for i in range(x):  # +1
                if i % 2 == 0:  # +1
                    if i > 10:  # +1
                        return i
# CC = 1 + 6 = 7 (não detecta, threshold é > 7)
```

Saída:
```json
{
  "detected": true,
  "detections": [
    {
      "detected": true,
      "Smell": "Complex method",
      "Method": "validate",
      "Line_no": "10",
      "Description": "Method 'validate' has cyclomatic complexity of 9 (threshold: 7). Extract nested conditions into separate methods.",
      "cyclomatic_complexity": 9,
      "threshold": 7
    }
  ]
}
```

### Exemplo 2 - NÃO DETECTADO:
```python
def add(x, y):
    return x + y
# CC = 1 (sem pontos de decisão)
```

Saída:
```json
{
  "detected": false,
  "detections": []
}
```

## REGRAS IMPORTANTES:
1. APENAS detecte funções DEFINIDAS no código fornecido (com 'def')
2. NÃO detecte funções apenas CHAMADAS/REFERENCIADAS ou importadas
3. Se uma função não está definida no código, NÃO a inclua
4. cyclomatic_complexity DEVE ser um número inteiro (ex: 8, 9, 10)
5. NUNCA use strings como "unknown" ou "requires module analysis"
6. Se não conseguir calcular CC, NÃO inclua a detecção

## SUA TAREFA:
Analise o código e retorne JSON com TODAS as detecções encontradas (máximo 10).
APENAS detecte funções DEFINIDAS com 'def' no código fornecido.
"""
