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

    ax = sns.barplot(
        data=df,
        x='language',
        y='overall_err',
        hue='model',
        errorbar=None,
        palette=model_colors
    )
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

if __name__ == '__main__':
    filename = '..\\..\\Results.json'

    # Will fail immediately with FileNotFoundError if file is missing (No dummy data)
    df = load_and_prepare_data(filename)
    generate_all_visualizations(df, output_dir='.')

    # Export full classification matrices & recall CSV tables
    export_classification_matrices(df, output_dir='.')
    reasoning_len_df = export_reasoning_length_stats_and_macros(
        df=df,
        output_dir='.',
        tex_out_path='./metrics_macros.tex',
    )
    append_language_overall_mae_macros(df, "./metrics_macros.tex")
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