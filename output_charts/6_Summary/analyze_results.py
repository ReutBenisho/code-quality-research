# -*- coding: utf-8 -*-
"""
Master Unified Comparative Analysis Script for Master's Thesis
Evaluates AI Models & SonarQube against Metadata Ground Truth (Expert Reviewers)
Developed for Reut's Master's Thesis
Date: October 2026
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Headless mode for clean chart rendering
import matplotlib.pyplot as plt
import seaborn as sns

# Environment & Style Setup
sns.set_theme(style='whitegrid', palette='colorblind', font='DejaVu Sans')
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11
CHART_DPI = 200

def load_and_prepare_data(file_path='Results.json'):
    """
    Loads Results.json / Results.txt. Fails immediately if file is missing (No dummy data).
    Extracts Metadata Ground Truth directly without runtime averaging.
    """
    if not os.path.exists(file_path):
        alt = 'Results.txt' if file_path.endswith('.json') else 'Results.json'
        if os.path.exists(alt):
            file_path = alt
        else:
            raise FileNotFoundError(
                f"[{file_path}] not found in directory! Please ensure Results.json or Results.txt is placed in the execution folder."
            )
            
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        
    records = []
    models = ['ChatGPT', 'Claude', 'Gemini', 'GithubCopilot', 'Sonarqube']
    
    for key, item in raw_data.items():
        meta = item.get('metadata', {})
        
        # Ground Truth directly from Metadata
        gt_read = pd.to_numeric(meta.get('readability_score'), errors='coerce')
        gt_und  = pd.to_numeric(meta.get('understandability_score'), errors='coerce')
        gt_maint = pd.to_numeric(meta.get('maintainability_score'), errors='coerce')
        gt_overall = pd.to_numeric(meta.get('overall_quality_score'), errors='coerce')
        if np.isnan(gt_overall) and not np.isnan(gt_read):
            gt_overall = np.mean([gt_read, gt_und, gt_maint])
            
        gt_sec = str(meta.get('security_classification', '')).strip().lower()
        gt_is_vulnerable = gt_sec in ['vulnerable', 'true', '1']
        
        gt_func = str(meta.get('functional_classification', '')).strip().lower()
        gt_is_buggy = gt_func in ['buggy', 'partially correct', 'code smell/bug', 'bug']
        
        cognitive_complexity = pd.to_numeric(meta.get('cognitive_complexity', 5), errors='coerce')
        
        row_base = {
            'snippet_id': key,
            'global_id': meta.get('id'),
            'language': str(meta.get('language', '')).lower(),
            'origin': meta.get('origin'),
            'gt_read': gt_read,
            'gt_und': gt_und,
            'gt_maint': gt_maint,
            'gt_overall': gt_overall,
            'gt_is_vulnerable': gt_is_vulnerable,
            'gt_is_buggy': gt_is_buggy,
            'cognitive_complexity': cognitive_complexity
        }
        
        for m in models:
            m_data = item.get(m, {})
            row = row_base.copy()
            row['model'] = m
            row['readability'] = pd.to_numeric(m_data.get('readability_score'), errors='coerce')
            row['understandability'] = pd.to_numeric(m_data.get('understandability_score'), errors='coerce')
            row['maintainability'] = pd.to_numeric(m_data.get('maintainability_score'), errors='coerce')
            row['overall_quality'] = np.mean([row['readability'], row['understandability'], row['maintainability']]) if not np.isnan(row['readability']) else np.nan
            
            row['func_class'] = str(m_data.get('functional_classification', '')).strip().lower()
            row['sec_class'] = str(m_data.get('security_classification', '')).strip().lower()
            row['reasoning'] = str(m_data.get('reasoning', ''))
            row['reasoning_len'] = len(row['reasoning'])
            row['reasoning_words'] = len(row['reasoning'].split())
            
            # Errors against Metadata GT
            row['maint_err'] = abs(row['maintainability'] - gt_maint) if not np.isnan(row['maintainability']) else np.nan
            row['read_err'] = abs(row['readability'] - gt_read) if not np.isnan(row['readability']) else np.nan
            row['und_err'] = abs(row['understandability'] - gt_und) if not np.isnan(row['understandability']) else np.nan
            row['overall_err'] = abs(row['overall_quality'] - gt_overall) if not np.isnan(row['overall_quality']) else np.nan
            
            # Vulnerability / Bug classification harmonization
            if m.lower() == 'sonarqube':
                try:
                    sec_val = float(row['sec_class'])
                    is_vuln = sec_val < 100.0
                except ValueError:
                    is_vuln = row['sec_class'] == 'vulnerable'
                is_buggy = row['func_class'] in ['code smell/bug', 'bug', 'buggy']
            else:
                is_vuln = row['sec_class'] == 'vulnerable'
                is_buggy = row['func_class'] in ['buggy', 'partially correct']
                
            row['is_vulnerable'] = is_vuln
            row['is_buggy'] = is_buggy
            
            row['sec_correct'] = (is_vuln == gt_is_vulnerable)
            row['func_correct'] = (is_buggy == gt_is_buggy)
            row['is_overall_correct'] = row['sec_correct'] and row['func_correct']
            
            records.append(row)
            
    return pd.DataFrame(records)

def generate_all_visualizations(df, output_dir='./output_charts'):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating all analytical thesis charts and saving to: {output_dir}")
    
    ai_df = df[df['model'].str.lower() != 'sonarqube']
    
    # ----------------------------------------------------
    # Chart 1: Mean Absolute Error (MAE) vs Metadata GT
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    mae_df = df.groupby('model')['overall_err'].mean().reset_index().sort_values(by='overall_err')
    ax = sns.barplot(data=mae_df, x='model', y='overall_err', hue='model', palette='Blues_r', legend=False)
    ax.set_title("Mean Absolute Error (MAE) of Overall Quality vs. Metadata Ground Truth", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Analysis Tool / AI Engine", fontweight='bold')
    ax.set_ylabel("Mean Absolute Error (Points Deviation from GT)", fontweight='bold')
    for c in ax.containers:
        ax.bar_label(c, fmt='%.2f pts', fontweight='bold', padding=3)
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '01_mae_vs_ground_truth.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()
    
    # ----------------------------------------------------
    # Chart 2: Classification F1-Scores vs Metadata GT
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    f1_rows = []
    for model in df['model'].unique():
        sub = df[df['model'] == model]
        # Security F1
        tp_sec = ((sub['is_vulnerable'] == True) & (sub['gt_is_vulnerable'] == True)).sum()
        fp_sec = ((sub['is_vulnerable'] == True) & (sub['gt_is_vulnerable'] == False)).sum()
        fn_sec = ((sub['is_vulnerable'] == False) & (sub['gt_is_vulnerable'] == True)).sum()
        prec_sec = tp_sec / (tp_sec + fp_sec) if (tp_sec + fp_sec) > 0 else 0
        rec_sec = tp_sec / (tp_sec + fn_sec) if (tp_sec + fn_sec) > 0 else 0
        f1_sec = 2 * (prec_sec * rec_sec) / (prec_sec + rec_sec) if (prec_sec + rec_sec) > 0 else 0
        
        # Functional F1
        tp_func = ((sub['is_buggy'] == True) & (sub['gt_is_buggy'] == True)).sum()
        fp_func = ((sub['is_buggy'] == True) & (sub['gt_is_buggy'] == False)).sum()
        fn_func = ((sub['is_buggy'] == False) & (sub['gt_is_buggy'] == True)).sum()
        prec_func = tp_func / (tp_func + fp_func) if (tp_func + fp_func) > 0 else 0
        rec_func = tp_func / (tp_func + fn_func) if (tp_func + fn_func) > 0 else 0
        f1_func = 2 * (prec_func * rec_func) / (prec_func + rec_func) if (prec_func + rec_func) > 0 else 0
        
        f1_rows.append({'model': model, 'Metric': 'Security (Vulnerabilities)', 'F1_Score': f1_sec * 100})
        f1_rows.append({'model': model, 'Metric': 'Functional (Bugs)', 'F1_Score': f1_func * 100})
        
    f1_df = pd.DataFrame(f1_rows)
    ax = sns.barplot(data=f1_df, x='model', y='F1_Score', hue='Metric', palette='Set2')
    ax.set_title("F1-Score for Defect & Vulnerability Classification against Metadata GT", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Analysis Tool / AI Engine", fontweight='bold')
    ax.set_ylabel("F1 Score (%)", fontweight='bold')
    ax.set_ylim(0, 110)
    for c in ax.containers:
        ax.bar_label(c, fmt='%.1f%%', fontweight='bold', padding=3)
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '02_f1_score_classification.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()
    
    # ----------------------------------------------------
    # Chart 3: SonarQube False Negatives on Vulnerable Code
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    vuln_gt_df = df[df['gt_is_vulnerable'] == True]
    fn_rates = (1 - vuln_gt_df.groupby('model')['is_vulnerable'].mean()) * 100
    fn_df = fn_rates.reset_index().rename(columns={'is_vulnerable': 'False_Negative_Rate'}).sort_values(by='False_Negative_Rate', ascending=False)
    
    ax = sns.barplot(data=fn_df, x='model', y='False_Negative_Rate', hue='model', palette='Oranges_r', legend=False)
    ax.set_title("False Negative Rate (% Missed Vulnerabilities on Vulnerable Ground Truth)", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Analysis Tool / AI Engine", fontweight='bold')
    ax.set_ylabel("False Negative Rate (%)", fontweight='bold')
    ax.set_ylim(0, 100)
    for c in ax.containers:
        ax.bar_label(c, fmt='%.1f%%', fontweight='bold', padding=3)
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '03_sonarqube_false_negatives.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()

    # ----------------------------------------------------
    # Chart 4: Language Error Sensitivity (MAE per Language)
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=df, x='language', y='overall_err', hue='model', errorbar=None, palette='Set2')
    ax.set_title("Language Sensitivity: Overall MAE vs GT Across Programming Languages", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Programming Language", fontweight='bold')
    ax.set_ylabel("Mean Absolute Error vs GT (Points)", fontweight='bold')
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_language_error_sensitivity.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()

    # ----------------------------------------------------
    # Chart 5: Spearman Correlation Matrix (Inter-AI Consistency)
    # ----------------------------------------------------
    plt.figure(figsize=(8, 7))
    piv_corr = ai_df.pivot(index='snippet_id', columns='model', values='overall_quality')
    corr_matrix = piv_corr.corr(method='spearman')
    ax = sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='Blues', vmin=0.0, vmax=1.0,
                square=True, linewidths=1, cbar_kws={"shrink": .8})
    ax.set_title("Spearman Correlation Matrix: AI Overall Quality Scores", fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '05_inter_ai_correlation.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()

    # ----------------------------------------------------
    # Chart 6: Disagreement Range Spread Across Languages
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    pivot_lang = ai_df.pivot_table(index=['snippet_id', 'language'], columns='model', values='overall_quality', aggfunc='mean')
    pivot_lang['disagreement_range'] = pivot_lang.max(axis=1) - pivot_lang.min(axis=1)
    pivot_lang = pivot_lang.reset_index()
    
    ax = sns.boxplot(data=pivot_lang, x='language', y='disagreement_range', hue='language', palette='Purples', legend=False)
    ax.set_title("Model Disagreement Range (Max - Min Quality Spread) per Language", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Programming Language", fontweight='bold')
    ax.set_ylabel("Score Spread Among AI Engines", fontweight='bold')
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '06_disagreement_spread_per_language.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()

    # ----------------------------------------------------
    # Chart 7: ChatGPT vs. GitHub Copilot Alignment
    # ----------------------------------------------------
    plt.figure(figsize=(8, 8))
    gpt_copilot = ai_df[ai_df['model'].isin(['ChatGPT', 'GithubCopilot'])]
    pivot_pair = gpt_copilot.pivot_table(index='snippet_id', columns='model', values='overall_quality', aggfunc='mean').dropna()
    
    ax = sns.regplot(data=pivot_pair, x='ChatGPT', y='GithubCopilot',
                     scatter_kws={'alpha': 0.6, 'color': '#2b5c8f'}, line_kws={'color': '#e74c3c', 'linewidth': 2})
    ax.set_title("ChatGPT vs. GitHub Copilot Quality Score Alignment", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("ChatGPT Overall Quality Score", fontweight='bold')
    ax.set_ylabel("GitHub Copilot Overall Quality Score", fontweight='bold')
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '07_chatgpt_vs_copilot.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()

    # ----------------------------------------------------
    # Chart 8: Cognitive Complexity vs Detection Accuracy
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    df['complexity_bucket'] = pd.cut(df['cognitive_complexity'], bins=[-1, 3, 8, 100], labels=['Low (0-3)', 'Medium (4-8)', 'High (9+)'])
    comp_acc = df.groupby(['complexity_bucket', 'model'], observed=False)['is_overall_correct'].mean() * 100
    comp_acc = comp_acc.reset_index()
    
    ax = sns.barplot(data=comp_acc, x='complexity_bucket', y='is_overall_correct', hue='model', palette='tab10')
    ax.set_title("Evaluation Accuracy vs. Code Cognitive Complexity Buckets", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Cognitive Complexity Bucket", fontweight='bold')
    ax.set_ylabel("Overall Accuracy vs Metadata GT (%)", fontweight='bold')
    ax.set_ylim(0, 110)
    for c in ax.containers:
        ax.bar_label(c, fmt='%.0f%%', fontsize=7, padding=2)
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '08_complexity_vs_accuracy.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()

    # ----------------------------------------------------
    # Chart 9: Reasoning Length vs. Error / Hallucination
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    ai_df_labeled = ai_df.copy()
    ai_df_labeled['Evaluation_Result'] = np.where(ai_df_labeled['is_overall_correct'], 'Correct Evaluation', 'Error / Hallucination')
    
    ax = sns.boxplot(data=ai_df_labeled, x='model', y='reasoning_len', hue='Evaluation_Result', palette=['#2ecc71', '#e74c3c'])
    ax.set_title("AI Reasoning Character Length: Correct vs. Incorrect Evaluations", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("AI Engine", fontweight='bold')
    ax.set_ylabel("Reasoning Explanation Length (Characters)", fontweight='bold')
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '09_reasoning_vs_hallucination.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()
    
    print("All 9 master analytical charts generated successfully!")

if __name__ == '__main__':
    filename = 'Results.json'
    
    # Will fail immediately with FileNotFoundError if file is missing (No dummy data)
    df = load_and_prepare_data(filename)
    generate_all_visualizations(df, output_dir='./output_charts')
    
    # Save comprehensive summary statistics table
    summary = df.groupby('model')[['overall_err', 'maint_err', 'sec_correct', 'is_overall_correct', 'reasoning_len']].mean()
    summary['sec_correct'] = summary['sec_correct'] * 100
    summary['is_overall_correct'] = summary['is_overall_correct'] * 100
    summary.columns = ['MAE_Overall_Quality', 'MAE_Maintainability', 'Security_Accuracy_Pct', 'Overall_Accuracy_Pct', 'Avg_Reasoning_Chars']
    
    summary_path = './output_charts/summary_statistics_thesis.csv'
    summary.to_csv(summary_path)
    
    print("\n" + "="*50)
    print(" SUCCESS! Master Thesis Unified Pipeline Complete!")
    print("="*50)
    print(f"Charts saved in: ./output_charts")
    print(f"Summary table saved to: {summary_path}")
    print("\nSummary Statistics:\n", summary)