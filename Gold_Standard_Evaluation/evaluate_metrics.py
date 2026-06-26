import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, cohen_kappa_score
import os

def calculate_metrics():
    # Load AI predictions
    ai_preds_path = "Outputs/Output_Table_2_Binary_Matrix.csv"
    if not os.path.exists(ai_preds_path):
        print("Predictions file not found! Please run evaluation_pipeline.py first.")
        return

    ai_df = pd.read_csv(ai_preds_path)
    # Ensure ID is string to merge properly
    ai_df['ID'] = ai_df['ID'].astype(str)

    # Load Gold Standard
    gold_df = pd.read_csv("../Imp Strategy Coder_Gold Standard Docs/imp_strat_final_sort of + clearly2.csv")
    gold_df['Cov_ID'] = gold_df['Cov_ID'].astype(str)

    # Find the overlapping IDs
    overlapping_ids = set(ai_df['ID']).intersection(set(gold_df['Cov_ID']))
    if not overlapping_ids:
        print("No overlapping IDs found. Make sure prediction data has matching IDs.")
        return
        
    print(f"Evaluating on {len(overlapping_ids)} overlapping papers.")

    # We need a list of strategies
    # Look at strat_1 to strat_73 structure or just the common columns
    ai_cols = set(ai_df.columns)
    gold_cols = set(gold_df.columns)
    
    # We want strategy columns like strat_1, strat_2 etc.
    strategy_cols = [c for c in ai_cols if c.startswith('strat_') and c in gold_cols]
    print(f"Evaluating across {len(strategy_cols)} strategies.")

    # Flatten the matrices to compute overall metrics
    # Or compute per-strategy
    
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

    # Calculate metrics
    precision = precision_score(overall_y_true, overall_y_pred, zero_division=0)
    recall = recall_score(overall_y_true, overall_y_pred, zero_division=0)
    f1 = f1_score(overall_y_true, overall_y_pred, zero_division=0)
    kappa = cohen_kappa_score(overall_y_true, overall_y_pred)

    # Calculate McNemar's Test P-Value
    from sklearn.metrics import confusion_matrix
    from statsmodels.stats.contingency_tables import mcnemar
    
    cm = confusion_matrix(overall_y_true, overall_y_pred)
    # mcnemar expects a 2x2 contingency table: [[TN, FP], [FN, TP]]
    mcnemar_result = mcnemar(cm, exact=False, correction=True)
    p_value = mcnemar_result.pvalue

    print("\n--- Overall Performance Metrics ---")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"Cohen's Kappa: {kappa:.4f}")
    
    if p_value < 0.001:
        print(f"McNemar's p-value: < 0.001 (Highly Significant Bias)")
    else:
        print(f"McNemar's p-value: {p_value:.4f}")

if __name__ == "__main__":
    calculate_metrics()
