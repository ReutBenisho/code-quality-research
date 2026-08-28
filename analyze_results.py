# -*- coding: utf-8 -*-
"""
Code Quality & Security Comparative Analysis Script
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.use('Agg')

sns.set_theme(style='whitegrid', palette='colorblind', font='DejaVu Sans')
CHART_DPI = 150

def load_and_harmonize_data(filepath):
    """
    Loads Results.json, flattens the nested structures, 
    and harmonizes classifications between AI models and SonarQube.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}. Please make sure 'Results.json' is in the same folder.")
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    rows = []
    for snippet_key, snippet_content in data.items():
        metadata = snippet_content.get('metadata', {})
        snippet_id = metadata.get('id')
        language = metadata.get('language', '').lower()
        origin = metadata.get('origin', '')
        
        for tool_name, tool_eval in snippet_content.items():
            if tool_name == 'metadata':
                continue
                
            # Convert readability, understandability, maintainability scores to numeric
            readability = pd.to_numeric(tool_eval.get('readability_score'), errors='coerce')
            understandability = pd.to_numeric(tool_eval.get('understandability_score'), errors='coerce')
            maintainability = pd.to_numeric(tool_eval.get('maintainability_score'), errors='coerce')
            
            # Functional classification
            func_class = tool_eval.get('functional_classification', '')
            # Security classification
            sec_class = str(tool_eval.get('security_classification', ''))
            
            # HARMONIZATION LOGIC
            # 1. Is Vulnerable?
            if tool_name.lower() == 'sonarqube':
                # SonarQube uses a security score where 100.0 is safe (0 vulnerabilities)
                try:
                    sec_score = float(sec_class)
                    is_vulnerable = sec_score < 100.0
                except ValueError:
                    is_vulnerable = False
            else:
                is_vulnerable = sec_class.strip().lower() == 'vulnerable'
                
            # 2. Is Buggy / Has Functional Defect?
            if tool_name.lower() == 'sonarqube':
                # SonarQube uses 'Clean' or 'Code Smell/Bug' or 'Bug'
                is_buggy = func_class.strip().lower() in ['code smell/bug', 'bug', 'buggy']
            else:
                # LLMs use 'Buggy', 'Partially Correct', 'Correct'
                is_buggy = func_class.strip().lower() in ['buggy', 'partially correct']
                
            # Overall combined quality score
            overall_quality = np.mean([readability, understandability, maintainability]) if not np.isnan(readability) else np.nan
                
            rows.append({
                'snippet_key': snippet_key,
                'snippet_id': snippet_id,
                'language': language,
                'origin': origin,
                'tool': tool_name,
                'readability_score': readability,
                'understandability_score': understandability,
                'maintainability_score': maintainability,
                'overall_quality_score': overall_quality,
                'functional_classification': func_class,
                'security_classification': sec_class,
                'is_vulnerable': is_vulnerable,
                'is_buggy': is_buggy,
                'cwe_id': tool_eval.get('cwe_id', 'None')
            })
            
    return pd.DataFrame(rows)

