import pandas as pd
import os, sys

sys.stdout.reconfigure(encoding='utf-8')

base = r'Outputs/Firstrun_3_16_2026/Human_Evaluated_Firstrun'

# Load all 3 researcher datasheets
df1 = pd.read_csv(os.path.join(base, 'For_Luis_2026 3-21  IS2 - Secondary coding for 30 new papers - Datasheet Kelly & Dena strat 1-18.csv'))
df2 = pd.read_csv(os.path.join(base, 'For_Luis_2026 3-21  IS2 - Secondary coding for 30 new papers - Datasheet Kirsten&Jure strat 19-51.csv'))
df3 = pd.read_csv(os.path.join(base, 'For_Luis_2026 3-21  IS2 - Secondary coding for 30 new papers - Datasheet Amanda&Allison strat 52-73.csv'))

# Normalize column names
for df in [df1, df2, df3]:
    df.columns = [c.strip() for c in df.columns]

# Standardize the variable name column
df1 = df1.rename(columns={'Variable name in dataset': 'Variable name'})
df2 = df2.rename(columns={'Variable name in dataset': 'Variable name'})
df3 = df3.rename(columns={'Variable name in dataset': 'Variable name'})

# Combine all
all_df = pd.concat([df1, df2, df3], ignore_index=True)

# Drop rows with missing values in either coded column
all_df = all_df.dropna(subset=['Human Coded Value', 'AI Coded Value'])
all_df['AI Coded Value'] = all_df['AI Coded Value'].astype(int)
all_df['Human Coded Value'] = all_df['Human Coded Value'].astype(int)

print(f'Total rows after cleaning: {len(all_df)}')
print(f'AI 1s: {(all_df["AI Coded Value"] == 1).sum()}')
print(f'AI 0s: {(all_df["AI Coded Value"] == 0).sum()}')
print(f'Human 1s: {(all_df["Human Coded Value"] == 1).sum()}')
print(f'Human 0s: {(all_df["Human Coded Value"] == 0).sum()}')

# Overall precision
ai_positive = all_df[all_df['AI Coded Value'] == 1]
tp = ((ai_positive['AI Coded Value'] == 1) & (ai_positive['Human Coded Value'] == 1)).sum()
fp = ((ai_positive['AI Coded Value'] == 1) & (ai_positive['Human Coded Value'] == 0)).sum()
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
print(f'\n=== OVERALL PRECISION ===')
print(f'True Positives (AI=1, Human=1): {tp}')
print(f'False Positives (AI=1, Human=0): {fp}')
print(f'Precision: {precision:.4f} ({precision*100:.1f}%)')

# Stratified by range
print(f'\n=== STRATIFIED BY RESEARCHER TEAM ===')
for label, df in [('Kelly & Dena (strat 1-18)', df1), ('Kirsten & Jure (strat 19-51)', df2), ('Amanda & Allison (strat 52-73)', df3)]:
    df_clean = df.dropna(subset=['Human Coded Value', 'AI Coded Value'])
    df_clean['AI Coded Value'] = df_clean['AI Coded Value'].astype(int)
    df_clean['Human Coded Value'] = df_clean['Human Coded Value'].astype(int)
    ai_pos = df_clean[df_clean['AI Coded Value'] == 1]
    t = ((ai_pos['Human Coded Value'] == 1)).sum()
    f = ((ai_pos['Human Coded Value'] == 0)).sum()
    p = t / (t + f) if (t + f) > 0 else 0
    print(f'{label}: TP={t}, FP={f}, Precision={p:.4f} ({p*100:.1f}%)')

# Per-strategy precision
print(f'\n=== PER-STRATEGY PRECISION ===')
print(f'{"Strategy":<12} {"Strategy Name":<65} {"AI_1s":>5} {"Human_1s":>8} {"Human_0s":>8} {"Precision":>9}')
print('-' * 115)

