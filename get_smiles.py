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