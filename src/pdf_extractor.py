import fitz  # PyMuPDF
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFExtractor:
    def __init__(self, filepath):
        self.filepath = filepath

    def extract_full_text(self):
        """
        Extracts all text from the PDF.
        """
        try:
            doc = fitz.open(self.filepath)
            text_blocks = []
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                # Getting blocks helps with order and layout vs just page.get_text()
                # But simple get_text() is usually fine for semantic analysis
                text = page.get_text("text")
                text_blocks.append(text)
            
            doc.close()
            return "\n".join(text_blocks)
        except Exception as e:
            logger.error(f"Error extracting {self.filepath}: {e}")
            return ""

    def get_abstract_or_first_page(self):
        """
        Retrieves just the first page to help the LLM identify the Target Disease.
        """
        try:
            doc = fitz.open(self.filepath)
            if len(doc) > 0:
                first_page_text = doc.load_page(0).get_text("text")
                # Also grab second page just in case abstract spills over
                if len(doc) > 1:
                    first_page_text += "\n" + doc.load_page(1).get_text("text")
                doc.close()
                return first_page_text
            return ""
        except Exception as e:
            logger.error(f"Error reading {self.filepath}: {e}")
            return ""

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        extractor = PDFExtractor(sys.argv[1])
        print("First 500 chars:", extractor.extract_full_text()[:500])
