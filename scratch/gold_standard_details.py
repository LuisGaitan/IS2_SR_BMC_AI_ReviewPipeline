import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, cohen_kappa_score, confusion_matrix
from statsmodels.stats.contingency_tables import mcnemar
import os, sys

sys.stdout.reconfigure(encoding='utf-8')

# Load AI predictions from Gold Standard evaluation
ai_df = pd.read_csv(r'Gold_Standard_Evaluation/Outputs/Output_Table_2_Binary_Matrix.csv')
ai_df['ID'] = ai_df['ID'].astype(str)

# Load Gold Standard
gold_df = pd.read_csv(r'Imp Strategy Coder_Gold Standard Docs/imp_strat_final_sort of + clearly2.csv')
gold_df['Cov_ID'] = gold_df['Cov_ID'].astype(str)

overlapping_ids = set(ai_df['ID']).intersection(set(gold_df['Cov_ID']))
strategy_cols = [c for c in ai_df.columns if c.startswith('strat_') and c in gold_df.columns]

print(f'Overlapping papers: {len(overlapping_ids)}')
print(f'Strategy columns: {len(strategy_cols)}')
print(f'Total coding decisions: {len(overlapping_ids) * len(strategy_cols)}')

overall_y_true = []
overall_y_pred = []

for cov_id in overlapping_ids:
    ai_row = ai_df[ai_df['ID'] == cov_id].iloc[0]
    gold_row = gold_df[gold_df['Cov_ID'] == cov_id].iloc[0]
    for col in strategy_cols:
        y_pred = int(ai_row[col]) if pd.notna(ai_row[col]) else 0
        y_true = int(gold_row[col]) if pd.notna(gold_row[col]) else 0
        overall_y_pred.append(y_pred)
        overall_y_true.append(y_true)

# Confusion matrix
cm = confusion_matrix(overall_y_true, overall_y_pred)
tn, fp, fn, tp = cm.ravel()

print(f'\n=== CONFUSION MATRIX (Gold Standard) ===')
print(f'                  AI Predicted')
print(f'                  0        1')
print(f'Human Gold  0   {tn:>5}   {fp:>5}   (TN, FP)')
print(f'Standard    1   {fn:>5}   {tp:>5}   (FN, TP)')

print(f'\nTrue Positives (TP):  {tp}')
print(f'True Negatives (TN):  {tn}')
print(f'False Positives (FP): {fp}')
print(f'False Negatives (FN): {fn}')
print(f'Total:                {tp+tn+fp+fn}')

precision = precision_score(overall_y_true, overall_y_pred, zero_division=0)
recall = recall_score(overall_y_true, overall_y_pred, zero_division=0)
f1 = f1_score(overall_y_true, overall_y_pred, zero_division=0)
kappa = cohen_kappa_score(overall_y_true, overall_y_pred)

mcnemar_result = mcnemar(cm, exact=False, correction=True)
p_value = mcnemar_result.pvalue

print(f'\n=== METRICS ===')
print(f'Precision:       {precision:.4f}')
print(f'Recall:          {recall:.4f}')
print(f'F1 Score:        {f1:.4f}')
print(f"Cohen's Kappa:   {kappa:.4f}")
print(f"McNemar's p:     {'< 0.001' if p_value < 0.001 else f'{p_value:.4f}'}")

# Also compute: what % of gold standard is 1 vs 0
gold_ones = sum(overall_y_true)
gold_zeros = len(overall_y_true) - gold_ones
ai_ones = sum(overall_y_pred)
ai_zeros = len(overall_y_pred) - ai_ones
print(f'\n=== PREVALENCE ===')
print(f'Gold Standard 1s: {gold_ones} ({gold_ones/len(overall_y_true)*100:.1f}%)')
print(f'Gold Standard 0s: {gold_zeros} ({gold_zeros/len(overall_y_true)*100:.1f}%)')
print(f'AI Predicted 1s:  {ai_ones} ({ai_ones/len(overall_y_pred)*100:.1f}%)')
print(f'AI Predicted 0s:  {ai_zeros} ({ai_zeros/len(overall_y_pred)*100:.1f}%)')

# Specificity and NPV
specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
npv = tn / (tn + fn) if (tn + fn) > 0 else 0
print(f'\n=== ADDITIONAL METRICS ===')
print(f'Specificity:     {specificity:.4f}')
print(f'NPV:             {npv:.4f}')
print(f'FP Rate:         {fp/(fp+tn):.4f}')
print(f'FN Rate:         {fn/(fn+tp):.4f}')
print(f'Prevalence:      {(tp+fn)/(tp+tn+fp+fn):.4f}')
