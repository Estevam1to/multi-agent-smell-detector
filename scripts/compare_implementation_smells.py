#!/usr/bin/env python3
import json
from collections import defaultdict

# Carregar resultados
with open('/home/luis-chaves/Área de trabalho/multi-agent-smell-detector/dataset/results/dpy_results/simple_test_implementation_smells.json') as f:
    dpy_results = json.load(f)

with open('/home/luis-chaves/Área de trabalho/multi-agent-smell-detector/dataset/results/examples_results.json') as f:
    our_results = json.load(f)

# Agrupar por tipo de smell
dpy_by_smell = defaultdict(list)
our_by_smell = defaultdict(list)

for smell in dpy_results:
    dpy_by_smell[smell['Smell']].append(smell)

for smell in our_results:
    our_by_smell[smell['Smell']].append(smell)

# Comparação
print("=" * 80)
print("COMPARAÇÃO: DPY vs NOSSO SISTEMA (Implementation Smells)")
print("=" * 80)
print()

print(f"Total DPY: {len(dpy_results)} detecções")
print(f"Total NOSSO: {len(our_results)} detecções")
print()

# Por tipo de smell
all_smells = sorted(set(list(dpy_by_smell.keys()) + list(our_by_smell.keys())))

print("DETECÇÕES POR TIPO:")
print("-" * 80)
for smell in all_smells:
    dpy_count = len(dpy_by_smell.get(smell, []))
    our_count = len(our_by_smell.get(smell, []))
    diff = our_count - dpy_count
    print(f"{smell:30} | DPY: {dpy_count:3} | NOSSO: {our_count:3} | Diff: {diff:+4}")

print()
print("=" * 80)
print("DETALHAMENTO POR SMELL")
print("=" * 80)

# Magic Number
print("\n1. MAGIC NUMBER")
print("-" * 80)
print(f"DPY detectou: {len(dpy_by_smell.get('Magic number', []))}")
for d in dpy_by_smell.get('Magic number', []):
    print(f"  - {d['Method']} linha {d['Line no']}: {d['Description']}")

print(f"\nNOSSO detectou: {len(our_by_smell.get('Magic number', []))}")
for d in our_by_smell.get('Magic number', []):
    print(f"  - {d.get('Method', 'N/A')} linha {d['Line no']}: {d['Description']}")

# Long Parameter List
print("\n2. LONG PARAMETER LIST")
print("-" * 80)
print(f"DPY detectou: {len(dpy_by_smell.get('Long parameter list', []))}")
print(f"NOSSO detectou: {len(our_by_smell.get('Long parameter list', []))}")
for d in our_by_smell.get('Long parameter list', []):
    print(f"  - {d['Method']} linha {d['Line no']}: {d['parameter_count']} params")

# Long Statement
print("\n3. LONG STATEMENT")
print("-" * 80)
print(f"DPY detectou: {len(dpy_by_smell.get('Long statement', []))}")
print(f"NOSSO detectou: {len(our_by_smell.get('Long statement', []))}")
for d in our_by_smell.get('Long statement', []):
    print(f"  - Linha {d['Line no']}: {d['line_length']} chars")

# Long Identifier
print("\n4. LONG IDENTIFIER")
print("-" * 80)
print(f"DPY detectou: {len(dpy_by_smell.get('Long identifier', []))}")
print(f"NOSSO detectou: {len(our_by_smell.get('Long identifier', []))}")
for d in our_by_smell.get('Long identifier', []):
    print(f"  - {d['identifier_name']} linha {d['Line no']}: {d['length']} chars")

# Long Message Chain
print("\n5. LONG MESSAGE CHAIN")
print("-" * 80)
print(f"DPY detectou: {len(dpy_by_smell.get('Long message chain', []))}")
print(f"NOSSO detectou: {len(our_by_smell.get('Long message chain', []))}")
for d in our_by_smell.get('Long message chain', []):
    print(f"  - {d['Method']} linha {d['Line no']}: {d['chain_length']} métodos")

# Complex Method
print("\n6. COMPLEX METHOD")
print("-" * 80)
print(f"DPY detectou: {len(dpy_by_smell.get('Complex method', []))}")
print(f"NOSSO detectou: {len(our_by_smell.get('Complex method', []))}")
for d in our_by_smell.get('Complex method', []):
    print(f"  - {d['Method']} linha {d['Line no']}: CC={d['cyclomatic_complexity']}")

print()
print("=" * 80)
print("RESUMO")
print("=" * 80)
print(f"NOSSO sistema detectou {len(our_results) - len(dpy_results):+} smells a mais que DPY")
print(f"Diferença: {len(our_results)} - {len(dpy_results)} = {len(our_results) - len(dpy_results)}")
