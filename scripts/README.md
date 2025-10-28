# Scripts de Análise em Batch

## 1. Análise de Múltiplos Arquivos

Analisa todos os arquivos `.py` de uma pasta e gera JSON:

```bash
python scripts/batch_analyze.py /caminho/pasta -o meu_sistema.json -p MeuProjeto
```

**Parâmetros:**
- Primeiro argumento: pasta com arquivos Python
- `-o`: arquivo de saída (padrão: `results.json`)
- `-p`: nome do projeto (padrão: `Code`)

**Saída:** JSON com todos os smells detectados no formato estruturado.

## 2. Comparação com DPy

Compara os resultados com a saída do DPy:

```bash
python scripts/compare_results.py meu_sistema.json dpy_output.json
```

**Métricas calculadas:**
- Precision
- Recall
- F1-Score
- True Positives, False Positives, False Negatives
- Detalhamento por tipo de smell

**Saída:** Relatório no terminal + `discrepancies.json` com diferenças.

## Exemplo Completo

```bash
# 1. Analisa arquivos com seu sistema
python scripts/batch_analyze.py /dataset/files/Code -o system_results.json -p Code

# 2. Roda DPy na mesma pasta (externamente)
# designite-python /dataset/files/Code -o dpy_results.json

# 3. Compara resultados
python scripts/compare_results.py system_results.json dpy_results.json
```

## Formato de Saída

Ambos os JSONs devem ter estrutura similar:

```json
[
  {
    "Project": "Code",
    "Package": "Code",
    "Module": "validate",
    "Class": "",
    "Smell": "Complex conditional",
    "Method": "validate_eligibility",
    "Line no": "49",
    "File": "/path/to/file.py",
    "Description": "..."
  }
]
```