import re
valid_strats = all_df[all_df['Variable name'].str.match(r'^strat_\d+$', na=False)]
print(f'(Filtered {len(all_df) - len(valid_strats)} rows with non-standard Variable names)')
strat_results = []
for strat in sorted(valid_strats['Variable name'].unique(), key=lambda x: int(x.replace('strat_', ''))):
    strat_data = all_df[(all_df['Variable name'] == strat) & (all_df['AI Coded Value'] == 1)]
    if len(strat_data) == 0:
        continue
    t = (strat_data['Human Coded Value'] == 1).sum()
    f = (strat_data['Human Coded Value'] == 0).sum()
    total = t + f
    p = t / total if total > 0 else 0
    name = strat_data['Strategy name'].iloc[0] if 'Strategy name' in strat_data.columns else ''
    if len(name) > 63:
        name = name[:60] + '...'
    print(f'{strat:<12} {name:<65} {total:>5} {t:>8} {f:>8} {p:>8.1f}%')
    strat_results.append({'strat': strat, 'name': name, 'ai_1s': total, 'human_1s': t, 'human_0s': f, 'precision': p})

# Worst strategies (lowest precision)
print(f'\n=== TOP 10 MOST OVER-CODED STRATEGIES (Lowest Precision) ===')
worst = sorted([s for s in strat_results if s['ai_1s'] >= 2], key=lambda x: x['precision'])
for s in worst[:10]:
    print(f"  {s['strat']}: {s['name'][:55]} — Precision: {s['precision']*100:.1f}% ({s['human_1s']}/{s['ai_1s']})")

# Best strategies (highest precision)
print(f'\n=== TOP 10 BEST STRATEGIES (Highest Precision, min 2 occurrences) ===')
best = sorted([s for s in strat_results if s['ai_1s'] >= 2], key=lambda x: -x['precision'])
for s in best[:10]:
    print(f"  {s['strat']}: {s['name'][:55]} — Precision: {s['precision']*100:.1f}% ({s['human_1s']}/{s['ai_1s']})")

# Per-paper precision
print(f'\n=== PER-PAPER PRECISION ===')
print(f'{"ID":<8} {"Author":<20} {"AI_1s":>5} {"Human_1s":>8} {"Human_0s":>8} {"Precision":>9}')
print('-' * 65)

paper_results = []
for paper_id in sorted(all_df['ID number'].unique()):
    paper_data = all_df[(all_df['ID number'] == paper_id) & (all_df['AI Coded Value'] == 1)]
    if len(paper_data) == 0:
        continue
    author = paper_data['Author last name'].iloc[0]
    t = (paper_data['Human Coded Value'] == 1).sum()
    f = (paper_data['Human Coded Value'] == 0).sum()
    total = t + f
    p = t / total if total > 0 else 0
    print(f'{int(paper_id):<8} {author:<20} {total:>5} {t:>8} {f:>8} {p:>8.1f}%')
    paper_results.append({'id': int(paper_id), 'author': author, 'ai_1s': total, 'human_1s': t, 'human_0s': f, 'precision': p})

# Worst papers
print(f'\n=== MOST PROBLEMATIC PAPERS (Lowest Precision) ===')
worst_p = sorted(paper_results, key=lambda x: x['precision'])
for p in worst_p[:5]:
    print(f"  {p['author']} ({p['id']}): Precision: {p['precision']*100:.1f}% ({p['human_1s']}/{p['ai_1s']})")

# Best papers
print(f'\n=== MOST ACCURATE PAPERS (Highest Precision) ===')
best_p = sorted(paper_results, key=lambda x: -x['precision'])
for p in best_p[:5]:
    print(f"  {p['author']} ({p['id']}): Precision: {p['precision']*100:.1f}% ({p['human_1s']}/{p['ai_1s']})")

# Binary matrix stats
print(f'\n=== BINARY MATRIX CONTEXT ===')
matrix_path = r'Outputs/Firstrun_3_16_2026/Output_Table_2_Binary_Matrix.csv'
matrix_df = pd.read_csv(matrix_path)
strat_cols = [c for c in matrix_df.columns if c.startswith('strat_')]
total_cells = len(matrix_df) * len(strat_cols)
total_ones = matrix_df[strat_cols].fillna(0).sum().sum()
total_zeros = total_cells - total_ones
print(f'Papers: {len(matrix_df)}')
print(f'Strategies: {len(strat_cols)}')
print(f'Total coding decisions: {total_cells}')
print(f'AI coded 1: {int(total_ones)} ({total_ones/total_cells*100:.1f}%)')
print(f'AI coded 0: {int(total_zeros)} ({total_zeros/total_cells*100:.1f}%)')