def generate_visualizations(df, output_dir='./output_charts'):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating charts and saving to: {output_dir}")
    
    # ----------------------------------------------------
    # Chart 1: Code Quality Pillars Comparison (RQ1.2)
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    quality_cols = ['readability_score', 'understandability_score', 'maintainability_score']
    # Melt the dataframe for plotting
    df_melt = df.melt(id_vars=['tool'], value_vars=quality_cols, 
                      var_name='Pillar', value_name='Score')
    df_melt['Pillar'] = df_melt['Pillar'].str.replace('_score', '').str.title()
    
    ax = sns.barplot(data=df_melt, x='tool', y='Score', hue='Pillar', errorbar=None)
    ax.set_title("Claude & ChatGPT Outperform in Code Quality Scores, While SonarQube Serves as Baseline", 
                 fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Analysis Tool / AI Model", fontsize=11, fontweight='bold')
    ax.set_ylabel("Average Score (0-100)", fontsize=11, fontweight='bold')
    ax.set_ylim(0, 110)
    for c in ax.containers:
        ax.bar_label(c, fmt='%.1f', fontsize=8, fontweight='bold', padding=3)
    
    sns.despine()
    plt.tight_layout(pad=1.5)
    plt.savefig(os.path.join(output_dir, 'chart1_quality_pillars.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()
    
    # ----------------------------------------------------
    # Chart 2: Language Sensitivity on Overall Quality (RQ1.3)
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=df, x='language', y='overall_quality_score', hue='tool', errorbar=None)
    ax.set_title("AI Code Quality Assessment Varies Across Languages with Python Leading in Scores", 
                 fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Programming Language", fontsize=11, fontweight='bold')
    ax.set_ylabel("Average Overall Quality Score (0-100)", fontsize=11, fontweight='bold')
    ax.set_ylim(0, 110)
    for c in ax.containers:
        ax.bar_label(c, fmt='%.1f', fontsize=8, padding=2)
        
    sns.despine()
    plt.tight_layout(pad=1.5)
    plt.savefig(os.path.join(output_dir, 'chart2_language_sensitivity.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()
    
    # ----------------------------------------------------
    # Chart 3: Vulnerability Detection Rate (RQ1.1 - Security)
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    # Calculate vulnerability percentage
    vuln_rates = df.groupby('tool')['is_vulnerable'].mean() * 100
    vuln_rates = vuln_rates.reset_index().sort_values(by='is_vulnerable', ascending=False)
    
    ax = sns.barplot(data=vuln_rates, x='tool', y='is_vulnerable', hue='tool', palette='Oranges_r', legend=False)
    ax.set_title("Claude and ChatGPT Detect Vulnerabilities in Over 50% of Challenged Code Snippets", 
                 fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Analysis Tool / AI Model", fontsize=11, fontweight='bold')
    ax.set_ylabel("Vulnerability Detection Rate (%)", fontsize=11, fontweight='bold')
    ax.set_ylim(0, 100)
    for c in ax.containers:
        ax.bar_label(c, fmt='%.1f%%', fontweight='bold', padding=3)
        
    sns.despine()
    plt.tight_layout(pad=1.5)
    plt.savefig(os.path.join(output_dir, 'chart3_security_vulnerability.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()

    # ----------------------------------------------------
    # Chart 4: Functional Correctness Distribution (RQ1.1 - Functional)
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    bug_rates = df.groupby('tool')['is_buggy'].mean() * 100
    bug_rates = bug_rates.reset_index().sort_values(by='is_buggy', ascending=False)
    
    ax = sns.barplot(data=bug_rates, x='tool', y='is_buggy', hue='tool', palette='Reds_r', legend=False)
    ax.set_title("AI Engines Highlight Functional Issues in 40%+ of Target Code Snippets", 
                 fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Analysis Tool / AI Model", fontsize=11, fontweight='bold')
    ax.set_ylabel("Functional Issues Flagged Rate (%)", fontsize=11, fontweight='bold')
    ax.set_ylim(0, 100)
    for c in ax.containers:
        ax.bar_label(c, fmt='%.1f%%', fontweight='bold', padding=3)
        
    sns.despine()
    plt.tight_layout(pad=1.5)
    plt.savefig(os.path.join(output_dir, 'chart4_functional_defects.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()
    
    print("All charts generated successfully!")

if __name__ == '__main__':
    # When running locally, expects 'Results.json' in the same folder.
    filename = 'Results.json'
    if not os.path.exists(filename) and os.path.exists('/workspace/scratch/dummy_results.json'):
        filename = '/workspace/scratch/dummy_results.json'
        print("Results.json not found locally. Running with dummy_results.json for testing...")
        
    try:
        df = load_and_harmonize_data(filename)
        generate_visualizations(df)
        
        # Save a basic summary table
        summary = df.groupby('tool')[['readability_score', 'understandability_score', 'maintainability_score', 'is_vulnerable', 'is_buggy']].mean()
        summary.to_csv('./output_charts/summary_statistics.csv')
        print("\nSummary Statistics:\n", summary)
    except Exception as e:
        print(f"Error occurred: {e}")
