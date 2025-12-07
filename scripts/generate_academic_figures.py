#!/usr/bin/env python3
"""Gera gráficos no estilo acadêmico para o TCC."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Configurações acadêmicas
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'axes.axisbelow': True,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Cores acadêmicas
BLUE = '#1f77b4'
ORANGE = '#ff7f0e'
GREEN = '#2ca02c'
RED = '#d62728'
GRAY = '#7f7f7f'

# Paths
BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = BASE_DIR / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
DATASET_DIR = BASE_DIR / "dataset"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    """Carrega todos os dados necessários."""
    gt = pd.read_csv(DATASET_DIR / "ground_truth" / "ground_truth_corrected.csv")
    ma_complete = pd.read_csv(RESULTS_DIR / "csv" / "results_with_complete_prompts.csv")
    ma_simple = pd.read_csv(RESULTS_DIR / "csv" / "results_simple_prompt.csv")
    dpy = pd.read_csv(RESULTS_DIR / "dpy" / "dataset_implementation_smells.csv")
    
    with open(RESULTS_DIR / "json" / "token_usage_complete_prompts.json") as f:
        tokens_complete = json.load(f)
    with open(RESULTS_DIR / "json" / "token_usage_simple_prompt.json") as f:
        tokens_simple = json.load(f)
    
    return gt, ma_complete, ma_simple, dpy, tokens_complete, tokens_simple


def normalize_smell(smell):
    if pd.isna(smell):
        return "unknown"
    return smell.lower().strip()


def extract_filename(path):
    if pd.isna(path):
        return ""
    return Path(str(path)).name


def calculate_metrics(detections_df, gt_df):
    """Calcula métricas de avaliação."""
    matched_gt = set()
    matched_det = set()
    
    for det_idx, det in detections_df.iterrows():
        for gt_idx, gt_row in gt_df.iterrows():
            if gt_idx in matched_gt:
                continue
            if det['file_name'] != gt_row['file_name']:
                continue
            if det['smell_normalized'] != gt_row['smell_normalized']:
                continue
            matched_gt.add(gt_idx)
            matched_det.add(det_idx)
            break
    
    tp = len(matched_det)
    fp = len(detections_df) - tp
    fn = len(gt_df) - len(matched_gt)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {'TP': tp, 'FP': fp, 'FN': fn, 'Precision': precision, 'Recall': recall, 'F1': f1}


def fig1_comparison_metrics(metrics_complete, metrics_simple, metrics_dpy):
    """Figura 1: Comparação de métricas entre abordagens."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    methods = ['Multi-agentes\n(Elaborados)', 'Multi-agentes\n(Simples)', 'DPy\n(Estático)']
    x = np.arange(len(methods))
    width = 0.25
    
    precision = [metrics_complete['Precision'], metrics_simple['Precision'], metrics_dpy['Precision']]
    recall = [metrics_complete['Recall'], metrics_simple['Recall'], metrics_dpy['Recall']]
    f1 = [metrics_complete['F1'], metrics_simple['F1'], metrics_dpy['F1']]
    
    bars1 = ax.bar(x - width, precision, width, label='Precision', color=BLUE)
    bars2 = ax.bar(x, recall, width, label='Recall', color=ORANGE)
    bars3 = ax.bar(x + width, f1, width, label='F1-Score', color=GREEN)
    
    ax.set_ylabel('Score')
    ax.set_ylim(0, 1)
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.legend(loc='upper right')
    ax.set_title('Comparação de Performance entre Abordagens')
    
    # Adicionar valores nas barras
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3), textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig1_comparison_metrics.pdf", bbox_inches='tight')
    plt.savefig(FIGURES_DIR / "fig1_comparison_metrics.png", bbox_inches='tight')
    plt.close()
    print("✓ Figura 1: Comparação de métricas")


def fig2_prompt_impact(metrics_complete, metrics_simple):
    """Figura 2: Impacto da qualidade dos prompts."""
    fig, ax = plt.subplots(figsize=(6, 4))
    
    metrics = ['Precision', 'Recall', 'F1-Score']
    x = np.arange(len(metrics))
    width = 0.35
    
    elaborados = [metrics_complete['Precision'], metrics_complete['Recall'], metrics_complete['F1']]
    simples = [metrics_simple['Precision'], metrics_simple['Recall'], metrics_simple['F1']]
    
    bars1 = ax.bar(x - width/2, elaborados, width, label='Prompts Elaborados', color=BLUE)
    bars2 = ax.bar(x + width/2, simples, width, label='Prompts Simples', color=ORANGE)
    
    ax.set_ylabel('Score')
    ax.set_ylim(0, 1)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()
    ax.set_title('Impacto da Qualidade dos Prompts')
    
    # Valores nas barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3), textcoords="offset points",
                       ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig2_prompt_impact.pdf", bbox_inches='tight')
    plt.savefig(FIGURES_DIR / "fig2_prompt_impact.png", bbox_inches='tight')
    plt.close()
    print("✓ Figura 2: Impacto dos prompts")


