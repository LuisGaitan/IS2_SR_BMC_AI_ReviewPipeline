# Precision Audit Report — First Run AI Pipeline (3/16/2026)

## Executive Summary

This report evaluates the **positive predictive value (Precision)** of the AI-powered Implementation Science data tagging pipeline by comparing AI-generated strategy codings against independent human expert review. The research team (Kelly & Dena, Kirsten & Jure, Amanda & Allison) reviewed all 307 positive identifications made by the AI across 30 academic papers and 73 implementation strategies.

> [!IMPORTANT]
> **Overall Precision: 72.3%** — Of the 307 times the AI identified a strategy as present (coded 1), human experts confirmed 222 and rejected 85.

---

## Methodology & Scope

- **Pipeline version:** First Run architecture (no feedback guardrails, no self-reflection)
- **Model:** Gemini 2.5 Pro (`temperature=0.0`)
- **Sample:** 30 academic papers × 73 implementation strategies = **2,190 total coding decisions**
- **Human review scope:** The research team reviewed only the AI's positive identifications (coded as 1). Cases where the AI coded 0 were **not** reviewed by the human team.

### What This Audit Measures

| Metric | Status | Notes |
|---|---|---|
| **Precision (PPV)** | ✅ Fully valid | Human-confirmed 1s / Total AI 1s |
| **Recall (Sensitivity)** | ❌ Not evaluated | Would require human review of AI's 0-coded strategies |
| **F1 Score** | ❌ Cannot compute | Requires both Precision and Recall |
| **Cohen's Kappa** | ❌ Cannot compute | Requires complete 2×2 contingency table |

> [!NOTE]
> **Recall was not evaluated in this round.** The human team only reviewed cases where the AI flagged a strategy as present. To estimate Recall, a stratified sample of the AI's 1,883 negative codings would need to be independently reviewed by the research team.

---

## AI Rejection Rate Context

The AI's overall coding behavior is **conservative by design** — the prompt instructs it to "default to 0" when evidence is ambiguous.

| Coding Decision | Count | Percentage |
|---|---|---|
| **AI coded 0 (Absent)** | 1,883 | **86.0%** |
| **AI coded 1 (Present)** | 307 | **14.0%** |
| **Total decisions** | 2,190 | 100% |

The AI rejected the vast majority of strategy–paper combinations. However, **when it did flag a strategy as present, it was correct approximately 72% of the time** and over-coded approximately 28% of its positive identifications.

---

## Overall Precision

| Metric | Value |
|---|---|
| **True Positives** (AI=1, Human=1) | 222 |
| **False Positives** (AI=1, Human=0) | 85 |
| **Overall Precision** | **72.3%** |
| **False Positive Rate (on positives)** | 27.7% |

---

## Stratified Precision by Researcher Team

Each researcher pair reviewed a distinct range of strategies:

| Researcher Team | Strategy Range | AI Positives | Confirmed (TP) | Rejected (FP) | Precision |
|---|---|---|---|---|---|
| Kelly & Dena | strat 1–18 | 109 | 71 | 38 | **65.1%** |
| Kirsten & Jure | strat 19–51 | 117 | 98 | 19 | **83.8%** |
| Amanda & Allison | strat 52–73 | 81 | 53 | 28 | **65.4%** |
| **Overall** | **strat 1–73** | **307** | **222** | **85** | **72.3%** |

> [!TIP]
> Strategies 19–51 showed notably higher precision (83.8%), suggesting the AI performs best on strategies with more concrete, observable definitions (e.g., coalitions, partnerships, meetings, training). Strategies 1–18 and 52–73, which include more abstract or judgment-dependent constructs, showed weaker precision (~65%).

---

## Per-Strategy Precision

### Complete Strategy Breakdown

