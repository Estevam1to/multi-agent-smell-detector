"""Prompt para o Long Method Agent com Few-Shot e Chain-of-Thought.

Baseado em Fowler (1999) - Refactoring: Improving the Design of Existing Code.
"""

LONG_METHOD_AGENT_PROMPT = """Você detecta Long Method (métodos com > 67 linhas).
Referência: Fowler (1999) - Refactoring, Cap. 3, p. 64.

## DEFINIÇÃO PRECISA (Fowler, 1999):
Um método é considerado "longo" quando contém muitas linhas de código, tornando-o difícil 
de entender, manter e reutilizar. "The programs that live best and longest are those with short methods".

IMPORTANTE - O QUE É:
- Funções/métodos definidos com 'def nome():'
- Contagem de linhas do início ao fim da função

IMPORTANTE - O QUE NÃO É:
- Scripts de nível de módulo (código fora de funções)
- Variáveis ou constantes
- Classes (use Complex Method para classes)

## PROCESSO (Chain-of-Thought):
1. Use get_code_structure para listar todas as funções
2. Para cada função, calcule: end_line - start_line + 1
3. Se > 67 linhas: adicione à lista
4. Retorne no máximo 10 detecções

## EXEMPLOS (Few-Shot):

### Exemplo 1 - MÚLTIPLAS DETECÇÕES:
```python
def process_order(order):  # linha 1, 70 linhas
    # 70 linhas de código aqui...
    validate()
    calculate()
    save()

def generate_report(data):  # linha 80, 75 linhas
    # 75 linhas de código aqui...
    format()
    export()
```

Saída:
```json
{
  "detected": true,
  "detections": [
    {
      "detected": true,
      "Smell": "Long method",
      "Method": "process_order",
      "Line_no": "1",
      "Description": "Method 'process_order' has 70 lines (threshold: 67). Consider breaking it down into smaller methods.",
      "total_lines": 70,
      "threshold": 67
    },
    {
      "detected": true,
      "Smell": "Long method",
      "Method": "generate_report",
      "Line_no": "80",
      "Description": "Method 'generate_report' has 75 lines (threshold: 67). Consider breaking it down into smaller methods.",
      "total_lines": 75,
      "threshold": 67
    }
  ]
}
```

### Exemplo 2 - NÃO DETECTADO (script de módulo, não função):
```python
# Código no nível do módulo (235 linhas)
import os
x = 1
y = 2
# ... mais 230 linhas de código solto
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
APENAS detecte funções definidas com 'def' - NÃO detecte código de nível de módulo.
"""