def fig3_f1_by_smell(gt, ma_complete):
    """Figura 3: F1-Score por tipo de code smell."""
    results = []
    
    for smell in gt['smell_normalized'].unique():
        det_smell = ma_complete[ma_complete['smell_normalized'] == smell]
        gt_smell = gt[gt['smell_normalized'] == smell]
        
        if len(gt_smell) == 0:
            continue
        
        metrics = calculate_metrics(det_smell, gt_smell)
        results.append({
            'Smell': smell.replace('_', ' ').title(),
            'F1': metrics['F1'],
            'GT': len(gt_smell)
        })
    
    df = pd.DataFrame(results).sort_values('F1', ascending=True)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    colors = [GREEN if f1 >= 0.7 else ORANGE if f1 >= 0.5 else RED for f1 in df['F1']]
    bars = ax.barh(df['Smell'], df['F1'], color=colors)
    
    ax.set_xlabel('F1-Score')
    ax.set_xlim(0, 1.1)
    ax.set_title('F1-Score por Tipo de Code Smell')
    ax.axvline(x=0.5, color=GRAY, linestyle='--', linewidth=0.8, alpha=0.7)
    ax.axvline(x=0.7, color=GRAY, linestyle='--', linewidth=0.8, alpha=0.7)
    
    # Valores nas barras
    for bar, f1 in zip(bars, df['F1']):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
                f'{f1:.2f}', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig3_f1_by_smell.pdf", bbox_inches='tight')
    plt.savefig(FIGURES_DIR / "fig3_f1_by_smell.png", bbox_inches='tight')
    plt.close()
    print("✓ Figura 3: F1 por tipo de smell")


def fig4_detection_distribution(gt):
    """Figura 4: Distribuição de code smells no ground truth."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    smell_counts = gt['smell_normalized'].value_counts()
    smells = [s.replace('_', ' ').title() for s in smell_counts.index]
    counts = smell_counts.values
    
    bars = ax.barh(smells, counts, color=BLUE)
    ax.set_xlabel('Número de Ocorrências')
    ax.set_title('Distribuição de Code Smells no Ground Truth')
    
    # Valores nas barras
    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                str(count), va='center', fontsize=9)
    
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig4_smell_distribution.pdf", bbox_inches='tight')
    plt.savefig(FIGURES_DIR / "fig4_smell_distribution.png", bbox_inches='tight')
    plt.close()
    print("✓ Figura 4: Distribuição de smells")


def fig5_confusion_matrix(metrics_complete, metrics_simple):
    """Figura 5: Matriz de confusão simplificada."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    
    for ax, metrics, title in [(axes[0], metrics_complete, 'Prompts Elaborados'),
                                (axes[1], metrics_simple, 'Prompts Simples')]:
        data = np.array([[metrics['TP'], metrics['FP']],
                        [metrics['FN'], 0]])
        
        im = ax.imshow(data, cmap='Blues', aspect='auto')
        
        labels = [['TP', 'FP'], ['FN', '-']]
        for i in range(2):
            for j in range(2):
                val = data[i, j]
                text = f"{labels[i][j]}\n{int(val)}" if val > 0 else "-"
                color = 'white' if val > data.max()/2 else 'black'
                ax.text(j, i, text, ha='center', va='center', color=color, fontsize=11)
        
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(['Positivo', 'Negativo'])
        ax.set_yticklabels(['Detectado', 'Não Detectado'])
        ax.set_xlabel('Ground Truth')
        ax.set_title(title)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig5_confusion_matrix.pdf", bbox_inches='tight')
    plt.savefig(FIGURES_DIR / "fig5_confusion_matrix.png", bbox_inches='tight')
    plt.close()
    print("✓ Figura 5: Matriz de confusão")


