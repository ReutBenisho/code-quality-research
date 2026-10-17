import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid', palette='colorblind', font='DejaVu Sans')
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11

def load_and_prepare_data(file_path='Results.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        
    records = []
    models = ['ChatGPT', 'Claude', 'Gemini', 'GithubCopilot', 'Sonarqube']
    
    for key, item in raw_data.items():
        meta = item['metadata']
        
        h_read = np.mean([item['Human1']['readability_score'], item['Human2']['readability_score'], item['Human3']['readability_score']])
        h_und  = np.mean([item['Human1']['understandability_score'], item['Human2']['understandability_score'], item['Human3']['understandability_score']])
        h_maint = np.mean([item['Human1']['maintainability_score'], item['Human2']['maintainability_score'], item['Human3']['maintainability_score']])
        
        row_base = {
            'snippet_id': key,
            'global_id': meta.get('id'),
            'language': meta.get('language'),
            'origin': meta.get('origin'),
            'gt_read': h_read,
            'gt_und': h_und,
            'gt_maint': h_maint,
            'gt_sec': meta.get('security_classification'),
            'gt_func': meta.get('functional_classification')
        }
        
        for m in models:
            m_data = item.get(m, {})
            row = row_base.copy()
            row['model'] = m
            row['readability'] = float(m_data.get('readability_score', 0))
            row['understandability'] = float(m_data.get('understandability_score', 0))
            row['maintainability'] = float(m_data.get('maintainability_score', 0))
            row['func_class'] = m_data.get('functional_classification')
            row['sec_class'] = str(m_data.get('security_classification'))
            row['reasoning'] = m_data.get('reasoning', '')
            row['reasoning_len'] = len(m_data.get('reasoning', ''))
            
            row['maint_err'] = abs(row['maintainability'] - h_maint)
            row['read_err'] = abs(row['readability'] - h_read)
            row['und_err'] = abs(row['understandability'] - h_und)
            
            row['sec_correct'] = 1 if row['sec_class'].lower() in ['safe', 'vulnerable'] and row['sec_class'].lower() == str(row['gt_sec']).lower() else 0
            row['func_correct'] = 1 if str(row['func_class']).lower() == str(row['gt_func']).lower() else 0
            
            records.append(row)
            
    return pd.DataFrame(records)


def plot_mae_by_language(df, output_path='01_mae_by_language.png'):
    fig, ax = plt.subplots(figsize=(10, 6))
    mae_df = df.groupby(['model', 'language'])['maint_err'].mean().reset_index()
    
    sns.barplot(data=mae_df, x='model', y='maint_err', hue='language', ax=ax, palette='Set2')
    
    ax.set_title('Mean Absolute Error (MAE) in Maintainability vs. Ground Truth', fontweight='bold', pad=15)
    ax.set_xlabel('Model')
    ax.set_ylabel('Mean Absolute Error (Points)')
    ax.legend(title='Language', frameon=True)
    
    for p in ax.patches:
        h = p.get_height()
        if h > 0:
            ax.annotate(f'{h:.1f}', (p.get_x() + p.get_width() / 2., h),
                        ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')
            
    sns.despine()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()


def plot_correlation_heatmap(df, output_path='02_correlation_heatmap.png'):
    fig, ax = plt.subplots(figsize=(8, 7))
    piv = df.pivot(index='snippet_id', columns='model', values='maintainability')
    corr = piv.corr(method='spearman')
    
    sns.heatmap(corr, annot=True, fmt='.3f', cmap='Blues', vmin=-0.2, vmax=1.0,
                square=True, linewidths=1, cbar_kws={"shrink": .8}, ax=ax)
    
    ax.set_title('Spearman Correlation Matrix: Maintainability Scores', fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()


def plot_chatgpt_vs_copilot(df, output_path='03_chatgpt_vs_copilot.png'):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    cg_copilot = df[df['model'].isin(['ChatGPT', 'GithubCopilot'])]
    
    sns.barplot(data=cg_copilot, x='language', y='maint_err', hue='model', ax=ax1, palette=['#2ca02c', '#1f77b4'])
    ax1.set_title('Maintainability MAE: ChatGPT vs. Copilot', fontweight='bold')
    ax1.set_xlabel('Language')
    ax1.set_ylabel('MAE (Lower is Better)')
    
    sec_df = cg_copilot.groupby(['language', 'model'])['sec_correct'].mean().reset_index()
    sec_df['sec_accuracy_pct'] = sec_df['sec_correct'] * 100
    
    sns.barplot(data=sec_df, x='language', y='sec_accuracy_pct', hue='model', ax=ax2, palette=['#2ca02c', '#1f77b4'])
    ax2.set_title('Security Classification Accuracy (%)', fontweight='bold')
    ax2.set_xlabel('Language')
    ax2.set_ylabel('Accuracy % (Higher is Better)')
    ax2.set_ylim(0, 100)

    sns.despine()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()


def plot_security_accuracy(df, output_path='04_security_accuracy.png'):
    fig, ax = plt.subplots(figsize=(10, 6))
    sec_df = df.groupby(['model', 'language'])['sec_correct'].mean().reset_index()
    sec_df['sec_accuracy'] = sec_df['sec_correct'] * 100
    
    sns.barplot(data=sec_df, x='model', y='sec_accuracy', hue='language', ax=ax, palette='Set2')
    ax.set_title('Security Vulnerability Detection Accuracy (%) by Language', fontweight='bold', pad=15)
    ax.set_xlabel('Model')
    ax.set_ylabel('Accuracy (%)')
    ax.set_ylim(0, 105)
    
    sns.despine()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()


def plot_reasoning_vs_error(df, output_path='05_reasoning_vs_error.png'):
    fig, ax = plt.subplots(figsize=(10, 6))
    ai_df = df[df['model'] != 'Sonarqube']
    
    sns.scatterplot(data=ai_df, x='reasoning_len', y='maint_err', hue='model', alpha=0.6, s=50, ax=ax)
    sns.regplot(data=ai_df, x='reasoning_len', y='maint_err', scatter=False, ax=ax, color='black', line_kws={'linestyle': '--', 'linewidth': 1.5})
    
    ax.set_title('Reasoning Character Length vs. Maintainability Error', fontweight='bold', pad=15)
    ax.set_xlabel('Reasoning Explanation Length (Characters)')
    ax.set_ylabel('Maintainability MAE (Error Points)')
    
    sns.despine()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    df = load_and_prepare_data('Results.json')
    plot_mae_by_language(df)
    plot_correlation_heatmap(df)
    plot_chatgpt_vs_copilot(df)
    plot_security_accuracy(df)
    plot_reasoning_vs_error(df)
    print("כל הגרפים יוצרו בהצלחה!")