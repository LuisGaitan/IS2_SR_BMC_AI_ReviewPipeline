import os
import glob
import pandas as pd
from data_loader import DataLoader
from pdf_extractor import PDFExtractor
from llm_client import analyze_target_disease, analyze_paper_cluster
import logging

logger = logging.getLogger(__name__)

def main():
    # Paths
    CODEBOOK_PATH = "../Imp Strategy Coder_Gold Standard Docs/Imp strategy codebook_updated 3-12-26.csv"
    MAPPING_PATH = "../Imp Strategy Coder_Gold Standard Docs/imp_strat_final_sort of + clearly2.csv"
    TARGET_DIR = "../Imp Strategy Coder_Target Docs"
    OUTPUT_DIR = "../Outputs"
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Configure logging to save to file and print to console
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(OUTPUT_DIR, "pipeline_execution.log"), mode='w', encoding='utf-8'),
            logging.StreamHandler()
        ],
        force=True
    )
    
    # 1. Initialize DataLoader
    dl = DataLoader(CODEBOOK_PATH, MAPPING_PATH)
    clusters = dl.get_all_clusters()
    
    target_pdfs = glob.glob(os.path.join(TARGET_DIR, "*.pdf"))
    
    all_codings = [] # for table 1 (quotes)
    matrix_rows = [] # for table 2 (binary matrix)
    
    for pdf_path in target_pdfs:
        filename = os.path.basename(pdf_path)
        # Parse "Alicea-Planas_3494.pdf" -> Author: "Alicea-Planas", ID: "3494"
        name_parts = filename.replace(".pdf", "").split("_")
        author = name_parts[0] if len(name_parts) > 0 else "Unknown"
        cov_id = name_parts[1] if len(name_parts) > 1 else "Unknown"
        
        logger.info(f"========== Processing: {filename} ==========")
        
        # 2. Extract PDF
        extractor = PDFExtractor(pdf_path)
        full_text = extractor.extract_full_text()
        first_page = extractor.get_abstract_or_first_page()
        
        if not full_text:
            logger.error(f"Failed to extract text for {filename}. Skipping.")
            continue
            
        # 3. LLM: Identify Target Disease
        try:
            disease_meta = analyze_target_disease(first_page)
            target_disease = disease_meta.primary_disease
            logger.info(f"  Target Disease Identified: {target_disease}")
        except Exception as e:
            logger.error(f"Failed to classify disease for {filename}: {e}")
            target_disease = "Multiple diseases" # Fallback
            
        # 4. Find Neighbors (The Neighborhood Rule)
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
            
        # 5. Process by Cluster
        for cluster in clusters:
            cluster_num = cluster['Cluster number']
            logger.info(f"  Analyzing Cluster {cluster_num}: {cluster['Cluster name']}")
            strategies = dl.get_strategies_for_cluster(cluster_num)
            
            # Send to LLM
            try:
                response, prompt = analyze_paper_cluster(full_text, strategies, neighbor_str)
            except Exception as e:
                logger.error(f"LLM Error on {filename} cluster {cluster_num}: {e}")
                continue
                
            for coding_obj in response.codings:
                coding = coding_obj.model_dump()
                # Store matrix result regardless of 0 or 1
                row_dict[coding['Strategy_ID']] = coding['Value_Coded']
                
                strat_name = next((s['Strategy name'] for s in strategies if s['Strategy_ID'] == coding['Strategy_ID']), "Unknown")
                
                # Consolidate row for Table 1
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

    # 6. Save Outputs
    if all_codings:
        table1_df = pd.DataFrame(all_codings)
        table1_df.to_csv(os.path.join(OUTPUT_DIR, "Output_Table_1_Quotes.csv"), index=False)
        logger.info("Saved Output_Table_1_Quotes.csv")
        
    if matrix_rows:
        table2_df = pd.DataFrame(matrix_rows)
        # Ensure ID, Author, Disease are first, followed by strat_1 to strat_73 sorted
        # For simplicity, just letting Pandas order them based on dict insertion
        table2_df.to_csv(os.path.join(OUTPUT_DIR, "Output_Table_2_Binary_Matrix.csv"), index=False)
        logger.info("Saved Output_Table_2_Binary_Matrix.csv")
    
    logger.info("Pipeline Complete!")

if __name__ == "__main__":
    import os
    if "GEMINI_API_KEY" not in os.environ:
        logger.error("You MUST set the GEMINI_API_KEY environment variable to run this script.")
        logger.error("Example: $env:GEMINI_API_KEY='your_key' (PowerShell)")
    else:
        main()
