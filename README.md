# AI-Guided Screening of Traditional Chinese Medicine Compounds Using Gene Expression Signatures

**Rachel Ren & Alex Manko**  
*Artificial Intelligence in Genomics — Final Project, Spring 2026*

---

## Overview

This project trains a neural network to predict how a chemical compound affects biological pathway activity using the LINCS L1000 gene expression dataset, then applies the trained model to screen 4,983 Traditional Chinese Medicine (TCM) compounds for predicted therapeutic effects. The pipeline is inspired by Tu Youyou's Nobel Prize-winning discovery of artemisinin — computationally replicating at scale what was previously done through years of manual laboratory screening.

---

## Repository Structure

```
/
├── AiG_Project.ipynb            # Main project notebook
│
├── lincs/
│   ├── load_data.py             # Step 1: Load and filter LINCS data
│   ├── preprocess.py            # Step 2: Remove DMSO, sample 20,000 profiles
│   └── get_lincs_smiles.py      # Step 3: Fetch SMILES from PubChem
│
├── tcm/
│   └── get_tcm_smiles.py        # Parse TCMID SDF file, extract SMILES
│
└── README.md
```

---

## Google Drive

All processed data files, raw datasets, and the main Colab notebook are available here:

> [Google Drive — Project Files](https://drive.google.com/drive/folders/1kflIxZAajW06gYEMGXk6DlpTZWit4n4U?usp=sharing)

> *Note: You must be signed in with an **NYU account** to access this folder.*
```
Code/
    ├── AiG_Project.ipynb
    │
    ├── LINCS/
    │   ├── load_data.py
    │   ├── preprocess.py
    │   ├── get_lincs_smiles.py
    │   ├── GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06.gctx
    │   ├── GSE70138_Broad_LINCS_gene_info_2017-03-06.txt
    │   ├── GSE70138_Broad_LINCS_sig_info_2017-03-06.txt
    │   ├── lincs_landmark_with_compounds.csv
    │   ├── lincs_clean.csv
    │   └── lincs_with_smiles.csv
    │
    ├── TCM/
    │   ├── get_tcm_smiles.py
    │   ├── tcmid-traditional-chinese-medicine-integrated-database-03-2026.sdf
    │   └── tcm_smiles.csv
    │
    └── Disease Signature (MSigDB)/
        ├── c2.all.v2026.1.Hs.entrez.gmt          <- used in notebook
        └── c2.all.v2026.1.Hs.symbols.gmt         <- not used
```
---

## Data

Due to file size, raw datasets are not included in this repository. Download them separately using the links below, or access the processed versions via the Google Drive link above.

### LINCS L1000 — Training Data
Download from GEO accession GSE70138:  
🔗 https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE70138

Files needed:
- `GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06.gctx`
- `GSE70138_Broad_LINCS_gene_info_2017-03-06.txt`
- `GSE70138_Broad_LINCS_sig_info_2017-03-06.txt`

### TCMID via COCONUT — TCM Screening Library
Download from COCONUT (DOI: 10.71606/coconut.cnpc0046):  
🔗 https://coconut.naturalproducts.net/search?type=tags&q=TCMID+(Traditional+Chinese+Medicine+Integrated+Database)&tagType=dataSource

File needed:
- `tcmid-traditional-chinese-medicine-integrated-database-03-2026.sdf`

> Note: The original TCMID website was inaccessible from the United States at the time of data collection. COCONUT was used as an alternative access point.

### MSigDB C2 — Disease Gene Signatures
Download after free registration at:  
🔗 https://www.gsea-msigdb.org/gsea/msigdb/human/collections.jsp

Navigate to **C2: curated gene sets** → click **NCBI (Entrez) Gene IDs**

File needed:
- `c2.all.v2026.1.Hs.entrez.gmt`

---

## How to Run

### Prerequisites

```bash
pip install pandas cmapPy requests rdkit
```

### Step 1 — LINCS Preprocessing

Place all three LINCS raw files in the `lincs/` folder, then run in order:

```bash
cd lincs
python3 load_data.py          # outputs: lincs_landmark_with_compounds.csv
python3 preprocess.py         # outputs: lincs_clean.csv
python3 get_lincs_smiles.py   # outputs: lincs_with_smiles.csv
```

### Step 2 — TCM Preprocessing

Place the TCMID SDF file in the `tcm/` folder, then run:

```bash
cd tcm
python3 get_tcm_smiles.py     # outputs: tcm_smiles.csv
```

### Step 3 — Model Training and TCM Screening

Upload the following files to Google Drive:
- `lincs_with_smiles.csv`
- `tcm_smiles.csv`
- `c2.all.v2026.1.Hs.entrez.gmt`

Then open and run `AiG_Project.ipynb` in Google Colab. The notebook is available in the Google Drive link above.

The notebook handles:
- TCM/LINCS overlap removal
- Morgan fingerprint computation
- Pathway score computation from the GMT file
- Hyperparameter grid search (72 configurations)
- MLP model training and evaluation
- TCM compound screening and ranking

---

## Dependencies

| Library | Purpose |
|---|---|
| `pandas` | Data loading and manipulation |
| `cmapPy` | Reading LINCS `.gctx` binary files |
| `requests` | PubChem REST API calls |
| `rdkit` | Morgan fingerprint computation, SDF parsing |
| `torch` | MLP model training |
| `scikit-learn` | Train/validation/test splitting |
| `scipy` | Pearson correlation evaluation |
| `matplotlib` | Loss curve and results visualization |
