import re
import logging

logger = logging.getLogger(__name__)

class QuoteVerifier:
    @staticmethod
    def verify_quote(quote, pdf_text):
        """
        Takes the exact quote returned by the LLM and mathematically verifies it exists
        within the raw extracted PDF text. 
        Returns True if verified, False if hallucinated.
        """
        if not quote or str(quote).strip() == "":
            return False
            
        # Clean up basic whitespace differences (LLMs sometimes compress multiple spaces or newlines)
        normalized_quote = re.sub(r'\s+', ' ', quote).strip().lower()
        normalized_pdf = re.sub(r'\s+', ' ', pdf_text).lower()
        
        if normalized_quote in normalized_pdf:
            return True
            
        # If strict substring fails, try stripping punctuation due to edge case tokenization 
        strip_quote = re.sub(r'[^\w\s]', '', normalized_quote)
        strip_pdf = re.sub(r'[^\w\s]', '', normalized_pdf)
        
        if strip_quote in strip_pdf and len(strip_quote) > 10:
             return True
             
        return False
        
    @staticmethod
    def enforce_anti_hallucination(strategy_codings, pdf_text):
        """
        Iterates over the StrategyCodings returned by the LLM. 
        If a coding is a 1, mathematically verifies the quote.
        If the quote hallucinates, downgrades the coding to a 0. 
        Returns the sanitized results as a list of dictionaries with Verification_Status.
        """
        sanitized_dicts = []
        for coding in strategy_codings:
            coding_dict = coding.model_dump()
            if coding_dict['Value_Coded'] == 1:
                is_verified = QuoteVerifier.verify_quote(coding_dict['Quote_Text'], pdf_text)
                if not is_verified:
                    logger.warning(f"HALLUCINATION REJECTED: Strategy {coding_dict['Strategy_ID']}. Quote: '{coding_dict['Quote_Text']}'")
                    # Downgrade to 0
                    coding_dict['Value_Coded'] = 0
                    # We intentionally leave coding_dict['Quote_Text'] intact so researchers can transparently
                    # audit what the LLM hallucinated, rather than overwriting it with a generic error string.
                    coding_dict['Rationale'] = "SYSTEM REJECTION: The LLM hallucinated this quote, which could not be found in the source PDF text."
                    coding_dict['Verification_Status'] = "System_Rejected_Hallucination"
                else:
                    coding_dict['Verification_Status'] = "Verified_Match"
            else:
                coding_dict['Verification_Status'] = "LLM_Determined_Absent"
            
            sanitized_dicts.append(coding_dict)
            
        return sanitized_dicts
