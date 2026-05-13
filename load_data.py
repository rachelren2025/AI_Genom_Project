"""
load_data.py:
    Loads the raw LINCS L1000 gene expression dataset, filters to the 978
    directly measured landmark genes, attaches compound names to each
    experimental profile, and saves the result as a CSV file.
 
Input files required (must be in the same directory):
    Note: we provide all of these downloaded files in the google drive link on the README page
    
    - GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06.gctx
        The main gene expression matrix in binary GCTx format.
        Download from: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE70138
 
    - GSE70138_Broad_LINCS_gene_info_2017-03-06.txt
        Gene metadata file. Contains a column 'pr_is_lm' that flags
        which genes are landmark genes (1 = landmark, 0 = inferred).
        Download from the same GEO accession above.
 
    - GSE70138_Broad_LINCS_sig_info_2017-03-06.txt
        Signature metadata file. Maps each experiment code (sig_id)
        to a compound name (pert_iname).
        Download from the same GEO accession above.
 
Output files:
    - lincs_landmark_with_compounds.csv
        A CSV where rows are experiments, columns are the 978 landmark
        genes plus a 'compound_name' column. Used as input to preprocess.py.
 
Dependencies:
    - pandas
    - cmapPy  (install with: pip install cmapPy)
 
Usage:
    python3 load_data.py
"""

import pandas as pd
from cmapPy.pandasGEXpress.parse import parse

# Load metadata
gene_info = pd.read_csv("GSE70138_Broad_LINCS_gene_info_2017-03-06.txt", sep="\t")
sig_info = pd.read_csv("GSE70138_Broad_LINCS_sig_info_2017-03-06.txt", sep="\t")

# Filter to only the 978 real landmark genes
landmark_genes = gene_info[gene_info["pr_is_lm"] == 1]["pr_gene_id"].astype(str).tolist()
print(f"Number of landmark genes: {len(landmark_genes)}")

# Load the main data
data = parse("GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06.gctx")
df = data.data_df

# Filter rows to landmark genes only
df = df[df.index.astype(str).isin(landmark_genes)]
print(f"Shape after filtering to landmark genes: {df.shape}")

# Transpose so rows=experiments, columns=genes
df = df.T
print(f"Shape after transpose: {df.shape}")

# Add compound names
sig_info_indexed = sig_info.set_index("sig_id")
df["compound_name"] = df.index.map(sig_info_indexed["pert_iname"])
print("\nSample of data with compound names:")
print(df[["compound_name"]].head(10))

# Save
df.to_csv("lincs_landmark_with_compounds.csv")
print("\nSaved to lincs_landmark_with_compounds.csv")