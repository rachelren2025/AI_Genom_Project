"""
preprocess.py: 
    Cleans the LINCS landmark gene expression dataset by removing control
    experiments (DMSO), then randomly samples 20,000 profiles to produce
    a manageable training dataset.
 
    Must be run AFTER load_data.py.
 
Input files required (must be in the same directory):
    - lincs_landmark_with_compounds.csv
        Output of load_data.py. Contains 118,050 experimental profiles
        across 978 landmark genes with compound names attached.
 
Output files:
    - lincs_clean.csv
        A CSV containing 20,000 randomly sampled profiles after DMSO
        removal. Used as input to get_lincs_smiles.py.
 
Dependencies:
    - pandas
 
Usage:
    python3 preprocess.py
"""

import pandas as pd

# Load the saved file
df = pd.read_csv("lincs_landmark_with_compounds.csv", index_col=0)

# Remove DMSO (control, not a real compound)
df = df[df["compound_name"] != "DMSO"]
print(f"Shape after removing DMSO: {df.shape}")

# Check how many unique compounds we have
print(f"Unique compounds: {df['compound_name'].nunique()}")

# Sample 20000 rows for training (manageable size)
df_sampled = df.sample(n=20000, random_state=42)
print(f"Sampled shape: {df_sampled.shape}")

df_sampled.to_csv("lincs_clean.csv")
print("Saved to lincs_clean.csv!")