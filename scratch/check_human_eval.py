import pandas as pd
import sys
sys.stdout.reconfigure(encoding="utf-8")

files = [
    r"Outputs\Firstrun_3_16_2026\Human_Evaluated_Firstrun\For_Luis_2026 3-21  IS2 - Secondary coding for 30 new papers - Datasheet Kelly & Dena strat 1-18.csv",
    r"Outputs\Firstrun_3_16_2026\Human_Evaluated_Firstrun\For_Luis_2026 3-21  IS2 - Secondary coding for 30 new papers - Datasheet Kirsten&Jure strat 19-51.csv",
    r"Outputs\Firstrun_3_16_2026\Human_Evaluated_Firstrun\For_Luis_2026 3-21  IS2 - Secondary coding for 30 new papers - Datasheet Amanda&Allison strat 52-73.csv",
]

dfs = [pd.read_csv(f, encoding="utf-8") for f in files]
combined = pd.concat(dfs, ignore_index=True)

print("Total rows:", len(combined))
print("Common columns:", [c for c in combined.columns if c in dfs[0].columns and c in dfs[1].columns and c in dfs[2].columns])

# Focus on AI positive codings
ai_pos = combined[combined["AI Coded Value"] == 1]
print(f"\nAI positives: {len(ai_pos)}")

tp = (ai_pos["Human Coded Value"] == 1).sum()
fp = (ai_pos["Human Coded Value"] == 0).sum()
human_na = ai_pos["Human Coded Value"].isna().sum()

print(f"TP (AI=1, Human=1): {tp}")
print(f"FP (AI=1, Human=0): {fp}")
print(f"Human not coded: {human_na}")
if tp + fp > 0:
    print(f"Precision (where human coded): {tp}/{tp+fp} = {tp/(tp+fp)*100:.1f}%")

papers = combined["ID number"].nunique()
print(f"Papers: {papers}")
