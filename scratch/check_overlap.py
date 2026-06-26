import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Check overlap between gold standard papers and first run papers
gold_df = pd.read_csv(r'Imp Strategy Coder_Gold Standard Docs/imp_strat_final_sort of + clearly2.csv')
gold_ids = set(gold_df['Cov_ID'].astype(str).unique())

firstrun_df = pd.read_csv(r'Outputs/Firstrun_3_16_2026/Output_Table_2_Binary_Matrix.csv')
firstrun_ids = set(firstrun_df['ID'].astype(str).unique())

gs_eval_df = pd.read_csv(r'Gold_Standard_Evaluation/Outputs/Output_Table_2_Binary_Matrix.csv')
gs_eval_ids = set(gs_eval_df['ID'].astype(str).unique())

print(f'Gold Standard human-coded papers: {len(gold_ids)}')
print(f'First Run target papers: {len(firstrun_ids)}')
print(f'Gold Standard Evaluation AI-coded papers: {len(gs_eval_ids)}')
print(f'Overlap between First Run and Gold Standard: {firstrun_ids & gold_ids}')
print(f'Gold Standard papers used in GS Evaluation: {len(gs_eval_ids & gold_ids)}')
