"""
get_lincs_smiles.py: 
    Gets the SMILES chemical structure string for each unique compound
    in the LINCS training dataset using the PubChem REST API. SMILES
    (Simplified Molecular Input Line Entry System) is a standard text-based
    notation for representing molecular structure, and is required as input
    for computing Morgan fingerprints used by the model.
 
    Must be run AFTER preprocess.py.
 
    Note: This script makes one HTTP request per unique compound to PubChem.
    Could take several minutes to run depending on the number of unique compounds.
 
Input files required (must be in the same directory):
    - lincs_clean.csv
        Output of preprocess.py. Contains 20,000 sampled LINCS profiles with compound names.
 
Output files:
    - lincs_with_smiles.csv
        The same 20,000 profiles with an additional 'SMILES' column.
        Rows where no valid SMILES could be found are dropped.
        This file is uploaded to Google Drive for use in the main notebook.
 
Dependencies:
    - requests  (install with: pip install requests)
    - pandas
 
External API:
    - PubChem REST API: https://pubchem.ncbi.nlm.nih.gov/rest/pug/
      Used to fetch canonical SMILES strings by compound name.
      No API key required. Free to use.
 
Usage:
    python3 get_lincs_smiles.py
"""

import requests
import pandas as pd
import time

df = pd.read_csv('lincs_clean.csv')
compounds = df['compound_name'].unique()
print(f"Fetching SMILES for {len(compounds)} unique compounds...")

results = {}
for i, name in enumerate(compounds):
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/property/CanonicalSMILES/JSON"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            props = r.json()['PropertyTable']['Properties'][0]
            smiles = props.get('ConnectivitySMILES') or props.get('CanonicalSMILES')
            results[name] = smiles
        else:
            results[name] = None
    except:
        results[name] = None
    if i % 100 == 0:
        print(f"Progress: {i}/{len(compounds)}")
    time.sleep(0.2)

df['SMILES'] = df['compound_name'].map(results)
df = df.dropna(subset=['SMILES'])
print(f"\nCompounds with SMILES: {len(df)}")
df.to_csv('lincs_with_smiles.csv', index=False)
print("Saved to lincs_with_smiles.csv!")