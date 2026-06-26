import os
import logging
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

logger = logging.getLogger(__name__)

# The user must have GEMINI_API_KEY exported in their environment.
# Initialize Gemini Client
client = genai.Client()

# Human-In-The-Loop Iterative Alignment removed to revert to first run architecture.

class TargetMetadata(BaseModel):
    primary_disease: str = Field(description="The primary disease outcome in the target paper (options: colorectal cancer(CRC), cervical cancer(HPV), diabetes, obesity, asthma, or multiple chronic diseases). Must be one of these exact strings.")

class StrategyCoding(BaseModel):
    Strategy_ID: str = Field(description="The exact strategy ID from the Codebook (e.g. strat_1)")
    Value_Coded: int = Field(description="0 for Absence, 1 for Presence as per Strict Coding Thresholds")
    Quote_Text: str = Field(description="A verbatim exact quote from the text that explicitly justifies a 1. MUST BE EXTRACTED EXACTLY AS WRITTEN IN THE TEXT. If Value_Coded is 0, leave empty or put 'N/A'.")
    Rationale: str = Field(description="A 1-sentence explanation of why the evidence fits the definition. If Value_Coded is 0, provide a 1-sentence explanation of why the strategy is considered absent (e.g., 'No evidence found', 'Standard clinical care').")

class ClusterAnalysisResponse(BaseModel):
    codings: list[StrategyCoding]

def analyze_target_disease(pdf_text):
    if not client:
        raise ValueError("Gemini Client not initialized.")
    prompt = "Read the abstract and introduction of this paper. Identify the primary disease outcome from these options ONLY: colorectal cancer(CRC), cervical cancer(HPV), diabetes, obesity, asthma, or multiple chronic diseases.\n\nText:\n" + pdf_text[:10000]
    
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TargetMetadata,
            temperature=0.0
        ),
    )
    return response.parsed

def analyze_paper_cluster(pdf_text, cluster_strategies, neighborhood_context):
    if not client:
        raise ValueError("Gemini Client not initialized.")
        
    strat_defs_str = "\n".join([f"- ID: {s['Strategy_ID']} | Name: {s['Strategy name']} | Definition: {s['Strategy definition (extended)']}" 
                                for s in cluster_strategies])
                                
    # Guardrails removed for first-run rollback

    prompt = f"""
You are an expert Implementation Science methodology coder. 
You are evaluating an academic paper to determine the presence (1) or absence (0) of specific Implementation Strategies.
You must adhere strictly to the provided definitions. Avoid "functional equivalence" drifting.

TARGET PAPER TEXT (Excerpt):
========================================
{pdf_text}
========================================

YOUR TASK is to evaluate the following Implementation Strategies against the target paper:
{strat_defs_str}

NEIGHBORHOOD BASELINE (Examples from Similar Papers):
The target paper is medically or structurally similar to the following Gold Standard papers, which were human-coded. Use them to calibrate your sensitivity threshold for what counts as a '1'.
{neighborhood_context}

RULES:
1. Strict Construction: Only code a 1 if the text describes a deliberate implementation strategy used to facilitate the intervention. Do not code 1 for activities that are part of the clinical protocol.
2. Default to 0: If evidence is ambiguous, default to 0.
3. Functional Equivalence: Do not wait for a verbatim strategy name. If a paper describes an activity fulfilling the definition, code it as 1.
4. Zero Hallucination: A '1' must have a DIRECT, VERBATIM quote from the text. DO NOT SUMMARIZE THE QUOTE. Copy it exactly as it appears in the text.

Evaluate the following full paper text and output the JSON array of your coding for the requested strategies:

PAPER TEXT:
{pdf_text}
"""
    
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ClusterAnalysisResponse,
            temperature=0.0
        ),
    )
    return response.parsed, prompt
