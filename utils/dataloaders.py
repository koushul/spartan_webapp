import base64
from pathlib import Path

import pandas as pd
import streamlit as st


@st.cache
def load_data():
    
    tf_severity = pd.read_parquet('./data/tf_activity.parquet')
    P = pd.read_parquet('./data/surface_protein.parquet')
        
    return P, tf_severity

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
