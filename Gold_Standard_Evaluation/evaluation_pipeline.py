import os
import sys
import glob
import pandas as pd
import logging

# Add src to path so we can import the original modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_loader import DataLoader
from pdf_extractor import PDFExtractor
from llm_client import analyze_target_disease, analyze_paper_cluster

logger = logging.getLogger(__name__)

def main():
    # Paths updated to point exactly where requested
    CODEBOOK_PATH = "../Imp Strategy Coder_Gold Standard Docs/Imp strategy codebook_updated 3-12-26.csv"
    MAPPING_PATH = "../Imp Strategy Coder_Gold Standard Docs/imp_strat_final_sort of + clearly2.csv"
    
    # Run ON the Gold Standard docs themselves
    TARGET_DIR = "../Imp Strategy Coder_Gold Standard Docs"
    
    # Save outputs to our new isolated folder
    OUTPUT_DIR = "Outputs"
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(OUTPUT_DIR, "pipeline_execution.log"), mode='w', encoding='utf-8'),
            logging.StreamHandler()
        ],
        force=True
    )
    
    dl = DataLoader(CODEBOOK_PATH, MAPPING_PATH)
    clusters = dl.get_all_clusters()
    
    target_pdfs = glob.glob(os.path.join(TARGET_DIR, "*.pdf"))
    
    all_codings = [] 
    matrix_rows = [] 
    
    for count, pdf_path in enumerate(target_pdfs, 1):
        filename = os.path.basename(pdf_path)
        name_parts = filename.replace(".pdf", "").split("_")
        author = name_parts[0] if len(name_parts) > 0 else "Unknown"
        cov_id = name_parts[1] if len(name_parts) > 1 else "Unknown"
        
        logger.info(f"========== Processing {count}/{len(target_pdfs)}: {filename} ==========")
        
        extractor = PDFExtractor(pdf_path)
        full_text = extractor.extract_full_text()
        first_page = extractor.get_abstract_or_first_page()
        
        if not full_text:
            logger.error(f"Failed to extract text for {filename}. Skipping.")
            continue
            
        try:
            disease_meta = analyze_target_disease(first_page)
            target_disease = disease_meta.primary_disease
            logger.info(f"  Target Disease Identified: {target_disease}")
        except Exception as e:
            logger.error(f"Failed to classify disease for {filename}: {e}")
            target_disease = "Multiple diseases"
            
        neighbors = dl.find_neighbors(target_disease, author, n_neighbors=3)
        neighbor_str = ""
        for n in neighbors:
            neighbor_str += f"- Cov_ID {n['Cov_ID']} by {n['Author']} (Disease: {n['Disease']})\n"
            
        logger.info(f"  Neighborhood Baseline: \n{neighbor_str}")
            
        row_dict = {
            "ID": cov_id,
            "Author last name": author,
            "Target disease": target_disease
        }
            
        for cluster in clusters:
            cluster_num = cluster['Cluster number']
            logger.info(f"  Analyzing Cluster {cluster_num}: {cluster['Cluster name']}")
            strategies = dl.get_strategies_for_cluster(cluster_num)
            
            try:
                response, prompt = analyze_paper_cluster(full_text, strategies, neighbor_str)
            except Exception as e:
                logger.error(f"LLM Error on {filename} cluster {cluster_num}: {e}")
                continue
                
            for coding_obj in response.codings:
                coding = coding_obj.model_dump()
                row_dict[coding['Strategy_ID']] = coding['Value_Coded']
                
                strat_name = next((s['Strategy name'] for s in strategies if s['Strategy_ID'] == coding['Strategy_ID']), "Unknown")
                
                output_record = {
                    "ID number": cov_id,
                    "Author last name": author,
                    "Variable name": coding['Strategy_ID'],
                    "Strategy name": strat_name,
                    "Coded Value": coding['Value_Coded'],
                    "Textual Evidence": coding['Quote_Text'],
                    "Rationale": coding['Rationale']
                }
                
                if coding['Value_Coded'] == 1:
                    all_codings.append(output_record)
                    
        matrix_rows.append(row_dict)
        
        # Incremental save added to prevent data loss on long runs
        pd.DataFrame(all_codings).to_csv(os.path.join(OUTPUT_DIR, "Output_Table_1_Quotes.csv"), index=False)
        pd.DataFrame(matrix_rows).to_csv(os.path.join(OUTPUT_DIR, "Output_Table_2_Binary_Matrix.csv"), index=False)

    logger.info("Pipeline Complete!")

if __name__ == "__main__":
    if "GEMINI_API_KEY" not in os.environ:
        logger.error("You MUST set the GEMINI_API_KEY environment variable to run this script.")
    else:
        main()
