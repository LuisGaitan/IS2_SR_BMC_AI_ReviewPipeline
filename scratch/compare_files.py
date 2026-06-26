import pandas as pd
import os, sys

sys.stdout.reconfigure(encoding='utf-8')

# Load both files
ai_file = r'Outputs/Firstrun_3_16_2026/Output_Table_1_Quotes.csv'
human_copy = r'Outputs/Firstrun_3_16_2026/Human_Evaluated_Firstrun/IS2 SR - FirstRound_Analysis_Quotes - Output_Table_1_Quotes.csv'

ai_df = pd.read_csv(ai_file)
hc_df = pd.read_csv(human_copy)

print('=== SHAPE COMPARISON ===')
print(f'AI Original:  {ai_df.shape}')
print(f'Human Copy:   {hc_df.shape}')
print(f'\nAI cols:    {list(ai_df.columns)}')
print(f'Human cols: {list(hc_df.columns)}')

extra_cols = [c for c in hc_df.columns if c not in ai_df.columns]
print(f'Extra columns in human copy: {extra_cols}')

# The rows seem to be in different order. Let's compare by key (ID number + Variable name)
shared_cols = [c for c in ai_df.columns if c in hc_df.columns]

ai_df['_key'] = ai_df['ID number'].astype(str) + '_' + ai_df['Variable name'].astype(str)
hc_df['_key'] = hc_df['ID number'].astype(str) + '_' + hc_df['Variable name'].astype(str)

ai_keys = set(ai_df['_key'])
hc_keys = set(hc_df['_key'])

print(f'\n=== KEY-BASED COMPARISON (ID + Variable name) ===')
print(f'AI unique keys: {len(ai_keys)}')
print(f'Human copy unique keys: {len(hc_keys)}')
print(f'Keys in AI but not in Human: {ai_keys - hc_keys}')
print(f'Keys in Human but not in AI: {hc_keys - ai_keys}')

# For overlapping keys, compare the actual content
overlap = ai_keys & hc_keys
print(f'Overlapping keys: {len(overlap)}')

# Merge on key and compare
ai_sorted = ai_df.set_index('_key').sort_index()
hc_sorted = hc_df.set_index('_key').sort_index()

# Compare on shared columns for overlapping keys
compare_cols = ['Strategy name', 'Coded Value', 'Textual Evidence', 'Rationale']
diffs = 0
diff_details = []
for key in sorted(overlap):
    for col in compare_cols:
        a_val = str(ai_sorted.loc[key, col]).strip() if key in ai_sorted.index else ''
        h_val = str(hc_sorted.loc[key, col]).strip() if key in hc_sorted.index else ''
        if a_val != h_val:
            diffs += 1
            if len(diff_details) < 5:
                diff_details.append(f'  Key={key}, Col={col}:\n    AI:    {a_val[:120]}\n    Human: {h_val[:120]}')

print(f'\nContent differences on overlapping keys: {diffs}')
for d in diff_details:
    print(d)

# Now examine all 3 researcher datasheets
print('\n\n========== RESEARCHER DATASHEETS ==========')
base = r'Outputs/Firstrun_3_16_2026/Human_Evaluated_Firstrun'

files = [
    ('Kelly & Dena strat 1-18', 'For_Luis_2026 3-21  IS2 - Secondary coding for 30 new papers - Datasheet Kelly & Dena strat 1-18.csv'),
    ('Kirsten & Jure strat 19-51', 'For_Luis_2026 3-21  IS2 - Secondary coding for 30 new papers - Datasheet Kirsten&Jure strat 19-51.csv'),
    ('Amanda & Allison strat 52-73', 'For_Luis_2026 3-21  IS2 - Secondary coding for 30 new papers - Datasheet Amanda&Allison strat 52-73.csv'),
]

for label, f in files:
    path = os.path.join(base, f)
    df = pd.read_csv(path, encoding='utf-8', on_bad_lines='skip')
    print(f'\n--- {label} ---')
    print(f'  Shape: {df.shape}')
    print(f'  Columns: {list(df.columns)}')
    # Check for key columns
    has_human_coded = 'Human Coded Value' in df.columns
    has_ai_coded = 'AI Coded Value' in df.columns
    print(f'  Has "AI Coded Value": {has_ai_coded}')
    print(f'  Has "Human Coded Value": {has_human_coded}')
    if has_human_coded and has_ai_coded:
        print(f'  AI 1s: {(df["AI Coded Value"] == 1).sum()}, Human 1s: {(df["Human Coded Value"] == 1).sum()}')
        print(f'  AI 0s: {(df["AI Coded Value"] == 0).sum()}, Human 0s: {(df["Human Coded Value"] == 0).sum()}')
        agree = (df["AI Coded Value"] == df["Human Coded Value"]).sum()
        print(f'  Agreement: {agree}/{len(df)} ({agree/len(df)*100:.1f}%)')
    # Show sample data
    print(f'  Sample rows (first 2):')
    for i, row in df.head(2).iterrows():
        for col in df.columns:
            val = str(row[col])
            if len(val) > 100:
                val = val[:100] + '...'
            print(f'    {col}: {val}')
        print('    ---')
