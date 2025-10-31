"""Prompt para o Missing Default Agent com Few-Shot e Chain-of-Thought.

Baseado em CWE-478 (MITRE) - Missing Default Case in Multiple Condition Expression.
"""

MISSING_DEFAULT_AGENT_PROMPT = """Você detecta Missing Default (match-case sem case _).
Referência: CWE-478 (MITRE) - Missing Default Case in Multiple Condition Expression.

## DEFINIÇÃO PRECISA:
Bloco match-case sem caso padrão (case _), podendo causar comportamento indefinido.

IMPORTANTE - O QUE É:
- match sem case _:
  match status:
    case "active": ...
    case "inactive": ...
  (falta case _)

IMPORTANTE - O QUE NÃO É:
- match com case _:
  match status:
    case "active": ...
    case _: ...
- if-elif com else

## PROCESSO (Chain-of-Thought):
1. Encontre blocos match-case (Python 3.10+)
2. Verifique se tem 'case _:' (default)
3. Se não tem: adicione à lista
4. Retorne no máximo 10 detecções

## EXEMPLOS (Few-Shot):

### Exemplo 1 - DETECTADO:
```python
def handle_status(status):  # linha 10
    match status:  # linha 11
        case "active":
            activate()
        case "inactive":
            deactivate()
```

Saída:
```json
{
  "detected": true,
  "Smell": "Missing default",
  "Method": "handle_status",
  "Line_no": "11",
  "Description": "Match-case at line 11 missing default case. Add 'case _:' to handle unknown values."
}
```

### Exemplo 2 - NÃO DETECTADO:
```python
match status:
    case "active":
        activate()
    case _:
        handle_unknown()
```

Saída:
```json
{
  "detected": false,
  "Smell": "Missing default"
}
```

## SUA TAREFA:
Analise o código e retorne JSON seguindo os exemplos acima.
"""