def fig6_cost_analysis(tokens_complete, tokens_simple):
    """Figura 6: Análise de custos."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    
    # Gráfico 1: Tokens utilizados
    ax1 = axes[0]
    methods = ['Elaborados', 'Simples']
    input_tokens = [tokens_complete['token_usage']['prompt_tokens']/1e6, 
                   tokens_simple['token_usage']['prompt_tokens']/1e6]
    output_tokens = [tokens_complete['token_usage']['completion_tokens']/1e6,
                    tokens_simple['token_usage']['completion_tokens']/1e6]
    
    x = np.arange(len(methods))
    width = 0.35
    
    ax1.bar(x - width/2, input_tokens, width, label='Input', color=BLUE)
    ax1.bar(x + width/2, output_tokens, width, label='Output', color=ORANGE)
    ax1.set_ylabel('Tokens (milhões)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(methods)
    ax1.legend()
    ax1.set_title('(a) Tokens Utilizados')
    
    # Gráfico 2: Custo total
    ax2 = axes[1]
    costs_complete = (tokens_complete['token_usage']['prompt_tokens'] * 3 + 
                     tokens_complete['token_usage']['completion_tokens'] * 15) / 1e6
    costs_simple = (tokens_simple['token_usage']['prompt_tokens'] * 3 + 
                   tokens_simple['token_usage']['completion_tokens'] * 15) / 1e6
    
    bars = ax2.bar(methods, [costs_complete, costs_simple], color=[BLUE, ORANGE])
    ax2.set_ylabel('Custo (USD)')
    ax2.set_title('(b) Custo Total')
    
    for bar, cost in zip(bars, [costs_complete, costs_simple]):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'${cost:.2f}', ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig6_cost_analysis.pdf", bbox_inches='tight')
    plt.savefig(FIGURES_DIR / "fig6_cost_analysis.png", bbox_inches='tight')
    plt.close()
    print("✓ Figura 6: Análise de custos")


def fig7_tp_fp_fn_comparison(metrics_complete, metrics_simple, metrics_dpy):
    """Figura 7: Comparação de TP, FP, FN."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    methods = ['Multi-agentes\n(Elaborados)', 'Multi-agentes\n(Simples)', 'DPy']
    x = np.arange(len(methods))
    width = 0.25
    
    tp = [metrics_complete['TP'], metrics_simple['TP'], metrics_dpy['TP']]
    fp = [metrics_complete['FP'], metrics_simple['FP'], metrics_dpy['FP']]
    fn = [metrics_complete['FN'], metrics_simple['FN'], metrics_dpy['FN']]
    
    ax.bar(x - width, tp, width, label='True Positives', color=GREEN)
    ax.bar(x, fp, width, label='False Positives', color=RED)
    ax.bar(x + width, fn, width, label='False Negatives', color=ORANGE)
    
    ax.set_ylabel('Quantidade')
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.legend()
    ax.set_title('Distribuição de Resultados por Abordagem')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig7_tp_fp_fn.pdf", bbox_inches='tight')
    plt.savefig(FIGURES_DIR / "fig7_tp_fp_fn.png", bbox_inches='tight')
    plt.close()
    print("✓ Figura 7: TP/FP/FN")


def main():
    """Gera todas as figuras."""
    print("=" * 60)
    print("Gerando figuras acadêmicas para o TCC")
    print("=" * 60)
    
    # Carregar dados
    gt, ma_complete, ma_simple, dpy, tokens_complete, tokens_simple = load_data()
    
    # Normalizar dados
    gt['smell_normalized'] = gt['Code_Smell'].apply(normalize_smell)
    ma_complete['smell_normalized'] = ma_complete['Code_Smell'].apply(normalize_smell)
    ma_simple['smell_normalized'] = ma_simple['Code_Smell'].apply(normalize_smell)
    dpy['smell_normalized'] = dpy['Smell'].apply(normalize_smell)
    
    gt['file_name'] = gt['File'].apply(extract_filename)
    ma_complete['file_name'] = ma_complete['File'].apply(extract_filename)
    ma_simple['file_name'] = ma_simple['File'].apply(extract_filename)
    dpy['file_name'] = dpy['File'].apply(extract_filename)
    
    # Calcular métricas
    metrics_complete = calculate_metrics(ma_complete, gt)
    metrics_simple = calculate_metrics(ma_simple, gt)
    metrics_dpy = calculate_metrics(dpy, gt)
    
    print(f"\nMétricas calculadas:")
    print(f"  Elaborados: P={metrics_complete['Precision']:.2f}, R={metrics_complete['Recall']:.2f}, F1={metrics_complete['F1']:.2f}")
    print(f"  Simples:    P={metrics_simple['Precision']:.2f}, R={metrics_simple['Recall']:.2f}, F1={metrics_simple['F1']:.2f}")
    print(f"  DPy:        P={metrics_dpy['Precision']:.2f}, R={metrics_dpy['Recall']:.2f}, F1={metrics_dpy['F1']:.2f}")
    print()
    
    # Gerar figuras
    fig1_comparison_metrics(metrics_complete, metrics_simple, metrics_dpy)
    fig2_prompt_impact(metrics_complete, metrics_simple)
    fig3_f1_by_smell(gt, ma_complete)
    fig4_detection_distribution(gt)
    fig5_confusion_matrix(metrics_complete, metrics_simple)
    fig6_cost_analysis(tokens_complete, tokens_simple)
    fig7_tp_fp_fn_comparison(metrics_complete, metrics_simple, metrics_dpy)
    
    print()
    print("=" * 60)
    print(f"Figuras salvas em: {FIGURES_DIR}")
    print("Formatos: PDF (para LaTeX) e PNG (para visualização)")
    print("=" * 60)


if __name__ == "__main__":
    main()

