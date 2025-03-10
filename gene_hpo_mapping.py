"""
This script is open for public viewing and usage but may not be modified, 
distributed with modifications, or used for commercial purposes without 
explicit permission from the author.

Author: Youssef Abdou
Email: ytabdou@generations-labs.com
Created: 2025-03-02
Version 1.0
Description: 
This script is intended to either simply map a TSV list of genes to the appropriate 
HPO terms and Id's or do that from a TSV files of annotated variants and then merge the HPO mappings 
back to the TSV file of annotated variants. This script should be used along with gene_to_phenotype.txt and
gene_to_hpo.pkl. If an updated gene_to_hpo.txt mapping source file is used, please use the
dict_hpo_anno.py script to regenerate the gene_to_hpo.pkl file. If you would like to use the TSV
file truncation option, please adjust the column values according to your needs.
"""


import pickle
import os
import csv
import pandas as pd

# Load preprocessed data
def load_hpo_mapping(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return None

    with open(file_path, "rb") as f:
        data = pickle.load(f)
        if data is None:
            print("Error: The pickle file is empty or corrupted.")
        return data

# Read gene list from TSV
def read_gene_list_from_tsv(tsv_file_path):
    gene_list = []
    try:
        with open(tsv_file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Avoid empty rows
                    gene_list.append(row[0])  # Assuming the gene names are in the first column
    except FileNotFoundError:
        print(f"Error: The file {tsv_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the TSV file: {e}")
    return gene_list

# Example batch processing
def process_genes(gene_to_hpo, gene_list, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['Gene', 'HPO Terms', 'HPO IDs'])  # Write header

        for gene in gene_list:
            if gene in gene_to_hpo:
                hpo_data = gene_to_hpo[gene]

                # Debugging: Print hpo_data to see its structure
                #print(f"Processing {gene}: {hpo_data}")

                if isinstance(hpo_data, list):
                    # Correct extraction of HPO terms (names) and IDs
                    hpo_terms = ', '.join([hpo_name for hpo_name, _ in hpo_data])
                    hpo_ids = ', '.join([hpo_id for _, hpo_id in hpo_data])
                    writer.writerow([gene, hpo_terms, hpo_ids])  # Write gene, HPO terms, and HPO IDs
                else:
                    writer.writerow([gene, "Invalid data format", "N/A"])
            else:
                writer.writerow([gene, "No HPO terms found", "N/A"])
                

def get_hpo_info(gene):
    gene_to_hpo = load_hpo_mapping("gene_to_hpo.pkl")
    
    if gene in gene_to_hpo:
        hpo_ids = ", ".join([hpo[0] for hpo in gene_to_hpo[gene]])
        hpo_terms = ", ".join([hpo[1] for hpo in gene_to_hpo[gene]])
        return pd.Series([hpo_ids, hpo_terms])
    return pd.Series(["N/A", "No HPO terms found"])

# Main script execution
def main():
    while True:
        print ("\nSelect functions to run:")
        print ("1. Annotate list of Genes only")
        print ("2. Annotate genes and merge to original TSV of variants")
        print ("3. Exit")

        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Prompt for TSV file containing gene list
            tsv_file_path = input("Enter the path to the TSV file containing the gene list: ")
                
            gene_list = read_gene_list_from_tsv(tsv_file_path)
            if not gene_list:
                print("No genes found in the TSV file or the file is empty.")
                return

            # Load HPO mapping data
            gene_to_hpo = load_hpo_mapping("gene_to_hpo.pkl")
            
            if gene_to_hpo is not None:
                directory, filename = os.path.split(tsv_file_path)
                name, ext = os.path.splitext(filename)
                
                descriptor = "_mapped_terms"
                
                output_file = os.path.join(directory, f"{name}{descriptor}{ext}")

                process_genes(gene_to_hpo, gene_list, output_file)
                print(f"Processing complete. Results saved to {output_file}")
            else:
                print("Failed to load HPO mapping data.")
            
            break
            
        elif choice == "2":
            variant_file = input("Enter the path to the TSV file containing all variants: ")
            
            variant_df = pd.read_csv(variant_file, dtype=str)
            
            hpo_info = variant_df.iloc[:, 4].apply(get_hpo_info)
            
            hpo_info.columns = ["HPO_Terms", "HPO_ID"]
                        
            for col in hpo_info.columns:
                variant_df.insert(4 + 20, col, hpo_info[col])
                    
            directory, filename = os.path.split(variant_file)
            name, ext = os.path.splitext(filename)
            
            descriptor = "_mapped_terms"
            
            output_file = os.path.join(directory, f"{name}{descriptor}.tsv")
            
            print(f"Processing complete. Results saved to {output_file}")
            
            print("\nWould you like to truncate your merged mapped tsv file?")
            
            truncate = input("input (Y/n)")
            
            if truncate.lower() == "y":
                keep_columns = list(range(0,5)) + [7, 9] + list(range(14,19)) + list(range(20,41))
                filtered_df = variant_df.iloc[:, keep_columns]
                filtered_df.to_csv(output_file, sep="\t", index=False, quoting=3)
            elif truncate.lower() == "n":
                variant_df.to_csv(output_file, sep="\t", index=False, quoting=3)
            else:
                print("Invalid selection! Exiting...")
                break
            
            break

        elif choice == "3":
            print ("Exiting...")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")


if __name__ == "__main__":
    main()