| Strategy | Strategy Name | AI 1s | Human 1s | Human 0s | Precision |
|---|---|---|---|---|---|
| strat_1 | Assess for readiness and identify barriers and facilitators | 4 | 0 | 4 | **0.0%** |
| strat_2 | Audit and provide feedback | 5 | 3 | 2 | 60.0% |
| strat_3 | Conduct cyclical small tests of change | 2 | 2 | 0 | 100.0% |
| strat_4 | Conduct local needs assessment | 9 | 3 | 6 | **33.3%** |
| strat_5 | Develop a formal implementation blueprint | 7 | 6 | 1 | 85.7% |
| strat_6 | Develop and implement tools for quality monitoring | 13 | 11 | 2 | 84.6% |
| strat_7 | Develop and organize quality monitoring systems | 9 | 6 | 3 | 66.7% |
| strat_8 | Obtain and use patient/consumer and family feedback | 6 | 6 | 0 | 100.0% |
| strat_9 | Purposefully reexamine the implementation | 9 | 5 | 4 | 55.6% |
| strat_10 | Stage implementation scale up | 8 | 1 | 7 | **12.5%** |
| strat_11 | Centralize technical assistance | 5 | 4 | 1 | 80.0% |
| strat_12 | Facilitation | 4 | 2 | 2 | 50.0% |
| strat_13 | Provide clinical supervision | 1 | 0 | 1 | 0.0% |
| strat_14 | Provide local technical assistance | 4 | 4 | 0 | 100.0% |
| strat_15 | Promote adaptability | 4 | 3 | 1 | 75.0% |
| strat_16 | Tailor strategies | 10 | 8 | 2 | 80.0% |
| strat_17 | Use data experts | 6 | 5 | 1 | 83.3% |
| strat_18 | Use data warehousing techniques | 3 | 2 | 1 | 66.7% |
| strat_19 | Build a coalition | 7 | 5 | 2 | 71.4% |
| strat_21 | Conduct local consensus discussions | 4 | 4 | 0 | 100.0% |
| strat_23 | Develop and/or leveraging academic partnerships | 15 | 11 | 4 | 73.3% |
| strat_27 | Involve executive boards | 3 | 3 | 0 | 100.0% |
| strat_29 | Obtain formal commitments | 4 | 4 | 0 | 100.0% |
| strat_30 | Organize clinician implementation team meetings | 3 | 3 | 0 | 100.0% |
| strat_31 | Promote network weaving | 1 | 1 | 0 | 100.0% |
| strat_32 | Recruit, designate and train for leadership | 2 | 1 | 1 | 50.0% |
| strat_33 | Use advisory boards and workgroups | 3 | 3 | 0 | 100.0% |
| strat_34 | Visit other sites | 1 | 0 | 1 | 0.0% |
| strat_35 | Use an implementation advisor | 4 | 2 | 2 | 50.0% |
| strat_36 | Conduct educational meetings | 4 | 3 | 1 | 75.0% |
| strat_37 | Conduct educational outreach visits | 1 | 1 | 0 | 100.0% |
| strat_38 | Conduct ongoing training | 2 | 2 | 0 | 100.0% |
| strat_40 | Develop educational materials | 14 | 13 | 1 | 92.9% |
| strat_41 | Distribute educational materials | 14 | 14 | 0 | **100.0%** |
| strat_43 | Provide ongoing consultation | 5 | 4 | 1 | 80.0% |
| strat_45 | Use train-the-trainer strategies | 1 | 1 | 0 | 100.0% |
| strat_46 | Work with educational institutions | 1 | 1 | 0 | 100.0% |
| strat_47 | Create new clinical teams | 2 | 2 | 0 | 100.0% |
| strat_48 | Develop resource sharing agreements | 9 | 6 | 3 | 66.7% |
| strat_49 | Facilitate relay of clinical data to providers | 4 | 3 | 1 | 75.0% |
| strat_50 | Remind clinicians | 2 | 2 | 0 | 100.0% |
| strat_51 | Revise professional roles | 10 | 9 | 1 | 90.0% |
| strat_52 | Increase demand | 1 | 1 | 0 | 100.0% |
| strat_53 | Intervene with patients/consumers to enhance uptake and adherence | 16 | 16 | 0 | **100.0%** |
| strat_54 | Involve patients/consumers and family members | 5 | 5 | 0 | 100.0% |
| strat_55 | Prepare patients/consumers to be active participants | 6 | 6 | 0 | 100.0% |
| strat_56 | Use mass media | 3 | 3 | 0 | 100.0% |
| strat_57 | Access new funding | 18 | 2 | 16 | **11.1%** |
| strat_59 | Alter patient/consumer fees | 4 | 4 | 0 | 100.0% |
| strat_60 | Develop disincentives | 1 | 0 | 1 | 0.0% |
| strat_61 | Fund and contract for clinical innovation | 1 | 0 | 1 | 0.0% |
| strat_62 | Make billing easier | 1 | 0 | 1 | 0.0% |
| strat_65 | Use other payment schemes | 1 | 1 | 0 | 100.0% |
| strat_69 | Change record systems | 7 | 5 | 2 | 71.4% |
| strat_70 | Change service sites | 13 | 7 | 6 | **53.8%** |
| strat_71 | Create or change credentialing and/or licensing standards | 1 | 0 | 1 | 0.0% |
| strat_72 | Mandate change | 2 | 2 | 0 | 100.0% |
| strat_73 | Start a dissemination organization | 1 | 1 | 0 | 100.0% |

