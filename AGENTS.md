# Agent Guidelines & Rules: Automated Implementation Science Review Pipeline

Welcome! You are an AI Agent assisting researchers or developers in this workspace. This document serves as your system rules and project-scoped directive. Please read and ingest this context immediately before writing code or running executions.

---

## 1. Project Context & Purpose

The codebase implements a programmatic Python data pipeline mapping academic papers to the 73 implementation strategies in the ERIC taxonomy. The pipeline runs locally and uses the Gemini API (`gemini-2.5-pro` / `gemini-3.5-flash`) for extraction. 

Your main goal when modifying code or assisting in this workspace is to preserve the integrity of the **First Run baseline architecture** (relying on structured schemas, neighborhood calibration baselines, and mathematical verification).

---

## 2. Strict Coding Thresholds (Verification Guardrails)

You must strictly adhere to the following rules, which reflect the human coding thresholds (the "Gold Standard") used in the study:

### Rule 1: Strict Construction (Clinical vs. Implementation)
Only code a strategy as present (`1`) if the text describes a **deliberate implementation strategy** used to facilitate or support the intervention.
*   **Absence (`0`)**: Activities that are part of the clinical protocol, standard patient care, or standard research study methodology (e.g. data collection).
*   **Presence (`1`)**: Deliberate efforts to train, prepare, incentivize, facilitate, or structure clinic staff or infrastructure to deliver the intervention.

### Rule 2: Default to 0
If the text is ambiguous, or if it is unclear whether an activity is standard care or an implementation strategy, **default to `0`**.

### Rule 3: Zero Hallucination (Direct Quotes)
A `1` coding must have a **direct, verbatim quote** extracted exactly as written from the PDF text. Do not summarize, rephrase, or correct typographical errors in the quote. The programmatic verification engine (`src/verifier.py`) performs an exact, case-insensitive substring search. Any modification of the quote will fail verification and result in a system downgrade to `0`.

### Rule 4: Functional Equivalence
Do not wait for a verbatim strategy name. If a paper describes an activity that fulfills the Codebook definition, code it as `1`.

---

## 3. Core Sources of Truth

*   **The Codebook (`Imp Strategy Coder_Gold Standard Docs/Imp strategy codebook_updated 3-12-26.csv`)**: The absolute source of truth for strategy variable names (e.g., `strat_1` to `strat_73`), cluster numbers (1 to 9), strategy names, and extended definitions.
*   **The Mapping Dataset (`Imp Strategy Coder_Gold Standard Docs/imp_strat_final_sort of + clearly2.csv`)**: The source of truth for calibration. It contains the binary matrices of the 70 human-coded Gold Standard papers.

---

## 4. Operational Instructions for Modifying Code

*   **No numeric or sequence drifting**: Before mapping variables or returning JSON responses, verify the index against the Codebook row. Explicitly check that `strat_11` is *Centralize technical assistance* (or *Provide local technical assistance* depending on the exact codebook row) and `strat_12` is *Facilitation*. Do not guess indexes from pre-existing knowledge.
*   **Check workspace imports**: Ensure any modification preserves class structures inside the core package (`src/pipeline.py`, `src/data_loader.py`, `src/pdf_extractor.py`, `src/llm_client.py`, `src/verifier.py`).
*   **Verify-First Protocol**: Before declaring any coding, data extraction, or programmatic change "complete," run the test suite and benchmarking metrics:
    ```bash
    # Run pipeline check
    python src/pipeline.py
    
    # Run Gold Standard metrics calculation
    python Gold_Standard_Evaluation/evaluate_metrics.py
    ```
