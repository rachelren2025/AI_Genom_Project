"""
get_tcm_smiles.py: 
    Parses the TCMID compound collection downloaded from the COCONUT natural
    products platform and extracts compound names and SMILES chemical structure
    strings from the SDF file. The resulting CSV is used as the TCM screening
    library — the set of compounds the trained model is applied to in order to
    predict their gene expression effects.
 
    TCMID (Traditional Chinese Medicine Integrated Database) was accessed via
    the COCONUT natural products platform (coconut.naturalproducts.net) because
    the original TCMID website was inaccessible from the United States at the
    time of data collection.
 
Input files required (must be in the same directory):
    Note: These input files are large and not included in the repository. We provide them
    in the google drive link on the README page.
    - tcmid-traditional-chinese-medicine-integrated-database-03-2026.sdf
        The full TCMID compound collection downloaded from COCONUT as a
        single SDF file. Download from:
        https://coconut.naturalproducts.net/search?type=tags&q=TCMID+
        (Traditional+Chinese+Medicine+Integrated+Database)&tagType=dataSource
        DOI: 10.71606/coconut.cnpc0046
 
Output files:
    - tcm_smiles.csv
        A CSV with two columns: 'compound_name' and 'SMILES'.
        Contains 4,983 TCM compounds with valid chemical structures.
        This file is uploaded to Google Drive for use in the main notebook.
 
Dependencies:
    - rdkit  (install with: pip install rdkit)
    - pandas
 
SDF file:
    SDF (Structure Data File) is a standard chemical file format that stores
    molecular structures alongside metadata properties. Each molecule in the file has a name, 
    a 2D/3D structure, and a set of named properties. RDKit's SDMolSupplier reads
    molecules from SDF files one at a time.
 
MILES string:
    SMILES (Simplified Molecular Input Line Entry System) is a standard text-based notation 
    for representing molecular structure.
    Example: 'CCO' represents ethanol (2 carbons and 1 oxygen).
    SMILES strings are required as input for computing Morgan fingerprints.
 
Usage:
    python3 get_tcm_smiles.py
"""

from rdkit import Chem
import pandas as pd

print("Loading SDF file...")
supplier = Chem.SDMolSupplier('tcmid-traditional-chinese-medicine-integrated-database-03-2026.sdf')

results = []
for i, mol in enumerate(supplier):
    if mol is not None:
        try:
            name = mol.GetProp('name') if mol.HasProp('name') else f'MOL_{i}'
            smiles = mol.GetProp('canonical_smiles') if mol.HasProp('canonical_smiles') else Chem.MolToSmiles(mol)
            results.append({'compound_name': name, 'SMILES': smiles})
        except:
            pass
    if i % 1000 == 0:
        print(f"Processed {i} compounds...")

df = pd.DataFrame(results)
print(f"\nTotal compounds: {len(df)}")
print(df.head())
df.to_csv('tcm_smiles.csv', index=False)
print("Saved to tcm_smiles.csv!")