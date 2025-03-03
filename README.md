This script is intended to either simply map a TSV list of genes to the appropriate 
HPO terms and Id's or do that from a TSV files of annotated variants and then merge the HPO mappings 
back to the TSV file of annotated variants. This script should be used along with gene_to_phenotype.txt and
gene_to_hpo.pkl. If an updated gene_to_hpo.txt mapping source file is used, please use the
dict_hpo_anno.py script to regenerate the gene_to_hpo.pkl file. If you would like to use the TSV
file truncation option, please adjust the column values according to your needs.

When using the script, please use full file paths such as, /path/to/your/file.tsv.

The script is set up to output your resulting mapped data to the same location as your primary input file.