---

### Top 10 Most Over-Coded Strategies (Lowest Precision)

These strategies are where the AI most frequently misidentified presence. They represent the highest-priority targets for prompt engineering improvements.

| Rank | Strategy | Name | Precision | Confirmed / Flagged |
|---|---|---|---|---|
| 1 | strat_1 | Assess for readiness and identify barriers and facilitators | **0.0%** | 0 / 4 |
| 2 | strat_57 | Access new funding | **11.1%** | 2 / 18 |
| 3 | strat_10 | Stage implementation scale up | **12.5%** | 1 / 8 |
| 4 | strat_4 | Conduct local needs assessment | **33.3%** | 3 / 9 |
| 5 | strat_12 | Facilitation | **50.0%** | 2 / 4 |
| 6 | strat_32 | Recruit, designate and train for leadership | **50.0%** | 1 / 2 |
| 7 | strat_35 | Use an implementation advisor | **50.0%** | 2 / 4 |
| 8 | strat_70 | Change service sites | **53.8%** | 7 / 13 |
| 9 | strat_9 | Purposefully reexamine the implementation | **55.6%** | 5 / 9 |
| 10 | strat_2 | Audit and provide feedback | **60.0%** | 3 / 5 |

> [!WARNING]
> **strat_57 (Access new funding)** is a critical outlier — the AI flagged it 18 times but humans confirmed only 2 (11.1% precision). The AI systematically misinterprets standard grant funding acknowledgments as a deliberate "implementation strategy." This alone accounts for **16 of the 85 total false positives (18.8%).**

> [!NOTE]
> **strat_1 (Assess for readiness)** had 0% precision — the AI confused patient-level assessments and community engagement processes with organizational-level readiness assessments, which is the correct interpretation per the codebook.

---

### Top 10 Most Accurate Strategies (Highest Precision, ≥2 occurrences)

| Rank | Strategy | Name | Precision | Confirmed / Flagged |
|---|---|---|---|---|
| 1 | strat_3 | Conduct cyclical small tests of change | **100.0%** | 2 / 2 |
| 2 | strat_8 | Obtain and use patient/consumer and family feedback | **100.0%** | 6 / 6 |
| 3 | strat_14 | Provide local technical assistance | **100.0%** | 4 / 4 |
| 4 | strat_21 | Conduct local consensus discussions | **100.0%** | 4 / 4 |
| 5 | strat_27 | Involve executive boards | **100.0%** | 3 / 3 |
| 6 | strat_29 | Obtain formal commitments | **100.0%** | 4 / 4 |
| 7 | strat_30 | Organize clinician implementation team meetings | **100.0%** | 3 / 3 |
| 8 | strat_33 | Use advisory boards and workgroups | **100.0%** | 3 / 3 |
| 9 | strat_38 | Conduct ongoing training | **100.0%** | 2 / 2 |
| 10 | strat_41 | Distribute educational materials | **100.0%** | 14 / 14 |

> [!TIP]
> **strat_53 (Intervene with patients/consumers)** had a perfect 100% precision across all 16 identifications — the highest-volume perfect strategy. **strat_41 (Distribute educational materials)** was also perfect at 14/14. These concrete, action-oriented strategies are where the AI performs best.

---

## Per-Paper Precision

### Complete Paper Breakdown

| ID | Author | AI 1s | Human 1s | Human 0s | Precision |
|---|---|---|---|---|---|
| 3528 | Kim | 19 | 15 | 4 | 78.9% |
| 3934 | Venishetty | 11 | 10 | 1 | 90.9% |
| 3936 | Farley | 7 | 5 | 2 | 71.4% |
| 3971 | Kruse | 6 | 4 | 2 | 66.7% |
| 3974 | Shareef | 12 | 10 | 2 | 83.3% |
| 3987 | Nuno | 7 | 6 | 1 | 85.7% |
| 3994 | Ghosh | 23 | 18 | 5 | 78.3% |
| 4025 | Champion | 2 | 2 | 0 | **100.0%** |
| 4036 | McAtee | 9 | 6 | 3 | 66.7% |
| 4052 | Gautom | 16 | 10 | 6 | 62.5% |
| 4068 | Yan | 9 | 7 | 2 | 77.8% |
| 4069 | Glasser | 19 | 17 | 2 | **89.5%** |
| 4115 | Walker | 3 | 2 | 1 | 66.7% |
| 4202 | Coronado | 11 | 7 | 4 | 63.6% |
| 4247 | Coronado | 11 | 8 | 3 | 72.7% |
| 4258 | Mehta | 8 | 4 | 4 | 50.0% |
| 4503 | McCann | 7 | 6 | 1 | 85.7% |
| 4519 | EspinozaSalomon | 9 | 4 | 5 | **44.4%** |
| 4520 | Radtke | 10 | 8 | 2 | 80.0% |
| 4545 | TangkaFKL | 11 | 8 | 3 | 72.7% |
| 4617 | Hammarlund | 4 | 2 | 2 | 50.0% |
| 4647 | Samuel-Hodge | 20 | 17 | 3 | 85.0% |
| 4674 | HudakKMA | 4 | 2 | 2 | 50.0% |
| 4684 | Thakur | 21 | 15 | 6 | 71.4% |
| 4701 | Katz | 14 | 9 | 5 | 64.3% |
| 4727 | Jelalian | 4 | 2 | 2 | 50.0% |
| 4746 | Llavona-Ortiz | 8 | 7 | 1 | 87.5% |
| 4811 | Bowen | 11 | 5 | 6 | **45.5%** |
| 4890 | Ung | 4 | 3 | 1 | 75.0% |
| 5032 | Burgermaster | 7 | 3 | 4 | **42.9%** |

