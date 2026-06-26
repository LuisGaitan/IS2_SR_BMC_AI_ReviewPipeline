import pandas as pd
import pathlib
import os

class DataLoader:
    def __init__(self, codebook_path, mapping_dataset_path):
        self.codebook_path = codebook_path
        self.mapping_dataset_path = mapping_dataset_path
        
        # Load Codebook (fixing the space in the headers if present)
        self.codebook_df = pd.read_csv(self.codebook_path, encoding='cp1252')
        self.codebook_df.columns = [c.strip() for c in self.codebook_df.columns]
        
        # Load Mapping Dataset
        self.mapping_df = pd.read_csv(self.mapping_dataset_path, encoding='utf-8')
        
    def get_strategies_for_cluster(self, cluster_number):
        """Returns a list of dicts with strategy details for a given cluster."""
        cluster_data = self.codebook_df[self.codebook_df['Cluster number'] == cluster_number]
        strategies = []
        for _, row in cluster_data.iterrows():
            strategies.append({
                'Strategy_ID': row['Strategy_ID'],
                'Strategy name': row['Strategy name'],
                'Strategy definition (brief)': row['Strategy definition (brief)'],
                'Strategy definition (extended)': row['Strategy definition (extended)']
            })
        return strategies
    
    def get_all_clusters(self):
        """Returns unique cluster numbers and their names."""
        clusters = self.codebook_df[['Cluster number', 'Cluster name']].drop_duplicates()
        return clusters.to_dict('records')

    def find_neighbors(self, target_disease, target_author, n_neighbors=3):
        """
        Finds the closest neighbors based on Disease match, then Author match.
        """
        # Copy to avoid SettingWithCopyWarning
        df = self.mapping_df.copy()
        
        # Calculate a simple match score
        df['match_score'] = 0
        df.loc[df['Disease'].str.contains(target_disease, case=False, na=False), 'match_score'] += 2
        
        if target_author:
            # If author matches, it gets an additional point
            df.loc[df['Author'].str.contains(target_author, case=False, na=False), 'match_score'] += 1
            
        # Sort by match_score descending
        df_sorted = df.sort_values(by='match_score', ascending=False)
        
        # Return top N Cov_IDs and their authors/diseases
        top_neighbors = df_sorted.head(n_neighbors)[['Cov_ID', 'Author', 'Disease', 'match_score']]
        return top_neighbors.to_dict('records')

    def get_high_activity_papers_for_cluster(self, cluster_number, n_papers=3):
        """
        Identify n papers with the highest density of 1s across the strategies for a given cluster.
        """
        cluster_strategies = [s['Strategy_ID'] for s in self.get_strategies_for_cluster(cluster_number)]
        
        df = self.mapping_df.copy()
        # Ensure columns exist in mapping dataset
        valid_cols = [c for c in cluster_strategies if c in df.columns]
        
        df['cluster_ones_count'] = df[valid_cols].sum(axis=1)
        df_sorted = df.sort_values(by='cluster_ones_count', ascending=False)
        
        top_papers = df_sorted.head(n_papers)[['Cov_ID', 'Author', 'Disease', 'cluster_ones_count']]
        return top_papers.to_dict('records')

if __name__ == "__main__":
    # Simple test
    cb_path = "../Imp Strategy Coder_Gold Standard Docs/Imp strategy codebook_updated 3-12-26.csv"
    md_path = "../Imp Strategy Coder_Gold Standard Docs/imp_strat_final_sort of + clearly2.csv"
    if os.path.exists(cb_path) and os.path.exists(md_path):
        dl = DataLoader(cb_path, md_path)
        print("Clusters:", dl.get_all_clusters())
        print("Cluster 1 Strategies:", [s['Strategy_ID'] for s in dl.get_strategies_for_cluster(1)])
        print("Neighbors for 'Asthma':", dl.find_neighbors("Asthma", ""))
        print("High activity for Cluster 1:", dl.get_high_activity_papers_for_cluster(1))
