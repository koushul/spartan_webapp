import base64
from pathlib import Path

import pandas as pd
import streamlit as st

from texts.descriptions import DatasetDesc

@st.cache
def load_data():
    
    tf_severity = pd.read_parquet('./data/tf_activity.parquet')
    
    data = {
        'name': ['E-MTAB-9357', 'GSE155673', 'meyer21_pbmc', 'GSE167118'],
        'organism': ['Homo sapiens', 'Homo sapiens', 'Homo sapiens', 'Homo sapiens'],
        'patients': [270, 12, 143, 93],
        'cell count': ['559,517', '59,664', '691,683', '86,935'],
        'platform': ['10X Genomics Chromium', 'Illumina HiSeq 4000', 'Illumina NovaSeq 6000', 'Illumina NovaSeq 6000'],
        'url': [
            'https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-9357',
            'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155673', 
            'https://www.covid19cellatlas.org/index.patient.html', 
            'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE167118'
        ],
        'title': [
            'Multiomic Immunophenotyping Of COVID-19 Patients Reveals Early Infection Trajectories',
            'Systems Biological Assessment Of Immunity To Mild Versus Severe COVID-19 Infection In Humans',
            'The Cellular Immune Response To COVID-19 Deciphered By Single Cell Multi-Omics Across 2 Three UK Centres',
            'Clonal expansion and activation of tissue-resident memory-like Th17 cells expressing GM-CSF in the lung of severe COVID-19 patients'
        ]
    }
    
    
    P = pd.read_csv("./data/data_created/P_1-1.csv", index_col=0)
        
    ds = pd.DataFrame(data)
        
    return P, tf_severity, ds

@st.cache
def litcov_search(search):
    lines = []
    with open(f'./litcovid/tsv?text={search}', 'r') as f:
        lines = f.readlines()[33:]
    if lines:
        litcovdf = pd.DataFrame([x.split('\t') for x in lines[1:]], 
                columns=['pmid', 'title', 'journal']).applymap(lambda x: x.replace('\n', ''))
    return litcovdf

@st.cache
def load_and_encode_images():
    images = []
    cell_images = list(Path('./assets/cells/').glob('*.png'))
    
    for image_file in cell_images:
            with open(image_file, "rb") as image:
                encoded = base64.b64encode(image.read()).decode()
                images.append(f"data:image/jpeg;base64, {encoded}")
                
    return images, cell_images
