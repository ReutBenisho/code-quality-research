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
import re
from scipy import stats

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
        gt_und = pd.to_numeric(meta.get('understandability_score'), errors='coerce')
        gt_maint = pd.to_numeric(meta.get('maintainability_score'), errors='coerce')
        gt_overall = pd.to_numeric(meta.get('overall_quality_score'), errors='coerce')
        if np.isnan(gt_overall) and not np.isnan(gt_read):
            gt_overall = np.mean([gt_read, gt_und, gt_maint])

        gt_sec = str(meta.get('security_classification', '')).strip().lower()
        gt_is_vulnerable = gt_sec in ['vulnerable', 'true', '1']

        gt_func = str(meta.get('functional_classification', '')).strip().lower()
        gt_is_buggy = gt_func in ['buggy', 'partially correct', 'code smell/bug', 'bug']
        gt_func_strict_buggy = (gt_func == 'buggy')

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
            'gt_func_strict_buggy': gt_func_strict_buggy,
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
            row['pred_func_strict_buggy'] = (row['func_class'] != 'clean') if m.lower() == 'sonarqube' else (row['func_class'] == 'buggy')

            row['sec_correct'] = (is_vuln == gt_is_vulnerable)
            row['func_correct'] = (is_buggy == gt_is_buggy)
            row['is_overall_correct'] = row['sec_correct'] and row['func_correct']

            records.append(row)

    return pd.DataFrame(records)

def plot_maintainability_mae_by_language(df, output_dir='./output_charts'):
    """Figure for the Maintainability MAE by model and language (book file: 01_mae_by_model.png)."""
    os.makedirs(output_dir, exist_ok=True)

    model_order = ['ChatGPT', 'Gemini', 'Claude', 'GithubCopilot', 'Sonarqube']
    display_names = {'ChatGPT': 'ChatGPT', 'Gemini': 'Gemini', 'Claude': 'Claude',
                     'GithubCopilot': 'GitHub Copilot', 'Sonarqube': 'SonarQube Cloud'}
    lang_order = ['cpp', 'java', 'python']
    lang_labels = {'cpp': 'C++', 'java': 'Java', 'python': 'Python'}
    lang_colors = {'cpp': '#0072B2', 'java': '#E69F00', 'python': '#009E73'}

    plot_df = df[df['model'].isin(model_order)]

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(
        data=plot_df, x='model', y='maint_err', hue='language',
        order=model_order, hue_order=lang_order,
        palette=lang_colors, errorbar=None
    )
    ax.set_xticks(range(len(model_order)))
    ax.set_xticklabels([display_names[m] for m in model_order])
    ax.set_title("Maintainability MAE by Model and Programming Language",
                 fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Analysis Tool / AI Engine", fontweight='bold')
    ax.set_ylabel("Maintainability MAE vs GT (Points)", fontweight='bold')

    max_val = plot_df.groupby(['model', 'language'])['maint_err'].mean().max()
    ax.set_ylim(0, max_val * 1.15)

    for c in ax.containers:
        ax.bar_label(c, fmt='%.1f', fontsize=8, fontweight='bold', padding=3)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, [lang_labels[l] for l in labels], title='Language',
              loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False)

    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '01_mae_by_model.png'),
                dpi=CHART_DPI, bbox_inches='tight')
    plt.close()