---

### 5 Most Problematic Papers (Lowest Precision)

| Rank | Author (ID) | Precision | Confirmed / Flagged |
|---|---|---|---|
| 1 | **Burgermaster** (5032) | **42.9%** | 3 / 7 |
| 2 | **EspinozaSalomon** (4519) | **44.4%** | 4 / 9 |
| 3 | **Bowen** (4811) | **45.5%** | 5 / 11 |
| 4 | **Mehta** (4258) | **50.0%** | 4 / 8 |
| 5 | **Hammarlund** (4617) | **50.0%** | 2 / 4 |

### 5 Most Accurate Papers (Highest Precision)

| Rank | Author (ID) | Precision | Confirmed / Flagged |
|---|---|---|---|
| 1 | **Champion** (4025) | **100.0%** | 2 / 2 |
| 2 | **Venishetty** (3934) | **90.9%** | 10 / 11 |
| 3 | **Glasser** (4069) | **89.5%** | 17 / 19 |
| 4 | **Llavona-Ortiz** (4746) | **87.5%** | 7 / 8 |
| 5 | **Nuno** (3987) | **85.7%** | 6 / 7 |

---

## Key Findings & Interpretation

### 1. The AI has a systematic over-coding bias
The AI tends to cast a wider net than human experts. Of its 307 positive identifications, 85 (27.7%) were rejected by human reviewers. The bias is concentrated in a small number of strategies.

### 2. Three strategies drive 34% of all false positives
| Strategy | FP Count | % of Total FPs |
|---|---|---|
| strat_57 (Access new funding) | 16 | 18.8% |
| strat_10 (Stage implementation scale up) | 7 | 8.2% |
| strat_4 (Conduct local needs assessment) | 6 | 7.1% |
| **Subtotal** | **29** | **34.1%** |

Fixing just these three strategies in the prompt engineering would reduce the total false positive count by over a third.

### 3. Concrete strategies outperform abstract ones
Strategies with clear, observable actions (distribute materials, intervene with patients, remind clinicians) achieve near-perfect precision. Abstract strategies requiring professional judgment (readiness assessment, facilitation, staging scale-up) are where the AI struggles most.

### 4. Paper-level precision is consistent
Most papers fall in the 65–90% precision range. Only 3 papers (Burgermaster, EspinozaSalomon, Bowen) fall below 50%, and these tend to have more ambiguous or multi-faceted implementations.

---

## Limitations

> [!CAUTION]
> **Recall (sensitivity) was not evaluated.** The human team only reviewed the 307 cases where the AI coded a strategy as present (1). The 1,883 cases where the AI coded 0 were not independently reviewed. Therefore:
> - We cannot determine how many strategies the AI **missed** (False Negatives)
> - True F1 Score and Cohen's Kappa cannot be computed
> - The AI's **conservative bias** (86% rejection rate) may mask missed strategies
>
> To obtain Recall, a stratified random sample of the AI's 0-coded strategies (~10–15% of 1,883 = ~190–280 cases) would need to be reviewed by the research team.

---

## Summary Statement

> Of the AI pipeline's 307 positive strategy identifications across 30 academic papers, **222 (72.3%) were confirmed** by independent human expert review. The remaining **85 (27.7%) were over-coded**, with the AI systematically misidentifying funding acknowledgments (strat_57), pilot study descriptions (strat_10), and local data citations (strat_4) as deliberate implementation strategies. The AI is conservative overall — it rejected 86% of all possible strategy–paper combinations — but when it does flag a strategy as present, it is correct approximately 72% of the time.
