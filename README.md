# Automated Implementation Science Strategy Coder (First Run Study)

An enterprise-grade Python data pipeline that leverages the Google Gemini API to perform high-sensitivity coding (presence/absence tagging) of academic research papers against the **73 implementation strategies** of the ERIC (Expert Recommendations for Implementing Change) taxonomy.

This repository contains the source code, validation benchmarks, and outputs representing the **First Run Study** detailed in our accompanying research paper.

---

## 1. Project Overview

Manual extraction of implementation strategies from academic literature is highly resource-intensive and prone to human coder drifting. This project implements a programmatic data pipeline to automate the coding process. By wrapping the LLM in a structured software harness, we establish a transparent, mathematically verifiable, and reproducible tagging standard:
*   **Zero Hallucination Guarantee**: Programmatic exact substring verification ensures that every positive coding (`1`) is accompanied by a verbatim quote that physically exists in the target PDF.
*   **Sensitivity Calibration**: programmatically scores and injects human-coded "neighbor" papers to calibrate target classification thresholds.
*   **High Negative Predictive Value**: Rejects absent strategies with **~95% accuracy**, acting as an efficient screening tool that reduces human coding workloads by ~68%.

---

## 2. Technical Architecture & Data Flow

The system coordinates raw text extractors, dataset parsers, and API managers in a strict sequential sequence:

1.  **Ingestion & Parsing (`src/pdf_extractor.py`)**: Uses `PyMuPDF` to programmatically extract raw text blocks and abstracts from target PDFs.
2.  **Disease Classification (`src/llm_client.py`)**: Classifies the primary disease outcome (e.g., CRC, HPV, Obesity, Diabetes, Asthma, or Multiple) from the abstract.
3.  **Neighborhood Matcher (`src/data_loader.py`)**: Queries the Gold Standard dataset (`imp_strat_final_sort of + clearly2.csv`) to programmatically score and fetch the 3 most similar studies by disease and author to serve as calibration context.
4.  **Structured Semantic Tagging (`src/llm_client.py`)**: Passes definitions directly from the Codebook CSV and queries Gemini using strict `pydantic` schemas to return a structured JSON response (containing Strategy ID, Value Coded 0/1, exact quote, and rationale).
5.  **Mathematical Quote Verification (`src/verifier.py`)**: Performs a literal substring search in the raw PDF text for the returned quote. If a mismatch or hallucination is caught, the verifier rejects the positive coding and programmatically downgrades the value to `0`.

For full step-by-step detail and technical flowchart diagrams, see the **[Architecture and Methodology Report](Outputs/Architecture_and_Methodology.md)**.

---

## 3. Directory Structure

```
├── src/                               # Core pipeline codebase
│   ├── pipeline.py                    # Main pipeline orchestrator
│   ├── data_loader.py                 # Codebook and neighbor matching loader
│   ├── pdf_extractor.py               # PDF parser utilizing PyMuPDF
│   ├── llm_client.py                  # API schemas and Gemini orchestrator
│   └── verifier.py                    # Verification and anti-hallucination engine
│
├── Gold_Standard_Evaluation/          # Benchmarking scripts for the Gold Standard corpus
│   ├── Outputs/                       # Output matrices & logs for Study 1
│   ├── evaluation_pipeline.py         # Benchmarking pipeline execution
│   └── evaluate_metrics.py            # Calculates F1, Kappa, and McNemar metrics
│
├── Imp Strategy Coder_Gold Standard Docs/  # Calibration docs, Codebook CSV, and mapping datasets
├── Imp Strategy Coder_Target Docs/         # 30 raw PDFs used in the Target Precision Audit
├── Outputs/                                # Output tables, reports, and logs
│   └── Firstrun_3_16_2026/            # Coded output matrices & human audits for Study 2
│
├── scratch/                           # Diagnostic and metrics audit scripts
└── combined_validation_report_GoldStandard-FirstRun.md  # Detailed validation report
```

---

## 4. Key Validation Findings

The pipeline was validated through two independent evaluation studies. For full details, see the **[Combined Validation Report](combined_validation_report_GoldStandard-FirstRun.md)**.

### Study 1: Gold Standard Benchmark (N = 69 Papers)
AI predictions were compared cell-by-cell across all 73 strategies against pre-existing human coding, yielding **5,037 total decisions**:
*   **Recall**: **72.9%** (Catches nearly 3 out of 4 truly present strategies).
*   **Negative Predictive Value (NPV)**: **94.8%** (When the AI says a strategy is absent, it is correct ~95% of the time).
*   **Precision**: **26.6%** (Reflects a systematic over-coding bias where the AI flags strategies at 2.7× the human rate; McNemar's p < 0.001).
*   **Cohen's Kappa**: **0.253** (Fair agreement).

### Study 2: Target Precision Audit (N = 30 Papers)
Three researcher pairs audited all **307 positive identifications** generated by the AI on a target library of new papers:
*   **Overall Precision**: **72.3%** (Of all positive predictions, human coders confirmed 222 as correct and rejected 85).
*   **Prevalence**: The AI coded presence at a rate of 14.0%, naturally aligning with the human base rate (12.5%).

---

## 5. Getting Started

### Prerequisites
*   Python 3.9+
*   Dependencies: `pandas`, `pymupdf` (`fitz`), `google-genai`, `scikit-learn`, `python-dotenv`

Install dependencies:
```bash
pip install pandas PyMuPDF google-genai scikit-learn python-dotenv
```

### Environment Configuration
Export your Google Gemini API key as an environment variable or define it in a `.env` file at the project root:
```bash
# In your terminal (Windows PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"
```

### Running the Pipeline
To run the coding pipeline on target documents:
```bash
python src/pipeline.py
```

To run benchmarking metrics on the Gold Standard corpus:
```bash
python Gold_Standard_Evaluation/evaluate_metrics.py
```