def generate_all_visualizations(df, output_dir='./output_charts'):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating all analytical thesis charts and saving to: {output_dir}")

    ai_df = df[df['model'].str.lower() != 'sonarqube']

    plot_maintainability_mae_by_language(df, output_dir)
    
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
        tp_sec = ((sub['is_vulnerable'] == True) & (sub['gt_is_vulnerable'] == True)).sum()
        fp_sec = ((sub['is_vulnerable'] == True) & (sub['gt_is_vulnerable'] == False)).sum()
        fn_sec = ((sub['is_vulnerable'] == False) & (sub['gt_is_vulnerable'] == True)).sum()
        prec_sec = tp_sec / (tp_sec + fp_sec) if (tp_sec + fp_sec) > 0 else 0
        rec_sec = tp_sec / (tp_sec + fn_sec) if (tp_sec + fn_sec) > 0 else 0
        f1_sec = 2 * (prec_sec * rec_sec) / (prec_sec + rec_sec) if (prec_sec + rec_sec) > 0 else 0

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
    model_colors = {
        'Claude': '#D97757',
        'ChatGPT': '#10A37F',
        'Gemini': '#1A73E8',
        'GithubCopilot': '#24292E',
        'Sonarqube': '#4E9BCD'
    }

    lang_order  = ['cpp', 'java', 'python']
    model_order = ['ChatGPT', 'Gemini', 'Claude', 'GithubCopilot', 'Sonarqube']
    display_names = {'ChatGPT': 'ChatGPT', 'Gemini': 'Gemini', 'Claude': 'Claude',
                    'GithubCopilot': 'GitHub Copilot', 'Sonarqube': 'SonarQube Cloud'}

    ax = sns.barplot(
        data=df, x='language', y='overall_err', hue='model',
        order=lang_order, hue_order=model_order,
        errorbar=None, palette=model_colors
    )
    ax.set_xticks(range(len(lang_order)))
    ax.set_xticklabels(['C++', 'Java', 'Python'])

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, [display_names[l] for l in labels], title='Model',
            loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=5, frameon=False)

    ax.set_title("Language Sensitivity: Overall MAE vs GT Across Programming Languages", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Programming Language", fontweight='bold')
    ax.set_ylabel("Mean Absolute Error vs GT (Points)", fontweight='bold')

    max_val = df.groupby(['language', 'model'])['overall_err'].mean().max()
    ax.set_ylim(0, max_val * 1.15)

    for c in ax.containers:
        ax.bar_label(c, fmt='%.1f', fontsize=8, fontweight='bold', padding=3)

    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_language_error_sensitivity.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()

    # ----------------------------------------------------
    # Chart 5: Spearman Correlation Matrix (Maintainability: Metadata GT & Tools)
    # ----------------------------------------------------
    plt.figure(figsize=(9, 8))
    piv_all = df.pivot(index='snippet_id', columns='model', values='maintainability')
    gt_scores = df.groupby('snippet_id')['gt_maint'].first()
    piv_all['GT'] = gt_scores

    desired_order = ['GT', 'ChatGPT', 'Claude', 'Gemini', 'GithubCopilot', 'Sonarqube']
    actual_cols = [c for c in desired_order if c in piv_all.columns]
    piv_ordered = piv_all[actual_cols]

    corr_matrix = piv_ordered.corr(method='spearman')
    ax = sns.heatmap(
        corr_matrix,
        annot=True,
        fmt='.3f',
        cmap='RdBu',
        center=0,
        vmin=-1.0,
        vmax=1.0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": .8}
    )
    ax.set_title("Spearman Correlation Matrix: Maintainability (GT vs. AI Models & SonarQube)", fontsize=13, fontweight='bold', pad=15)
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


def _binary_metrics_from_counts(tp: int, fp: int, tn: int, fn: int) -> dict:
    tot = tp + fp + tn + fn
    acc = (tp + tn) / tot * 100.0 if tot > 0 else np.nan
    prec = tp / (tp + fp) * 100.0 if (tp + fp) > 0 else np.nan
    rec = tp / (tp + fn) * 100.0 if (tp + fn) > 0 else np.nan
    if pd.notna(prec) and pd.notna(rec) and (prec + rec) > 0:
        f1 = 2.0 * prec * rec / (prec + rec)
    else:
        f1 = 0.0 if (pd.notna(prec) and pd.notna(rec)) else np.nan
    return {
        "TP": int(tp),
        "FP": int(fp),
        "TN": int(tn),
        "FN": int(fn),
        "Accuracy_pct": round(float(acc), 2) if pd.notna(acc) else np.nan,
        "Precision_pct": round(float(prec), 2) if pd.notna(prec) else np.nan,
        "Recall_pct": round(float(rec), 2) if pd.notna(rec) else np.nan,
        "F1_pct": round(float(f1), 2) if pd.notna(f1) else np.nan,
        "_raw_rec": float(rec) if pd.notna(rec) else np.nan,
    }


def _compute_classification_rows(sub_df: pd.DataFrame, models: list[str], extra_cols: dict | None = None) -> list[dict]:
    rows = []
    n_snippets = sub_df["snippet_id"].nunique()
    for m in models:
        m_sub = sub_df[sub_df["model"] == m]

        gt_sec = m_sub["gt_is_vulnerable"] == True
        pred_sec = m_sub["is_vulnerable"] == True
        tp_s = int((gt_sec & pred_sec).sum())
        fp_s = int((~gt_sec & pred_sec).sum())
        tn_s = int((~gt_sec & ~pred_sec).sum())
        fn_s = int((gt_sec & ~pred_sec).sum())

        gt_fb = m_sub["gt_func_strict_buggy"] == True
        pred_fb = m_sub["pred_func_strict_buggy"] == True
        tp_fb = int((gt_fb & pred_fb).sum())
        fp_fb = int((~gt_fb & pred_fb).sum())
        tn_fb = int((~gt_fb & ~pred_fb).sum())
        fn_fb = int((gt_fb & ~pred_fb).sum())

        gt_fa = m_sub["gt_is_buggy"] == True
        pred_fa = m_sub["is_buggy"] == True
        tp_fa = int((gt_fa & pred_fa).sum())
        fp_fa = int((~gt_fa & pred_fa).sum())
        tn_fa = int((~gt_fa & ~pred_fa).sum())
        fn_fa = int((gt_fa & ~pred_fa).sum())

        sec_m = _binary_metrics_from_counts(tp_s, fp_s, tn_s, fn_s)
        fb_m = _binary_metrics_from_counts(tp_fb, fp_fb, tn_fb, fn_fb)
        fa_m = _binary_metrics_from_counts(tp_fa, fp_fa, tn_fa, fn_fa)

        raw_recs = [x for x in (sec_m["_raw_rec"], fb_m["_raw_rec"]) if pd.notna(x)]
        macro_rec_bug = float(np.mean(raw_recs)) if raw_recs else np.nan

        denom_pooled = (tp_s + fn_s) + (tp_fb + fn_fb)
        pooled_rec_bug = ((tp_s + tp_fb) / denom_pooled * 100.0) if denom_pooled > 0 else np.nan

        row = {}
        if extra_cols:
            row.update(extra_cols)
        row.update({
            "Model": m,
            "N_Snippets": int(n_snippets),
            "Sec_TP": sec_m["TP"], "Sec_FP": sec_m["FP"], "Sec_TN": sec_m["TN"], "Sec_FN": sec_m["FN"],
            "Sec_Acc_pct": sec_m["Accuracy_pct"],
            "Sec_Prec_pct": sec_m["Precision_pct"],
            "Sec_Rec_pct": sec_m["Recall_pct"],
            "Sec_F1_pct": sec_m["F1_pct"],
            "FuncBug_TP": fb_m["TP"], "FuncBug_FP": fb_m["FP"], "FuncBug_TN": fb_m["TN"], "FuncBug_FN": fb_m["FN"],
            "FuncBug_Acc_pct": fb_m["Accuracy_pct"],
            "FuncBug_Prec_pct": fb_m["Precision_pct"],
            "FuncBug_Rec_pct": fb_m["Recall_pct"],
            "FuncBug_F1_pct": fb_m["F1_pct"],
            "MacroRec_Sec_FuncBug_pct": round(macro_rec_bug, 2) if pd.notna(macro_rec_bug) else np.nan,
            "PooledRec_Sec_FuncBug_pct": round(pooled_rec_bug, 2) if pd.notna(pooled_rec_bug) else np.nan,
            "FuncAny_TP": fa_m["TP"], "FuncAny_FP": fa_m["FP"], "FuncAny_TN": fa_m["TN"], "FuncAny_FN": fa_m["FN"],
            "FuncAny_Acc_pct": fa_m["Accuracy_pct"],
            "FuncAny_Prec_pct": fa_m["Precision_pct"],
            "FuncAny_Rec_pct": fa_m["Recall_pct"],
            "FuncAny_F1_pct": fa_m["F1_pct"],
        })
        rows.append(row)
    return rows


METRIC_FULL_LABELS = {
    "N_Snippets": "Number of Snippets",
    "Sec_TP": "Security - True Positives",
    "Sec_FP": "Security - False Positives",
    "Sec_TN": "Security - True Negatives",
    "Sec_FN": "Security - False Negatives",
    "Sec_Acc_pct": "Security - Accuracy (%)",
    "Sec_Prec_pct": "Security - Precision (%)",
    "Sec_Rec_pct": "Security - Recall (%)",
    "Sec_F1_pct": "Security - F1 Score (%)",
    "FuncBug_TP": "Functional (Buggy Only) - True Positives",
    "FuncBug_FP": "Functional (Buggy Only) - False Positives",
    "FuncBug_TN": "Functional (Buggy Only) - True Negatives",
    "FuncBug_FN": "Functional (Buggy Only) - False Negatives",
    "FuncBug_Acc_pct": "Functional (Buggy Only) - Accuracy (%)",
    "FuncBug_Prec_pct": "Functional (Buggy Only) - Precision (%)",
    "FuncBug_Rec_pct": "Functional (Buggy Only) - Recall (%)",
    "FuncBug_F1_pct": "Functional (Buggy Only) - F1 Score (%)",
    "MacroRec_Sec_FuncBug_pct": "Macro Average Recall (Security & Buggy Only) (%)",
    "PooledRec_Sec_FuncBug_pct": "Pooled Recall (Security & Buggy Only) (%)",
    "FuncAny_TP": "Functional (Buggy + Partially Correct) - True Positives",
    "FuncAny_FP": "Functional (Buggy + Partially Correct) - False Positives",
    "FuncAny_TN": "Functional (Buggy + Partially Correct) - True Negatives",
    "FuncAny_FN": "Functional (Buggy + Partially Correct) - False Negatives",
    "FuncAny_Acc_pct": "Functional (Buggy + Partially Correct) - Accuracy (%)",
    "FuncAny_Prec_pct": "Functional (Buggy + Partially Correct) - Precision (%)",
    "FuncAny_Rec_pct": "Functional (Buggy + Partially Correct) - Recall (%)",
    "FuncAny_F1_pct": "Functional (Buggy + Partially Correct) - F1 Score (%)",
}

def _to_camel_alpha(text: str) -> str:
    """Converts text to alphabetic-only CamelCase safe for LaTeX \\newcommand."""
    words = re.findall(r"[A-Za-z]+", text)
    return "".join(w.capitalize() for w in words)


def export_language_overall_and_macros(
    df: pd.DataFrame,
    by_lang_df: pd.DataFrame,
    output_dir: str = "./output_charts",
    tex_out_path: str = "./output_charts/thesis_metrics_macros.tex",
):
    """
    Exports a per-language overall summary CSV (GT counts + mean metrics across engines)
    and appends per-language (overall & per-model) LaTeX macros to thesis_metrics_macros.tex.
    """
    os.makedirs(output_dir, exist_ok=True)

    # 1. Per-language Ground Truth counts (one row per snippet)
    snip_gt = df.drop_duplicates(subset=["snippet_id"]).copy()
    gt_lang = (
        snip_gt.groupby("language", dropna=False)
        .agg(
            N_Snippets=("snippet_id", "nunique"),
            GT_Sec_Vulnerable=("gt_is_vulnerable", "sum"),
            GT_Sec_Safe=("gt_is_vulnerable", lambda s: int((~s).sum())),
            GT_FuncBug_Count=("gt_func_strict_buggy", "sum"),
            GT_FuncAny_Count=("gt_is_buggy", "sum"),
        )
        .reset_index()
        .rename(columns={"language": "Language"})
    )

    # 2. Mean metrics across all engines per language
    numeric_cols = [
        c for c in by_lang_df.columns
        if c not in ("Language", "Model", "N_Snippets") and pd.api.types.is_numeric_dtype(by_lang_df[c])
    ]
    mean_all_lang = by_lang_df.groupby("Language", dropna=False)[numeric_cols].mean().round(2).reset_index()
    mean_all_lang.columns = [
        "Language" if c == "Language" else f"AllEnginesMean_{c}" for c in mean_all_lang.columns
    ]

    # 3. Mean metrics across AI models only (excluding SonarQube) per language
    ai_lang_df = by_lang_df[by_lang_df["Model"].str.lower() != "sonarqube"]
    mean_ai_lang = ai_lang_df.groupby("Language", dropna=False)[numeric_cols].mean().round(2).reset_index()
    mean_ai_lang.columns = [
        "Language" if c == "Language" else f"AIMean_{c}" for c in mean_ai_lang.columns
    ]

    lang_summary_df = gt_lang.merge(mean_all_lang, on="Language", how="left").merge(mean_ai_lang, on="Language", how="left")
    lang_summary_path = os.path.join(output_dir, "language_overall_summary.csv")
    lang_summary_df.to_csv(lang_summary_path, index=False)
    print(f" - {lang_summary_path}")

    # 4. Append per-language macros (overall & per-model) to thesis_metrics_macros.tex
    macro_lines = ["", "% === Per-Language Overall (GT & Mean Across Engines) Macros ==="]
    for _, r in lang_summary_df.iterrows():
        lang_tag = _to_camel_alpha(r["Language"])
        for col in ["N_Snippets", "GT_Sec_Vulnerable", "GT_Sec_Safe", "GT_FuncBug_Count", "GT_FuncAny_Count"]:
            if pd.notna(r[col]):
                macro_lines.append(f"\\newcommand{{\\{lang_tag}{_to_camel_alpha(col)}}}{{{int(round(float(r[col])))}}}")
        for col in [c for c in lang_summary_df.columns if c.endswith("_pct")]:
            if pd.notna(r[col]):
                macro_lines.append(f"\\newcommand{{\\{lang_tag}{_to_camel_alpha(col)}}}{{{float(r[col]):.2f}\\%}}")

    macro_lines.append("")
    macro_lines.append("% === Per-Language Per-Engine Macros ===")
    for _, r in by_lang_df.iterrows():
        m = str(r["Model"])
        m_camel = m[0].lower() + m[1:]
        lang_tag = _to_camel_alpha(r["Language"])
        for col in ["Sec_TP", "Sec_FP", "Sec_TN", "Sec_FN", "FuncBug_TP", "FuncBug_FP", "FuncBug_TN", "FuncBug_FN", "FuncAny_TP", "FuncAny_FP", "FuncAny_TN", "FuncAny_FN"]:
            if col in r and pd.notna(r[col]):
                macro_lines.append(f"\\newcommand{{\\{m_camel}{lang_tag}{_to_camel_alpha(col)}}}{{{int(round(float(r[col])))}}}")
        for col in [c for c in by_lang_df.columns if c.endswith("_pct")]:
            if pd.notna(r[col]):
                macro_lines.append(f"\\newcommand{{\\{m_camel}{lang_tag}{_to_camel_alpha(col)}}}{{{float(r[col]):.2f}\\%}}")

    if os.path.exists(tex_out_path):
        with open(tex_out_path, "r", encoding="utf-8") as f:
            existing = f.read()
        marker = "% === Per-Language Overall"
        if marker in existing:
            existing = existing.split(marker)[0].rstrip() + "\n"
        with open(tex_out_path, "w", encoding="utf-8") as f:
            f.write(existing + "\n".join(macro_lines).strip() + "\n")
        print(f" - Updated {tex_out_path} with per-language macros")

    return lang_summary_df

def export_latex_macros_from_transposed_csv(
    transposed_csv_path: str = "./output_charts/full_classification_matrices_overall_transposed.csv",
    tex_out_path: str = "./output_charts/thesis_metrics_macros.tex",
) -> str:
    """
    Reads the transposed classification CSV and generates a LaTeX macro file
    so metrics can be referenced consistently across Overleaf without manual entry.
    """
    df_t = pd.read_csv(transposed_csv_path)
    model_cols = [c for c in df_t.columns if c != "Metric"]

    lines = [
        "% Auto-generated LaTeX metric commands for Overleaf",
        "% Source: full_classification_matrices_overall_transposed.csv",
        "",
    ]

    for _, row in df_t.iterrows():
        metric_label = str(row["Metric"])
        is_pct = "(%)" in metric_label
        is_count = any(k in metric_label for k in ("Positives", "Negatives", "Snippets"))

        clean_metric = metric_label.replace("(%)", "").strip()
        metric_camel = _to_camel_alpha(clean_metric)
        suffix = "Pct" if is_pct else ""

        for m in model_cols:
            model_camel = m[0].lower() + m[1:]
            val = row[m]
            if pd.isna(val):
                formatted = "N/A"
            elif is_count:
                formatted = f"{int(round(float(val)))}"
            elif is_pct:
                formatted = f"{float(val):.2f}\\%"
            else:
                formatted = f"{float(val):.2f}"

            cmd_name = f"\\{model_camel}{metric_camel}{suffix}"
            lines.append(f"\\newcommand{{{cmd_name}}}{{{formatted}}}")
        lines.append("")
# Extra derived security macros (Total Vulnerable & FNR) from transposed CSV
    lines.append("% Derived Security Total Vulnerable & False Negative Rate (FNR)")
    for m in model_cols:
        model_camel = m[0].lower() + m[1:]
        tp_val = row_val = df_t.set_index("Metric")[m].get("Security - True Positives")
        fn_val = df_t.set_index("Metric")[m].get("Security - False Negatives")
        if pd.notna(tp_val) and pd.notna(fn_val):
            tp_int, fn_int = int(round(float(tp_val))), int(round(float(fn_val)))
            tot_vuln = tp_int + fn_int
            fnr_pct = (fn_int / tot_vuln * 100.0) if tot_vuln > 0 else 0.0
            lines.append(f"\\newcommand{{\\{model_camel}SecurityTotalVulnerable}}{{{tot_vuln}}}")
            lines.append(f"\\newcommand{{\\{model_camel}SecurityFnrPct}}{{{fnr_pct:.2f}\\%}}")
    lines.append("")

    # Per-language security accuracy macros (if by_language CSV exists)
    by_lang_csv_path = os.path.join(os.path.dirname(transposed_csv_path), "full_classification_matrices_by_language.csv")
    if os.path.exists(by_lang_csv_path):
        df_lang = pd.read_csv(by_lang_csv_path)
        lines.append("% Per-language Security Accuracy (%)")
        for _, r in df_lang.iterrows():
            m = str(r["Model"])
            model_camel = m[0].lower() + m[1:]
            lang_cap = str(r["Language"]).strip().capitalize()
            acc_val = r.get("Sec_Acc_pct")
            if pd.notna(acc_val) and lang_cap:
                lines.append(f"\\newcommand{{\\{model_camel}{lang_cap}SecurityAccuracyPct}}{{{float(acc_val):.2f}\\%}}")
        lines.append("")

    # Extra derived security macros (Total Safe, Total Vulnerable, Predicted Safe, FNR)
    lines.append("% Derived Security Counts & False Negative Rate (FNR)")
    metric_series = df_t.set_index("Metric")
    for m in model_cols:
        model_camel = m[0].lower() + m[1:]
        tp_val = metric_series[m].get("Security - True Positives")
        fp_val = metric_series[m].get("Security - False Positives")
        tn_val = metric_series[m].get("Security - True Negatives")
        fn_val = metric_series[m].get("Security - False Negatives")
        if all(pd.notna(x) for x in (tp_val, fp_val, tn_val, fn_val)):
            tp_int = int(round(float(tp_val)))
            fp_int = int(round(float(fp_val)))
            tn_int = int(round(float(tn_val)))
            fn_int = int(round(float(fn_val)))
            tot_safe = tn_int + fp_int
            tot_vuln = tp_int + fn_int
            pred_safe = tn_int + fn_int
            fnr_pct = (fn_int / tot_vuln * 100.0) if tot_vuln > 0 else 0.0
            lines.append(f"\\newcommand{{\\{model_camel}SecurityTotalSafe}}{{{tot_safe}}}")
            lines.append(f"\\newcommand{{\\{model_camel}SecurityTotalVulnerable}}{{{tot_vuln}}}")
            lines.append(f"\\newcommand{{\\{model_camel}SecurityPredictedSafeCount}}{{{pred_safe}}}")
            lines.append(f"\\newcommand{{\\{model_camel}SecurityFnrPct}}{{{fnr_pct:.2f}\\%}}")
    lines.append("")

    n_snip_val = metric_series[m].get("Number of Snippets")
    if pd.notna(n_snip_val):
        n_snip_int = int(round(float(n_snip_val)))
        lines.append(f"\\newcommand{{\\{model_camel}SecurityNumberOfSnippets}}{{{n_snip_int}}}")

    tex_content = "\n".join(lines).strip() + "\n"
    with open(tex_out_path, "w", encoding="utf-8") as f:
        f.write(tex_content)

    print(f" - {tex_out_path}")
    return tex_content

def export_transposed_overall_matrix(overall_df: pd.DataFrame, output_dir: str = "./output_charts") -> pd.DataFrame:
    """
    Transposes the overall classification matrix so models are columns and full metric names are rows.
    """
    os.makedirs(output_dir, exist_ok=True)
    indexed = overall_df.set_index("Model")
    transposed = indexed.T
    transposed.index = [METRIC_FULL_LABELS.get(col_name, col_name) for col_name in transposed.index]
    transposed.index.name = "Metric"
    transposed_df = transposed.reset_index()

    out_path = os.path.join(output_dir, "full_classification_matrices_overall_transposed.csv")
    transposed_df.to_csv(out_path, index=False)
    print(f" - {out_path}")
    export_latex_macros_from_transposed_csv(transposed_csv_path=out_path, tex_out_path=os.path.join(output_dir, "metrics_macros.tex"))
    return transposed_df

def export_classification_matrices(df: pd.DataFrame, output_dir: str = "./output_charts"):
    """
    Exports overall, per-language, macro-across-languages, and ChatGPT audit CSV tables
    directly from the prepared analysis DataFrame.
    """
    os.makedirs(output_dir, exist_ok=True)
    models = ["ChatGPT", "Claude", "Gemini", "GithubCopilot", "Sonarqube"]

    work_df = df.copy()
    if "gt_func_strict_buggy" not in work_df.columns:
        work_df["gt_func_strict_buggy"] = False
    if "pred_func_strict_buggy" not in work_df.columns:
        work_df["pred_func_strict_buggy"] = np.where(
            work_df["model"].str.lower() == "sonarqube",
            work_df["func_class"] != "clean",
            work_df["func_class"] == "buggy",
        )

    overall_df = pd.DataFrame(_compute_classification_rows(work_df, models))
    overall_path = os.path.join(output_dir, "full_classification_matrices_overall.csv")
    overall_df.to_csv(overall_path, index=False)

    languages = sorted([x for x in work_df["language"].dropna().unique() if str(x).strip() != ""])
    lang_rows = []
    for lang in languages:
        sub_lang = work_df[work_df["language"] == lang]
        lang_rows.extend(_compute_classification_rows(sub_lang, models, extra_cols={"Language": lang}))
    by_lang_df = pd.DataFrame(lang_rows)
    by_lang_path = os.path.join(output_dir, "full_classification_matrices_by_language.csv")
    by_lang_df.to_csv(by_lang_path, index=False)

    macro_lang_rows = []
    for m in models:
        sub_m = by_lang_df[by_lang_df["Model"] == m]
        macro_lang_rows.append({
            "Model": m,
            "MacroLang_Sec_Rec_pct": round(float(sub_m["Sec_Rec_pct"].mean()), 2),
            "MacroLang_FuncBug_Rec_pct": round(float(sub_m["FuncBug_Rec_pct"].mean()), 2),
            "MacroLang_FuncAny_Rec_pct": round(float(sub_m["FuncAny_Rec_pct"].mean()), 2),
        })
    macro_lang_df = pd.DataFrame(macro_lang_rows)
    macro_lang_path = os.path.join(output_dir, "macro_recall_across_languages.csv")
    macro_lang_df.to_csv(macro_lang_path, index=False)

    cg_overall = overall_df[overall_df["Model"] == "ChatGPT"].iloc[0]
    audit_rows = [{
        "Scope": "Overall",
        "N_Snippets": cg_overall["N_Snippets"],
        "Sec_TP": cg_overall["Sec_TP"],
        "Sec_FP": cg_overall["Sec_FP"],
        "Sec_TN": cg_overall["Sec_TN"],
        "Sec_FN": cg_overall["Sec_FN"],
        "Sec_Acc_pct": cg_overall["Sec_Acc_pct"],
        "Sec_Prec_pct": cg_overall["Sec_Prec_pct"],
        "Sec_Rec_pct": cg_overall["Sec_Rec_pct"],
        "Sec_F1_pct": cg_overall["Sec_F1_pct"],
    }]
    for _, r in by_lang_df[by_lang_df["Model"] == "ChatGPT"].iterrows():
        audit_rows.append({
            "Scope": f"Language={r['Language']}",
            "N_Snippets": r["N_Snippets"],
            "Sec_TP": r["Sec_TP"],
            "Sec_FP": r["Sec_FP"],
            "Sec_TN": r["Sec_TN"],
            "Sec_FN": r["Sec_FN"],
            "Sec_Acc_pct": r["Sec_Acc_pct"],
            "Sec_Prec_pct": r["Sec_Prec_pct"],
            "Sec_Rec_pct": r["Sec_Rec_pct"],
            "Sec_F1_pct": r["Sec_F1_pct"],
        })
    chatgpt_audit_df = pd.DataFrame(audit_rows)
    chatgpt_audit_path = os.path.join(output_dir, "chatgpt_audit_breakdown.csv")
    chatgpt_audit_df.to_csv(chatgpt_audit_path, index=False)

    print("Classification matrix CSVs saved:")
    for p in (overall_path, by_lang_path, macro_lang_path, chatgpt_audit_path):
        print(" -", p)

    transposed_overall_df = export_transposed_overall_matrix(overall_df, output_dir=output_dir)

    lang_summary_df = export_language_overall_and_macros(
        df=work_df,
        by_lang_df=by_lang_df,
        output_dir=output_dir,
        tex_out_path=os.path.join(output_dir, "metrics_macros.tex"),
    )

    return {
        "overall": overall_df,
        "overall_transposed": transposed_overall_df,
        "by_language": by_lang_df,
        "macro_by_language": macro_lang_df,
        "chatgpt_audit": chatgpt_audit_df,
    }

def append_language_overall_mae_macros(
    df: pd.DataFrame,
    tex_out_path: str = "./metrics_macros.tex",
):
    """
    Appends per-language per-model Overall Quality MAE macros (from overall_err)
    to thesis_metrics_macros.tex.
    """
    if "overall_err" not in df.columns or not os.path.exists(tex_out_path):
        return

    mae_piv = df.pivot_table(index="model", columns="language", values="overall_err", aggfunc="mean")
    lines = ["", "% === Per-Language Per-Engine Overall Quality MAE Macros ==="]
    for m in mae_piv.index:
        m_camel = str(m)[0].lower() + str(m)[1:]
        for lang in mae_piv.columns:
            val = mae_piv.loc[m, lang]
            if pd.notna(val) and str(lang).strip():
                lang_tag = _to_camel_alpha(lang)
                lines.append(f"\\newcommand{{\\{m_camel}{lang_tag}OverallMae}}{{{float(val):.2f}}}")

    with open(tex_out_path, "r", encoding="utf-8") as f:
        existing = f.read()

    marker = "% === Per-Language Per-Engine Overall Quality MAE Macros ==="
    if marker in existing:
        existing = existing.split(marker)[0].rstrip() + "\n"

    with open(tex_out_path, "w", encoding="utf-8") as f:
        f.write(existing + "\n".join(lines).strip() + "\n")
    print(f" - Updated {tex_out_path} with per-language Overall MAE macros")

def export_mae_by_language_and_criterion(df, output_dir='./output_charts'):
    os.makedirs(output_dir, exist_ok=True)
    
    mae_breakdown = (
        df.groupby(['language', 'model'], dropna=False)[
            ['read_err', 'und_err', 'maint_err', 'overall_err']
        ]
        .agg(['mean', 'count'])
    )
    
    # השטחת שמות העמודות לנוחות עבודה ב-CSV / Excel / pandas
    mae_breakdown.columns = [f"{metric}_{stat}" for metric, stat in mae_breakdown.columns]
    mae_breakdown = mae_breakdown.reset_index()
    
    # עיגול עמודות הממוצע ל-3 ספרות אחרי הנקודה
    mean_cols = [c for c in mae_breakdown.columns if c.endswith('_mean')]
    mae_breakdown[mean_cols] = mae_breakdown[mean_cols].round(3)
    
    out_path = os.path.join(output_dir, 'mae_by_language_model_criterion.csv')
    mae_breakdown.to_csv(out_path, index=False)
    print(f"Saved detailed MAE breakdown to: {out_path}")
    return mae_breakdown

def export_reasoning_length_stats_and_macros(
    df: pd.DataFrame,
    output_dir: str = ".",
    tex_out_path: str = "./metrics_macros.tex",
) -> pd.DataFrame:
    """
    Exports reasoning character length comparison (Accurate vs. Erroneous evaluations)
    to CSV and appends LaTeX macros to thesis_metrics_macros.tex.
    """
    os.makedirs(output_dir, exist_ok=True)
    ai_df = df[df["model"].str.lower() != "sonarqube"].copy()

    rows = []
    for m in ["ChatGPT", "Claude", "Gemini", "GithubCopilot"]:
        sub = ai_df[ai_df["model"] == m]
        acc_lens = sub[sub["is_overall_correct"] == True]["reasoning_len"]
        err_lens = sub[sub["is_overall_correct"] == False]["reasoning_len"]

        acc_mean = float(acc_lens.mean()) if len(acc_lens) > 0 else np.nan
        err_mean = float(err_lens.mean()) if len(err_lens) > 0 else np.nan
        delta = err_mean - acc_mean if (pd.notna(acc_mean) and pd.notna(err_mean)) else np.nan

        rows.append({
            "Model": m,
            "Accurate_Count": int(len(acc_lens)),
            "Erroneous_Count": int(len(err_lens)),
            "Accurate_Mean_Chars": round(acc_mean, 2),
            "Erroneous_Mean_Chars": round(err_mean, 2),
            "Delta_Chars": round(delta, 2),
        })

    res_df = pd.DataFrame(rows)
    csv_path = os.path.join(output_dir, "reasoning_length_invariance.csv")
    res_df.to_csv(csv_path, index=False)
    print(f" - {csv_path}")

    macro_lines = ["", "% === Reasoning Length Invariance Macros (Chars) ==="]
    for _, r in res_df.iterrows():
        m = str(r["Model"])
        m_camel = m[0].lower() + m[1:]
        acc_val = float(r["Accurate_Mean_Chars"])
        err_val = float(r["Erroneous_Mean_Chars"])
        delta_val = float(r["Delta_Chars"])
        delta_str = f"{delta_val:+.2f}"

        macro_lines.append(f"\\newcommand{{\\{m_camel}ReasoningAccurateChars}}{{{acc_val:.2f}}}")
        macro_lines.append(f"\\newcommand{{\\{m_camel}ReasoningErroneousChars}}{{{err_val:.2f}}}")
        macro_lines.append(f"\\newcommand{{\\{m_camel}ReasoningDeltaChars}}{{{delta_str}}}")

    if os.path.exists(tex_out_path):
        with open(tex_out_path, "r", encoding="utf-8") as f:
            existing = f.read()
        marker = "% === Reasoning Length Invariance Macros (Chars) ==="
        if marker in existing:
            existing = existing.split(marker)[0].rstrip() + "\n"
        with open(tex_out_path, "w", encoding="utf-8") as f:
            f.write(existing + "\n".join(macro_lines).strip() + "\n")
        print(f" - Updated {tex_out_path} with reasoning length macros")

    return res_df


def export_chatgpt_vs_copilot_stats_and_macros(
    df: pd.DataFrame,
    overall_df: pd.DataFrame,
    output_dir: str = "./output_charts",
    tex_out_path: str = "./output_charts/thesis_metrics_macros.tex",
) -> pd.DataFrame:
    """
    Exports ChatGPT vs. GitHub Copilot alignment, MAE, and security comparison metrics
    to CSV and appends LaTeX macros to thesis_metrics_macros.tex.
    """
    os.makedirs(output_dir, exist_ok=True)

    piv_q = df.pivot(index="snippet_id", columns="model", values="overall_quality").dropna(
        subset=["ChatGPT", "GithubCopilot"]
    )
    r_val, _ = stats.pearsonr(piv_q["ChatGPT"], piv_q["GithubCopilot"])
    slope, intercept, _, _, _ = stats.linregress(piv_q["ChatGPT"], piv_q["GithubCopilot"])
    pred_at_85 = float(slope * 85.0 + intercept)

    ov_idx = overall_df.set_index("Model")
    rows = []
    for m in ["ChatGPT", "GithubCopilot"]:
        sub = df[df["model"] == m]
        rows.append({
            "Model": m,
            "Pearson_r_Overall": round(float(r_val), 2),
            "Pred_Copilot_At_85": round(pred_at_85, 2),
            "Read_MAE": round(float(sub["read_err"].mean()), 2),
            "Und_MAE": round(float(sub["und_err"].mean()), 2),
            "Maint_MAE": round(float(sub["maint_err"].mean()), 2),
            "Overall_MAE": round(float(sub["overall_err"].mean()), 2),
            "Sec_Acc_pct": round(float(ov_idx.loc[m, "Sec_Acc_pct"]), 2),
            "Sec_Prec_pct": round(float(ov_idx.loc[m, "Sec_Prec_pct"]), 2),
            "Sec_Rec_pct": round(float(ov_idx.loc[m, "Sec_Rec_pct"]), 2),
            "Sec_FP": int(round(float(ov_idx.loc[m, "Sec_FP"]))),
        })

    comp_df = pd.DataFrame(rows)
    csv_path = os.path.join(output_dir, "chatgpt_vs_copilot_comparison.csv")
    comp_df.to_csv(csv_path, index=False)
    print(f" - {csv_path}")

    cg = comp_df[comp_df["Model"] == "ChatGPT"].iloc[0]
    cop = comp_df[comp_df["Model"] == "GithubCopilot"].iloc[0]

    read_rel_pct = (float(cg["Read_MAE"]) - float(cop["Read_MAE"])) / float(cop["Read_MAE"]) * 100.0
    und_rel_pct = (float(cg["Und_MAE"]) - float(cop["Und_MAE"])) / float(cop["Und_MAE"]) * 100.0
    maint_rel_pct = (float(cg["Maint_MAE"]) - float(cop["Maint_MAE"])) / float(cop["Maint_MAE"]) * 100.0

    sec_acc_pp = float(cg["Sec_Acc_pct"]) - float(cop["Sec_Acc_pct"])
    prec_pp = float(cg["Sec_Prec_pct"]) - float(cop["Sec_Prec_pct"])
    rec_pp = float(cg["Sec_Rec_pct"]) - float(cop["Sec_Rec_pct"])

    macro_lines = [
        "",
        "% === ChatGPT vs. GitHub Copilot Comparison Macros ===",
        f"\\newcommand{{\\cgCopilotPearsonR}}{{{float(r_val):.2f}}}",
        f"\\newcommand{{\\copilotPredAtEightyFive}}{{{pred_at_85:.2f}}}",
        f"\\newcommand{{\\cgCopilotReadMaeDeltaRelPct}}{{{read_rel_pct:+.2f}\\%}}",
        f"\\newcommand{{\\cgCopilotUndMaeDeltaRelPct}}{{{und_rel_pct:+.2f}\\%}}",
        f"\\newcommand{{\\cgCopilotMaintMaeDeltaRelPct}}{{{maint_rel_pct:+.2f}\\%}}",
        f"\\newcommand{{\\cgCopilotSecAccDeltaPp}}{{{sec_acc_pp:+.2f}~\\text{{pp}}}}",
        f"\\newcommand{{\\cgCopilotSecPrecDeltaPp}}{{{prec_pp:+.2f}~\\text{{pp}}}}",
        f"\\newcommand{{\\cgCopilotSecRecDeltaPp}}{{{rec_pp:+.2f}~\\text{{pp}}}}",
    ]

    for _, r in comp_df.iterrows():
        prefix = "cg" if r["Model"] == "ChatGPT" else "copilot"
        macro_lines.append(f"\\newcommand{{\\{prefix}CompReadMae}}{{{float(r['Read_MAE']):.2f}}}")
        macro_lines.append(f"\\newcommand{{\\{prefix}CompUndMae}}{{{float(r['Und_MAE']):.2f}}}")
        macro_lines.append(f"\\newcommand{{\\{prefix}CompMaintMae}}{{{float(r['Maint_MAE']):.2f}}}")
        macro_lines.append(f"\\newcommand{{\\{prefix}CompOverallMae}}{{{float(r['Overall_MAE']):.2f}}}")
        macro_lines.append(f"\\newcommand{{\\{prefix}CompSecAccPct}}{{{float(r['Sec_Acc_pct']):.2f}}}")
        macro_lines.append(f"\\newcommand{{\\{prefix}CompSecPrecPct}}{{{float(r['Sec_Prec_pct']):.2f}}}")
        macro_lines.append(f"\\newcommand{{\\{prefix}CompSecRecPct}}{{{float(r['Sec_Rec_pct']):.2f}}}")
        macro_lines.append(f"\\newcommand{{\\{prefix}CompSecFp}}{{{int(r['Sec_FP'])}}}")

    if os.path.exists(tex_out_path):
        with open(tex_out_path, "r", encoding="utf-8") as f:
            existing = f.read()
        marker = "% === ChatGPT vs. GitHub Copilot Comparison Macros ==="
        if marker in existing:
            existing = existing.split(marker)[0].rstrip() + "\n"
        with open(tex_out_path, "w", encoding="utf-8") as f:
            f.write(existing + "\n".join(macro_lines).strip() + "\n")
        print(f" - Updated {tex_out_path} with ChatGPT vs. Copilot macros")

    return comp_df

def export_conclusion_metrics_and_macros(
    df: pd.DataFrame,
    output_dir: str = ".",
    tex_out_path: str = "./thesis_metrics_macros.tex",
) -> pd.DataFrame:
    """
    Exports per-model Overall MAE and Maintainability Spearman correlation vs. GT
    to CSV and appends LaTeX macros to thesis_metrics_macros.tex.
    """
    os.makedirs(output_dir, exist_ok=True)
    piv_m = df.pivot(index="snippet_id", columns="model", values="maintainability")
    gt_m = df.groupby("snippet_id")["gt_maint"].first()
    piv_m["GT"] = gt_m
    spearman_map = piv_m.corr(method="spearman")["GT"].to_dict()

    mae_map = df.groupby("model")["overall_err"].mean().to_dict()

    rows = []
    for m in ["ChatGPT", "Claude", "Gemini", "GithubCopilot", "Sonarqube"]:
        rows.append({
            "Model": m,
            "Overall_MAE": round(float(mae_map.get(m, np.nan)), 2),
            "Maint_Spearman_vs_GT": round(float(spearman_map.get(m, np.nan)), 3),
        })

    conc_df = pd.DataFrame(rows)
    csv_path = os.path.join(output_dir, "conclusion_summary_metrics.csv")
    conc_df.to_csv(csv_path, index=False)
    print(f" - {csv_path}")

    ai_corrs = [float(spearman_map[m]) for m in ["ChatGPT", "Claude", "Gemini", "GithubCopilot"] if m in spearman_map]
    min_ai_rho = min(ai_corrs) if ai_corrs else np.nan
    max_ai_rho = max(ai_corrs) if ai_corrs else np.nan

    macro_lines = [
        "",
        "% === Conclusion Summary Macros ===",
        f"\\newcommand{{\\aiMinMaintSpearman}}{{{min_ai_rho:.3f}}}",
        f"\\newcommand{{\\aiMaxMaintSpearman}}{{{max_ai_rho:.3f}}}",
    ]
    for _, r in conc_df.iterrows():
        m = str(r["Model"])
        m_camel = m[0].lower() + m[1:]
        macro_lines.append(f"\\newcommand{{\\{m_camel}OverallMae}}{{{float(r['Overall_MAE']):.2f}}}")
        macro_lines.append(f"\\newcommand{{\\{m_camel}MaintSpearman}}{{{float(r['Maint_Spearman_vs_GT']):.3f}}}")

    if os.path.exists(tex_out_path):
        with open(tex_out_path, "r", encoding="utf-8") as f:
            existing = f.read()
        marker = "% === Conclusion Summary Macros ==="
        if marker in existing:
            existing = existing.split(marker)[0].rstrip() + "\n"
        with open(tex_out_path, "w", encoding="utf-8") as f:
            f.write(existing + "\n".join(macro_lines).strip() + "\n")
        print(f" - Updated {tex_out_path} with conclusion macros")

    return conc_df


def _cronbach_alpha(df_items: pd.DataFrame) -> float:
    df_clean = df_items.dropna()
    k = df_clean.shape[1]
    if k <= 1 or len(df_clean) < 2:
        return np.nan
    item_vars = df_clean.var(axis=0, ddof=1)
    total_var = df_clean.sum(axis=1).var(axis=0, ddof=1)
    if total_var == 0:
        return np.nan
    return float((k / (k - 1.0)) * (1.0 - item_vars.sum() / total_var))


def _icc_3_1(df_items: pd.DataFrame) -> float:
    """Two-way mixed, consistency, single-rater ICC(3,1) (Shrout & Fleiss, 1979)."""
    df_clean = df_items.dropna()
    n, k = df_clean.shape
    if n < 2 or k < 2:
        return np.nan
    grand_mean = df_clean.values.mean()
    row_means = df_clean.mean(axis=1).values
    col_means = df_clean.mean(axis=0).values

    ss_total = ((df_clean.values - grand_mean) ** 2).sum()
    ss_rows = k * ((row_means - grand_mean) ** 2).sum()
    ss_cols = n * ((col_means - grand_mean) ** 2).sum()
    ss_err = ss_total - ss_rows - ss_cols

    ms_rows = ss_rows / (n - 1)
    ms_err = ss_err / ((n - 1) * (k - 1))
    denom = ms_rows + (k - 1) * ms_err
    return float((ms_rows - ms_err) / denom) if denom != 0 else np.nan


def _mean_pairwise_spearman(df_items: pd.DataFrame) -> float:
    df_clean = df_items.dropna()
    cols = list(df_clean.columns)
    rhos = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            r, _ = stats.spearmanr(df_clean[cols[i]], df_clean[cols[j]])
            if pd.notna(r):
                rhos.append(float(r))
    return float(np.mean(rhos)) if rhos else np.nan


def _loo_mae(df_items: pd.DataFrame) -> float:
    """Leave-One-Expert-Out MAE: each expert k vs. mean of the other two experts."""
    df_clean = df_items.dropna()
    cols = list(df_clean.columns)
    k = len(cols)
    if k < 2 or len(df_clean) == 0:
        return np.nan
    expert_maes = []
    for idx_k, col_k in enumerate(cols):
        other_cols = [c for j, c in enumerate(cols) if j != idx_k]
        other_mean = df_clean[other_cols].mean(axis=1)
        expert_maes.append(float((df_clean[col_k] - other_mean).abs().mean()))
    return float(np.mean(expert_maes))


def export_human_reliability_and_macros(
    raw_json_path: str = "Results.json",
    output_dir: str = "./output_charts",
    tex_out_path: str = "./output_charts/thesis_metrics_macros.tex",
) -> pd.DataFrame:
    """
    Computes inter-rater reliability (Cronbach's alpha, ICC(3,1), mean pairwise Spearman rho)
    and Leave-One-Expert-Out MAE across Human1, Human2, Human3, saves CSV, and appends
    LaTeX macros to thesis_metrics_macros.tex.
    """
    if not os.path.exists(raw_json_path) and os.path.exists("Results.txt"):
        raw_json_path = "Results.txt"
    with open(raw_json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    experts = ["Human1", "Human2", "Human3"]
    dims = ["readability_score", "understandability_score", "maintainability_score"]
    data_by_dim = {d: {h: [] for h in experts} for d in dims}

    for _, item in raw_data.items():
        for d in dims:
            for h in experts:
                val = pd.to_numeric(item.get(h, {}).get(d), errors="coerce")
                data_by_dim[d][h].append(val)

    # Snippet-level overall quality (mean of 3 dimensions per expert per snippet)
    n_items = len(data_by_dim["readability_score"][experts[0]])
    snip_overall = {
        h: [float(np.mean([data_by_dim[d][h][i] for d in dims])) for i in range(n_items)]
        for h in experts
    }

    entries = [
        ("Readability", "Readability", pd.DataFrame(data_by_dim["readability_score"])),
        ("Understandability", "Understandability", pd.DataFrame(data_by_dim["understandability_score"])),
        ("Maintainability", "Maintainability", pd.DataFrame(data_by_dim["maintainability_score"])),
        ("OverallQuality", "Overall Quality Score", pd.DataFrame(snip_overall)),
    ]

    rows = []
    macro_lines = ["", "% === Human Inter-Rater Reliability & Leave-One-Out Ceiling Macros ==="]

    for tag, label, df_dim in entries:
        alpha_val = _cronbach_alpha(df_dim)
        icc_val = _icc_3_1(df_dim)
        rho_val = _mean_pairwise_spearman(df_dim)
        loo_val = _loo_mae(df_dim)

        rows.append({
            "Dimension": label,
            "N_Snippets": int(len(df_dim.dropna())),
            "Cronbach_Alpha": round(alpha_val, 3),
            "ICC_3_1": round(icc_val, 3),
            "Mean_Pairwise_Spearman_Rho": round(rho_val, 3),
            "LOO_MAE": round(loo_val, 2),
        })

        macro_lines.append(f"\\newcommand{{\\human{tag}Alpha}}{{{alpha_val:.3f}}}")
        macro_lines.append(f"\\newcommand{{\\human{tag}Icc}}{{{icc_val:.3f}}}")
        macro_lines.append(f"\\newcommand{{\\human{tag}Rho}}{{{rho_val:.3f}}}")
        macro_lines.append(f"\\newcommand{{\\human{tag}LooMae}}{{{loo_val:.2f}}}")

    os.makedirs(output_dir, exist_ok=True)
    out_csv = os.path.join(output_dir, "human_reliability_ceiling.csv")
    res_df = pd.DataFrame(rows)
    res_df.to_csv(out_csv, index=False)
    print(f" - {out_csv}")

    if os.path.exists(tex_out_path):
        with open(tex_out_path, "r", encoding="utf-8") as f:
            existing = f.read()
        marker = "% === Human Inter-Rater Reliability & Leave-One-Out Ceiling Macros ==="
        if marker in existing:
            existing = existing.split(marker)[0].rstrip() + "\n"
        with open(tex_out_path, "w", encoding="utf-8") as f:
            f.write(existing + "\n".join(macro_lines).strip() + "\n")
        print(f" - Updated {tex_out_path} with human reliability macros")

    return res_df


def _bootstrap_ci_mean(values, n_boot: int = 2000, seed: int = 42):
    arr = np.asarray(values, dtype=float)
    arr = arr[~np.isnan(arr)]
    if len(arr) == 0:
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(arr), size=(n_boot, len(arr)))
    boot_means = arr[idx].mean(axis=1)
    return float(np.percentile(boot_means, 2.5)), float(np.percentile(boot_means, 97.5))


def export_baselines_calibration_and_stats(
    raw_json_path: str = "Results.json",
    output_dir: str = "./output_charts",
    tex_out_path: str = "./output_charts/thesis_metrics_macros.tex",
) -> pd.DataFrame:
    """
    Computes naive/human reference baselines, bias decomposition, calibrated MAE,
    Spearman rank correlation, 95% bootstrap CIs, and Wilcoxon signed-rank tests
    vs. ChatGPT. Exports CSV and appends LaTeX macros to thesis_metrics_macros.tex.
    """
    if not os.path.exists(raw_json_path) and os.path.exists("Results.txt"):
        raw_json_path = "Results.txt"
    with open(raw_json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    dims = ["readability_score", "understandability_score", "maintainability_score"]
    experts = ["Human1", "Human2", "Human3"]
    models = ["ChatGPT", "Claude", "Gemini", "GithubCopilot", "Sonarqube"]

    gt_ov_list = []
    sec_gt_list = []
    human_ov_by_exp = {h: [] for h in experts}
    model_records = []

    for snip_id, item in raw_data.items():
        meta = item.get("metadata", {})
        gt_ov = float(np.mean([pd.to_numeric(meta.get(d), errors="coerce") for d in dims]))
        gt_ov_list.append(gt_ov)
        sec_gt_list.append(meta.get("security_classification"))

        for h in experts:
            hd = item.get(h, {})
            human_ov_by_exp[h].append(
                float(np.mean([pd.to_numeric(hd.get(d), errors="coerce") for d in dims]))
            )

        for m in models:
            md = item.get(m, {})
            m_ov = float(np.mean([pd.to_numeric(md.get(d), errors="coerce") for d in dims]))
            model_records.append({
                "snippet_id": snip_id,
                "model": m,
                "gt_ov": gt_ov,
                "m_ov": m_ov,
                "abs_err": abs(m_ov - gt_ov),
                "signed_err": m_ov - gt_ov,
            })

    mdf = pd.DataFrame(model_records)
    gt_arr = np.array(gt_ov_list, dtype=float)
    gt_mean = float(np.mean(gt_arr))

    # Naive mean baseline
    naive_errs = np.abs(gt_arr - gt_mean)
    naive_mae = float(np.mean(naive_errs))
    naive_ci_lo, naive_ci_hi = _bootstrap_ci_mean(naive_errs, seed=101)

    # Majority security baseline
    sec_series = pd.Series(sec_gt_list).dropna()
    majority_pct = float(sec_series.value_counts().max() / len(sec_series) * 100.0) if len(sec_series) > 0 else np.nan

    # Human LOO baseline & mean pairwise Spearman on snippet overall quality
    h_df = pd.DataFrame(human_ov_by_exp)
    loo_per_exp = []
    snip_loo_cols = []
    for col_k in experts:
        other_cols = [c for c in experts if c != col_k]
        diff_k = np.abs(h_df[col_k] - h_df[other_cols].mean(axis=1))
        loo_per_exp.append(float(diff_k.mean()))
        snip_loo_cols.append(diff_k.values)
    human_loo_mae = float(np.mean(loo_per_exp))
    human_loo_ci_lo, human_loo_ci_hi = _bootstrap_ci_mean(np.mean(snip_loo_cols, axis=0), seed=102)

    rhos = []
    for i in range(len(experts)):
        for j in range(i + 1, len(experts)):
            r_ij, _ = stats.spearmanr(h_df[experts[i]], h_df[experts[j]])
            rhos.append(float(r_ij))
    human_mean_rho = float(np.mean(rhos))

    table_rows = [
        {
            "System": "NaiveMeanBaseline",
            "Raw_MAE": round(naive_mae, 2),
            "CI_Low": round(naive_ci_lo, 2),
            "CI_High": round(naive_ci_hi, 2),
            "Mean_Bias": 0.0,
            "Bias_Label": "Zero",
            "Calibrated_MAE": round(naive_mae, 2),
            "Spearman_Rho": 0.0,
        },
        {
            "System": "HumanReferenceBaseline",
            "Raw_MAE": round(human_loo_mae, 2),
            "CI_Low": round(human_loo_ci_lo, 2),
            "CI_High": round(human_loo_ci_hi, 2),
            "Mean_Bias": 0.0,
            "Bias_Label": "Zero",
            "Calibrated_MAE": round(human_loo_mae, 2),
            "Spearman_Rho": round(human_mean_rho, 3),
        },
    ]

    macro_lines = [
        "",
        "% === Baseline Comparisons, Calibration & Significance Macros ===",
        f"\\newcommand{{\\datasetOverallQualityMean}}{{{gt_mean:.2f}}}",
        f"\\newcommand{{\\majoritySecurityBaselinePct}}{{{majority_pct:.2f}\\%}}",
        f"\\newcommand{{\\naiveMeanBaselineMae}}{{{naive_mae:.2f}}}",
        f"\\newcommand{{\\naiveMeanBaselineCiLow}}{{{naive_ci_lo:.2f}}}",
        f"\\newcommand{{\\naiveMeanBaselineCiHigh}}{{{naive_ci_hi:.2f}}}",
        f"\\newcommand{{\\humanRefBaselineMae}}{{{human_loo_mae:.2f}}}",
        f"\\newcommand{{\\humanRefBaselineCiLow}}{{{human_loo_ci_lo:.2f}}}",
        f"\\newcommand{{\\humanRefBaselineCiHigh}}{{{human_loo_ci_hi:.2f}}}",
        f"\\newcommand{{\\humanRefBaselineRho}}{{{human_mean_rho:.3f}}}",
    ]

    for idx_m, m in enumerate(models):
        sub = mdf[mdf["model"] == m]
        raw_mae = float(sub["abs_err"].mean())
        ci_lo, ci_hi = _bootstrap_ci_mean(sub["abs_err"], seed=200 + idx_m)
        mean_bias = float(sub["signed_err"].mean())
        cal_mae = float(np.abs(sub["m_ov"] - mean_bias - sub["gt_ov"]).mean())
        rho_m, _ = stats.spearmanr(sub["m_ov"], sub["gt_ov"])
        rho_m = float(rho_m)

        if abs(mean_bias) < 1.0:
            bias_lbl = "Neutral"
        elif mean_bias >= 8.0:
            bias_lbl = "High Optimistic"
        elif mean_bias > 0:
            bias_lbl = "Optimistic"
        elif mean_bias <= -10.0:
            bias_lbl = "Strong Pessimistic"
        else:
            bias_lbl = "Pessimistic"

        table_rows.append({
            "System": m,
            "Raw_MAE": round(raw_mae, 2),
            "CI_Low": round(ci_lo, 2),
            "CI_High": round(ci_hi, 2),
            "Mean_Bias": round(mean_bias, 2),
            "Bias_Label": bias_lbl,
            "Calibrated_MAE": round(cal_mae, 2),
            "Spearman_Rho": round(rho_m, 3),
        })

        prefix = m[0].lower() + m[1:]
        macro_lines.extend([
            f"\\newcommand{{\\{prefix}CalRawMae}}{{{raw_mae:.2f}}}",
            f"\\newcommand{{\\{prefix}CalCiLow}}{{{ci_lo:.2f}}}",
            f"\\newcommand{{\\{prefix}CalCiHigh}}{{{ci_hi:.2f}}}",
            f"\\newcommand{{\\{prefix}CalMeanBias}}{{{mean_bias:+.2f}}}",
            f"\\newcommand{{\\{prefix}CalBiasLabel}}{{{bias_lbl}}}",
            f"\\newcommand{{\\{prefix}CalAdjustedMae}}{{{cal_mae:.2f}}}",
            f"\\newcommand{{\\{prefix}CalSpearmanRho}}{{{rho_m:.3f}}}",
        ])

    # Pairwise Wilcoxon tests vs. ChatGPT on absolute error
    cg_err = mdf[mdf["model"] == "ChatGPT"].set_index("snippet_id")["abs_err"]
    for other_m in ["Claude", "GithubCopilot", "Sonarqube", "Gemini"]:
        other_err = mdf[mdf["model"] == other_m].set_index("snippet_id")["abs_err"]
        w_stat, p_val = stats.wilcoxon(cg_err, other_err)
        cohen_d = abs(float((cg_err.mean() - other_err.mean()) / np.sqrt((cg_err.var(ddof=1) + other_err.var(ddof=1)) / 2.0)))
        tag = other_m[0].upper() + other_m[1:]
        p_str = "< 0.001" if p_val < 0.001 else f"= {float(p_val):.3f}"
        macro_lines.extend([
            f"\\newcommand{{\\cgVs{tag}WilcoxonW}}{{{float(w_stat):.1f}}}",
            f"\\newcommand{{\\cgVs{tag}WilcoxonP}}{{{p_str}}}",
            f"\\newcommand{{\\cgVs{tag}EffectD}}{{{cohen_d:.3f}}}",
        ])

    out_df = pd.DataFrame(table_rows)
    csv_path = os.path.join(output_dir, "baseline_calibration_significance.csv")
    out_df.to_csv(csv_path, index=False)
    print(f" - {csv_path}")

    if os.path.exists(tex_out_path):
        with open(tex_out_path, "r", encoding="utf-8") as f:
            existing = f.read()
        marker = "% === Baseline Comparisons, Calibration & Significance Macros ==="
        if marker in existing:
            existing = existing.split(marker)[0].rstrip() + "\n"
        with open(tex_out_path, "w", encoding="utf-8") as f:
            f.write(existing + "\n".join(macro_lines).strip() + "\n")
        print(f" - Updated {tex_out_path} with baseline & calibration macros")

    return out_df


CWE_CATEGORY_MAPPING = {
    "MemoryAndPointerSafety": {
        "label": "Memory \\& Pointer Safety",
        "codes": {
            "CWE-119", "CWE-120", "CWE-121", "CWE-125", "CWE-129",
            "CWE-401", "CWE-415", "CWE-416", "CWE-476", "CWE-787", "CWE-789", "CWE-824",
        },
    },
    "InputValidationAndInjection": {
        "label": "Input Validation \\& Injection",
        "codes": {
            "CWE-20", "CWE-22", "CWE-73", "CWE-89", "CWE-94", "CWE-183", "CWE-470",
        },
    },
    "EncapsulationLogicAndResources": {
        "label": "Encapsulation, Logic \\& Resources",
        "codes": {
            "CWE-190", "CWE-200", "CWE-367", "CWE-369", "CWE-374", "CWE-375",
            "CWE-400", "CWE-404", "CWE-495", "CWE-595", "CWE-597", "CWE-617",
            "CWE-672", "CWE-703", "CWE-704", "CWE-798", "CWE-835",
        },
    },
}

def _pred_is_vulnerable(model, item_model):
    sc = str(item_model.get("security_classification", "")).strip().lower()
    if model.lower() == "sonarqube":
        try:
            return float(sc) < 100.0
        except ValueError:
            return sc == "vulnerable"
    return sc == "vulnerable"

def export_cwe_category_recall_and_macros(
    raw_json_path: str = "Results.json",
    output_dir: str = "./output_charts",
    tex_out_path: str = "./output_charts/thesis_metrics_macros.tex",
) -> pd.DataFrame:
    """
    Maps snippet CWE IDs into MITRE-informed functional/security groups, computes
    per-group vulnerability recall across all evaluated models, saves CSV, and
    appends alphabetic CamelCase LaTeX macros to thesis_metrics_macros.tex.
    """
    if not os.path.exists(raw_json_path) and os.path.exists("Results.txt"):
        raw_json_path = "Results.txt"
    with open(raw_json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    models = ["ChatGPT", "Claude", "Gemini", "GithubCopilot", "Sonarqube"]

    vuln_items = []
    for snip_id, item in raw_data.items():
        meta = item.get("metadata", {})
        if str(meta.get("security_classification", "")).strip().lower() == "vulnerable":
            codes = [
                c.upper()
                for c in re.findall(r"CWE-\d+", str(meta.get("cwe_id", "")), flags=re.IGNORECASE)
            ]
            vuln_items.append((snip_id, item, codes))

    rows = []
    macro_lines = ["", "% === CWE Category Vulnerability Recall Macros ==="]

    for cat_key, cat_info in CWE_CATEGORY_MAPPING.items():
        code_set = cat_info["codes"]
        matching = [(sid, it) for sid, it, codes in vuln_items if any(c in code_set for c in codes)]
        n_cat = len(matching)

        row = {"Category_Key": cat_key, "Category_Label": cat_info["label"], "N_Snippets": n_cat}
        macro_lines.append(f"\\newcommand{{\\cwe{cat_key}Count}}{{{n_cat}}}")

        for m in models:
            tp_m = sum(1 for _, it in matching if _pred_is_vulnerable(m, it.get(m, {})))
            rec_m = (tp_m / n_cat * 100.0) if n_cat > 0 else 0.0
            row[f"{m}_Recall_pct"] = round(rec_m, 1)
            prefix = m[0].lower() + m[1:]
            macro_lines.append(f"\\newcommand{{\\cwe{cat_key}{prefix[0].upper() + prefix[1:]}RecallPct}}{{{rec_m:.1f}\\%}}")

        rows.append(row)

    cwe_df = pd.DataFrame(rows)
    csv_path = os.path.join(output_dir, "cwe_category_recall.csv")
    cwe_df.to_csv(csv_path, index=False)
    print(f" - {csv_path}")

    if os.path.exists(tex_out_path):
        with open(tex_out_path, "r", encoding="utf-8") as f:
            existing = f.read()
        marker = "% === CWE Category Vulnerability Recall Macros ==="
        if marker in existing:
            existing = existing.split(marker)[0].rstrip() + "\n"
        with open(tex_out_path, "w", encoding="utf-8") as f:
            f.write(existing + "\n".join(macro_lines).strip() + "\n")
        print(f" - Updated {tex_out_path} with CWE category macros")

    return cwe_df

def generate_latex_macros(
    df: pd.DataFrame,
    overall_df: pd.DataFrame,
    by_lang_df: pd.DataFrame,
    macro_lang_df: pd.DataFrame,
    cwe_table_counts: dict[str, int] | None = None,
    cwe_table_recalls: dict[str, dict[str, float]] | None = None,
    output_path: str = "./output_charts/thesis_macros.tex",
) -> str:
    """
    Generates a LaTeX macro file directly from computed DataFrames and Results.json data.
    Uses \\providecommand so re-running safely overwrites or updates definitions cleanly.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    macros: list[str] = ["% Auto-generated LaTeX macros from evaluation results. Do not edit manually."]

    def add_macro(name: str, val: str) -> None:
        macros.append(f"\\providecommand{{\\{name}}}{{}}\\renewcommand{{\\{name}}}{{{val}}}")

    # Dataset & class distribution
    n_total = int(df["snippet_id"].nunique())
    gt_sec_per_snip = df.groupby("snippet_id")["gt_is_vulnerable"].first()
    n_vuln = int(gt_sec_per_snip.sum())
    n_safe = int(n_total - n_vuln)
    safe_pct = n_safe / n_total * 100.0
    vuln_pct = n_vuln / n_total * 100.0

    add_macro("TotalSnippets", f"{n_total}")
    add_macro("SafeCount", f"{n_safe}")
    add_macro("VulnCount", f"{n_vuln}")
    add_macro("SafePct", f"{safe_pct:.2f}")
    add_macro("VulnPct", f"{vuln_pct:.2f}")

    # Per-language MAE & classification metrics
    lang_map = {"java": "Java", "cpp": "Cpp", "python": "Python"}
    model_map = {
        "ChatGPT": "ChatGPT",
        "Claude": "Claude",
        "Gemini": "Gemini",
        "GithubCopilot": "Copilot",
        "Sonarqube": "Sonar",
    }

    mae_by_lang_model = df.groupby(["language", "model"])["overall_err"].mean()
    for lang_key, lang_tag in lang_map.items():
        n_lang = int(df[df["language"] == lang_key]["snippet_id"].nunique())
        add_macro(f"LangCount{lang_tag}", f"{n_lang}")

        for m_key, m_tag in model_map.items():
            mae_val = mae_by_lang_model.loc[(lang_key, m_key)]
            add_macro(f"Mae{lang_tag}{m_tag}", f"{mae_val:.2f}")

            sub_l = by_lang_df[(by_lang_df["Language"] == lang_key) & (by_lang_df["Model"] == m_key)]
            if not sub_l.empty:
                r = sub_l.iloc[0]
                acc_v = 0.0 if pd.isna(r["Sec_Acc_pct"]) else float(r["Sec_Acc_pct"])
                prec_v = 0.0 if pd.isna(r["Sec_Prec_pct"]) else float(r["Sec_Prec_pct"])
                rec_v = 0.0 if pd.isna(r["Sec_Rec_pct"]) else float(r["Sec_Rec_pct"])
                f1_v = 0.0 if pd.isna(r["Sec_F1_pct"]) else float(r["Sec_F1_pct"])

                add_macro(f"SecAcc{lang_tag}{m_tag}", f"{acc_v:.1f}")
                add_macro(f"SecPrec{lang_tag}{m_tag}", f"{prec_v:.1f}")
                add_macro(f"SecRec{lang_tag}{m_tag}", f"{rec_v:.1f}")
                add_macro(f"SecFOne{lang_tag}{m_tag}", f"{f1_v:.1f}")

    # Macro recall across languages
    macro_indexed = macro_lang_df.set_index("Model")
    for m_key, m_tag in model_map.items():
        if m_key in macro_indexed.index:
            m_sec_rec = float(macro_indexed.loc[m_key, "MacroLang_Sec_Rec_pct"])
            add_macro(f"MacroLangSecRec{m_tag}", f"{m_sec_rec:.1f}")

    # Overall classification, confusion matrices & functional/combined recall
    ov_indexed = overall_df.set_index("Model")
    for m_key, m_tag in model_map.items():
        if m_key in ov_indexed.index:
            row = ov_indexed.loc[m_key]
            add_macro(f"SecTP{m_tag}", f"{int(row['Sec_TP'])}")
            add_macro(f"SecFP{m_tag}", f"{int(row['Sec_FP'])}")
            add_macro(f"SecTN{m_tag}", f"{int(row['Sec_TN'])}")
            add_macro(f"SecFN{m_tag}", f"{int(row['Sec_FN'])}")
            add_macro(f"SecAccOverall{m_tag}", f"{float(row['Sec_Acc_pct']):.1f}")
            add_macro(f"FuncBugFOne{m_tag}", f"{float(row['FuncBug_F1_pct']):.1f}")
            add_macro(f"FuncAnyAcc{m_tag}", f"{float(row['FuncAny_Acc_pct']):.1f}")
            add_macro(f"FuncAnyPrec{m_tag}", f"{float(row['FuncAny_Prec_pct']):.1f}")
            add_macro(f"FuncAnyRec{m_tag}", f"{float(row['FuncAny_Rec_pct']):.1f}")
            add_macro(f"FuncAnyFOne{m_tag}", f"{float(row['FuncAny_F1_pct']):.1f}")
            add_macro(f"MacroRecSecBug{m_tag}", f"{float(row['MacroRec_Sec_FuncBug_pct']):.1f}")
            add_macro(f"PooledRecSecBug{m_tag}", f"{float(row['PooledRec_Sec_FuncBug_pct']):.1f}")

    # Cognitive complexity strata (Low 0-3, Medium 4-8, High 9+)
    comp_series = pd.cut(
        df["cognitive_complexity"],
        bins=[-1, 3, 8, 100],
        labels=["Low", "Medium", "High"],
    )
    df_comp = df.assign(comp_bucket=comp_series)
    bucket_counts = df_comp[df_comp["model"] == "ChatGPT"]["comp_bucket"].value_counts()
    mae_bucket = df_comp.groupby(["comp_bucket", "model"], observed=False)["overall_err"].mean()
    sec_acc_bucket = df_comp.groupby(["comp_bucket", "model"], observed=False)["sec_correct"].mean() * 100.0

    for b_name in ["Low", "Medium", "High"]:
        add_macro(f"CompCount{b_name}", f"{int(bucket_counts.get(b_name, 0))}")
        for m_key, m_tag in model_map.items():
            add_macro(f"CompMae{b_name}{m_tag}", f"{float(mae_bucket.loc[(b_name, m_key)]):.2f}")
            add_macro(f"CompSecAcc{b_name}{m_tag}", f"{float(sec_acc_bucket.loc[(b_name, m_key)]):.1f}")

    # Optional CWE table counts & recalls if passed from your CWE grouping logic
    if cwe_table_counts:
        for cat_tag, cnt in cwe_table_counts.items():
            add_macro(f"CweCount{cat_tag}", f"{int(cnt)}")
    if cwe_table_recalls:
        for cat_tag, m_dict in cwe_table_recalls.items():
            for m_key, m_tag in model_map.items():
                if m_key in m_dict:
                    add_macro(f"CweRec{cat_tag}{m_tag}", f"{float(m_dict[m_key]):.1f}")

    marker = macros[0]
    existing = ""
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            existing = f.read()
        if marker in existing:
            existing = existing.split(marker)[0].rstrip() + "\n"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(existing + "\n".join(macros) + "\n")

    print(f"LaTeX macros written to: {output_path}")
    return output_path

def append_advanced_security_macros(
    overall_df: pd.DataFrame,
    output_path: str = "./thesis_macros.tex",
) -> None:
    """
    Computes Balanced Accuracy, MCC and Cohen's kappa from the overall security
    confusion counts and appends \\SecBalAccX, \\SecMCCX, \\SecKappaX macros.
    Must run AFTER generate_latex_macros (which rewrites the file from scratch).
    """
    model_map = {
        "ChatGPT": "ChatGPT",
        "Claude": "Claude",
        "Gemini": "Gemini",
        "GithubCopilot": "Copilot",
        "Sonarqube": "Sonar",
    }
    lines = ["", "% === Advanced Security Metrics (Balanced Acc., MCC, Cohen's kappa) ==="]

    def add(name, val):
        lines.append(f"\\providecommand{{\\{name}}}{{}}\\renewcommand{{\\{name}}}{{{val}}}")

    for _, r in overall_df.iterrows():
        tag = model_map.get(r["Model"])
        if tag is None:
            continue
        tp, fp, tn, fn = (float(r[c]) for c in ("Sec_TP", "Sec_FP", "Sec_TN", "Sec_FN"))
        n = tp + fp + tn + fn

        tpr = tp / (tp + fn) if (tp + fn) > 0 else np.nan
        tnr = tn / (tn + fp) if (tn + fp) > 0 else np.nan
        bal_acc = (tpr + tnr) / 2.0 * 100.0

        denom = np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
        mcc = (tp * tn - fp * fn) / denom if denom > 0 else 0.0

        p_o = (tp + tn) / n
        p_e = ((tp + fp) * (tp + fn) + (fn + tn) * (fp + tn)) / (n ** 2)
        kappa = (p_o - p_e) / (1.0 - p_e) if p_e < 1.0 else np.nan

        add(f"SecBalAcc{tag}", f"{bal_acc:.1f}")
        add(f"SecMCC{tag}", f"{mcc:.3f}")
        add(f"SecKappa{tag}", f"{kappa:.3f}")

    with open(output_path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Advanced security macros appended to: {output_path}")


def export_extra_macros(raw_json_path="Results.json",
                        tex_out_path="./metrics_macros.tex",
                        csv_out_path="./extra_metrics_summary.csv"):
    with open(raw_json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    models = ["ChatGPT", "Claude", "Gemini", "GithubCopilot", "Sonarqube"]
    llms = models[:4]
    dims = {"Read": "readability_score", "Und": "understandability_score", "Maint": "maintainability_score"}
    langs = {"cpp": "Cpp", "java": "Java", "python": "Python"}
    func_map = {"correct": "Correct", "partially correct": "Partial", "buggy": "Buggy"}
    tag = lambda m: m[0].lower() + m[1:]
    cwes = lambda x: set(c.upper() for c in re.findall(r"CWE-\d+", str(x), flags=re.IGNORECASE))

    rows = []
    for sid, item in raw.items():
        meta = item.get("metadata", {})
        r = {"sid": sid, "lang": str(meta.get("language", "")).strip().lower(),
             "gt_func": str(meta.get("functional_classification", "")).strip().lower(),
             "gt_vuln": str(meta.get("security_classification", "")).strip().lower() == "vulnerable",
             "gt_cwe": cwes(meta.get("cwe_id", ""))}
        for d, key in dims.items():
            r[f"gt_{d}"] = pd.to_numeric(meta.get(key), errors="coerce")
        r["gt_Overall"] = float(np.mean([r[f"gt_{d}"] for d in dims]))
        for m in models:
            md = item.get(m, {})
            for d, key in dims.items():
                r[f"{m}_{d}"] = pd.to_numeric(md.get(key), errors="coerce")
            r[f"{m}_Overall"] = float(np.mean([r[f"{m}_{d}"] for d in dims]))
            r[f"{m}_func"] = str(md.get("functional_classification", "")).strip().lower()
            r[f"{m}_cwe"] = cwes(md.get("cwe_id", ""))
        rows.append(r)
    d = pd.DataFrame(rows)
    unknown = set(d["lang"]) - set(langs)
    if unknown:
        print(f"WARNING: unmapped language values {unknown}")

    out = {}
    for D in list(dims) + ["Overall"]:                       # 1. ground truth stats
        out[f"gtMean{D}"] = f"{d[f'gt_{D}'].mean():.2f}"
        out[f"gtSd{D}"] = f"{d[f'gt_{D}'].std(ddof=1):.2f}"

    for m in models:                                          # 2. MAE, signed bias, means, delta
        t = tag(m)
        for D in dims:
            err = d[f"{m}_{D}"] - d[f"gt_{D}"]
            out[f"{t}Mae{D}"] = f"{err.abs().mean():.2f}"
            out[f"{t}Bias{D}"] = f"{err.mean():+.2f}"
            out[f"{t}Mean{D}"] = f"{d[f'{m}_{D}'].mean():.2f}"
        per_lang = {D: [] for D in list(dims) + ["Overall"]}
        for lk, L in langs.items():
            sub = d[d["lang"] == lk]
            for D in list(dims) + ["Overall"]:
                mae = (sub[f"{m}_{D}"] - sub[f"gt_{D}"]).abs().mean()
                per_lang[D].append(mae)
                if D != "Overall":
                    out[f"{t}{L}Mae{D}"] = f"{mae:.2f}"
        for D, vals in per_lang.items():
            out[f"{t}DeltaMaeLang{D}"] = f"{max(vals) - min(vals):.2f}"

    for lab, name in func_map.items():                        # 3. functional, 3 classes
        n = int((d["gt_func"] == lab).sum())
        out[f"gtFunc{name}Count"] = str(n)
        out[f"gtFunc{name}Pct"] = f"{n / len(d) * 100:.1f}\\%"
    bad_gt = set(d["gt_func"]) - set(func_map)
    if bad_gt:
        print(f"WARNING: unexpected ground-truth functional labels {bad_gt}")
    for m in llms:
        t = tag(m)
        bad = set(d[f"{m}_func"]) - set(func_map)
        if bad:
            print(f"WARNING: {m} has unexpected functional labels {bad} (counted as wrong)")
        ok = d[f"{m}_func"] == d["gt_func"]
        out[f"{t}FuncAccPct"] = f"{ok.mean() * 100:.2f}\\%"
        for lab, name in func_map.items():
            out[f"{t}FuncRec{name}Pct"] = f"{ok[d['gt_func'] == lab].mean() * 100:.1f}\\%"
        for lk, L in langs.items():
            out[f"{t}{L}FuncAccPct"] = f"{ok[d['lang'] == lk].mean() * 100:.1f}\\%"

    vuln = d[d["gt_vuln"]]                                    # 4. CWE alignment
    n_no_cwe = int((vuln["gt_cwe"].apply(len) == 0).sum())
    if n_no_cwe:
        print(f"WARNING: {n_no_cwe} ground-truth Vulnerable snippets have no CWE id")
    for m in models:
        hit = vuln.apply(lambda r: len(r[f"{m}_cwe"] & r["gt_cwe"]) > 0, axis=1)
        out[f"{tag(m)}CweAlignCount"] = str(int(hit.sum()))
        out[f"{tag(m)}CweAlignPct"] = f"{hit.mean() * 100:.1f}\\%"

    names = ["GT"] + models                                   # 5. Spearman matrices
    for D in dims:
        mat = pd.DataFrame({"GT": d[f"gt_{D}"], **{m: d[f"{m}_{D}"] for m in models}})
        corr = mat.corr(method="spearman")
        for a in names:
            for b in names:
                if a != b and pd.notna(corr.loc[a, b]):
                    out[f"sp{D}{a}{b}"] = f"{corr.loc[a, b]:.3f}"


        # 6. Binary functional defect detection: positive = defective = Partially Correct or Buggy
    defect_labels = {"buggy", "partially correct"}
    gt_def = d["gt_func"].isin(defect_labels)
    n_def = int(gt_def.sum())
    out["funcDefectiveCount"] = str(n_def)
    out["funcDefectivePct"] = f"{n_def / len(d) * 100:.1f}\\%"

    sonar_labels = set(d["Sonarqube_func"])
    if not sonar_labels <= {"clean", "code smell/bug"}:
        print(f"WARNING: unexpected SonarQube functional labels {sonar_labels}")

    def pct(x):
        return "N/A" if pd.isna(x) else f"{x * 100:.1f}\\%"

    for m in models:
        t = tag(m)
        pred = (d[f"{m}_func"] != "clean") if m == "Sonarqube" else d[f"{m}_func"].isin(defect_labels)
        tp = int((pred & gt_def).sum()); fp = int((pred & ~gt_def).sum())
        fn = int((~pred & gt_def).sum()); tn = int((~pred & ~gt_def).sum())
        prec = tp / (tp + fp) if (tp + fp) else float("nan")
        rec = tp / (tp + fn) if (tp + fn) else float("nan")
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else float("nan")
        out[f"{t}FuncBinTP"] = str(tp)
        out[f"{t}FuncBinFP"] = str(fp)
        out[f"{t}FuncBinFN"] = str(fn)
        out[f"{t}FuncBinTN"] = str(tn)
        out[f"{t}FuncBinAccPct"] = pct((tp + tn) / len(d))
        out[f"{t}FuncBinPrecPct"] = pct(prec)
        out[f"{t}FuncBinRecPct"] = pct(rec)
        out[f"{t}FuncBinFnrPct"] = pct(1 - rec) if not pd.isna(rec) else "N/A"
        out[f"{t}FuncBinFPct"] = pct(f1)

    base_prec = n_def / len(d)
    out["funcAlwaysDefectiveFPct"] = pct(2 * base_prec / (1 + base_prec))

    # 7. Low-maintainability stratum: bottom quartile of expert maintainability
    q1 = d["gt_Maint"].quantile(0.25)
    low = d["gt_Maint"] <= q1
    out["lowMaintQ"] = f"{q1:.0f}"
    out["lowMaintCount"] = str(int(low.sum()))
    out["sonarqubeLowMaintTopPct"] = f"{(d.loc[low, 'Sonarqube_Maint'] >= 100).mean() * 100:.1f}\\%"
    for m in models:
        out[f"{tag(m)}LowMaintMean"] = f"{d.loc[low, f'{m}_Maint'].mean():.1f}"

    marker = "% === Extra Macros (export_extra_macros) ==="
    lines = ["", marker]
    for k, v in out.items():
        lines.append(f"\\providecommand{{\\{k}}}{{}}\\renewcommand{{\\{k}}}{{{v}}}")
    existing = ""
    if os.path.exists(tex_out_path):
        with open(tex_out_path, "r", encoding="utf-8") as f:
            existing = f.read()
        if marker in existing:
            existing = existing.split(marker)[0].rstrip() + "\n"
    with open(tex_out_path, "w", encoding="utf-8") as f:
        f.write(existing + "\n".join(lines).strip() + "\n")
    summary = pd.DataFrame({"macro": list(out.keys()), "value": list(out.values())})
    summary.to_csv(csv_out_path, index=False)
    print(f" - {tex_out_path} ({len(out)} macros)\n - {csv_out_path}")
    return summary

if __name__ == '__main__':
    filename = '..\\..\\Results.json'

    # Will fail immediately with FileNotFoundError if file is missing (No dummy data)
    df = load_and_prepare_data(filename)
    generate_all_visualizations(df, output_dir='.')

    # Export full classification matrices & recall CSV tables
    matrices = export_classification_matrices(df, output_dir='.')
    generate_latex_macros(df, matrices["overall"], matrices["by_language"],
                      matrices["macro_by_language"], output_path="./metrics_macros.tex")
    append_advanced_security_macros(matrices["overall"], "./metrics_macros.tex")
    reasoning_len_df = export_reasoning_length_stats_and_macros(
        df=df,
        output_dir='.',
        tex_out_path='./metrics_macros.tex',
    )
    export_chatgpt_vs_copilot_stats_and_macros(df, matrices["overall"], output_dir='.', tex_out_path='./metrics_macros.tex')
    append_language_overall_mae_macros(df, "./metrics_macros.tex")
    export_conclusion_metrics_and_macros(df, output_dir='.', tex_out_path='./metrics_macros.tex')
    export_human_reliability_and_macros(
        raw_json_path=filename,
        output_dir='.',
        tex_out_path='./metrics_macros.tex',
    )
    export_baselines_calibration_and_stats(
        raw_json_path=filename,
        output_dir='.',
        tex_out_path='./metrics_macros.tex',
    )
    export_cwe_category_recall_and_macros(raw_json_path=filename,
                output_dir='.',
                tex_out_path='./metrics_macros.tex')
    export_extra_macros(raw_json_path=filename)

    mae_details = export_mae_by_language_and_criterion(df, output_dir='./')
    print("\nMAE by Language, Model & Criterion:\n", mae_details.to_string(index=False))

    # Save comprehensive summary statistics table
    summary = df.groupby('model')[['overall_err', 'maint_err', 'sec_correct', 'is_overall_correct', 'reasoning_len']].mean()
    summary['sec_correct'] = summary['sec_correct'] * 100
    summary['is_overall_correct'] = summary['is_overall_correct'] * 100
    summary.columns = ['MAE_Overall_Quality', 'MAE_Maintainability', 'Security_Accuracy_Pct', 'Overall_Accuracy_Pct', 'Avg_Reasoning_Chars']

    summary_path = './summary_statistics_thesis.csv'
    summary.to_csv(summary_path)

    print("\n" + "="*50)
    print(" SUCCESS! Master Thesis Unified Pipeline Complete!")
    print("="*50)
    print(f"Charts saved in: .")
    print(f"Summary table saved to: {summary_path}")
    print("\nSummary Statistics:\n", summary)