"""
This script along with the support scritps that come with it, such as the dict_hpot_anno.py, 
is open for public viewing and usage but may not be modified, 
distributed with modifications, or used for commercial purposes without 
explicit permission from the author.

Author: Youssef Abdou
Email: ytabdou@generations-labs.com
Created: 2025-03-02
Version 1.0
Description: This script is used to generate the gene_to_hpo.pkl file.
"""

import pickle

def preprocess_hpo_file(hpo_file):
    gene_to_hpo = {}
    
    with open (hpo_file, "r") as f:
        for line in f:
            if line.startswith("ncbi_gene_id"):
                continue
            ncbi_gene_id, gene_symbol, hpo_id, hpo_name, frequency, disease_id = line.strip().split("\t")
        
            if gene_symbol not in gene_to_hpo:
                gene_to_hpo[gene_symbol] = []        
            gene_to_hpo[gene_symbol].append((hpo_name, hpo_id))
  
    for gene in gene_to_hpo:
        gene_to_hpo[gene] = list(set(gene_to_hpo[gene]))
        
    return gene_to_hpo

def save_hpo_mapping (gene_to_hpo, output_file):
    with open(output_file, "wb") as f:
        pickle.dump(gene_to_hpo, f)
        
hpo_file = "genes_to_phenotype.txt"
output_file = "gene_to_hpo.pkl"

gene_to_hpo = preprocess_hpo_file(hpo_file)
save_hpo_mapping(gene_to_hpo, output_file)

print(f"HPO mapping data has been saved to {output_file}")