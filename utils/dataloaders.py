import pandas as pd
import streamlit as st
from pathlib import Path
import base64

@st.cache
def load_data():
    
    projD = pd.read_csv('projD_ori.csv').set_index('Unnamed: 0')
    projD.index.name = 'TF'
    
    P = pd.read_csv('P_1-1.csv').set_index('Unnamed: 0')
    P.index.name='Cell'
    
    tf_severity = pd.read_excel('/ihome/hosmanbeyoglu/kor11/tools/spartan_webapp/CD16_Mono_projD_median_group_100_1500.xlsx', 
        engine='openpyxl').set_index('Unnamed: 0')
    tf_severity.index.name = 'TF'
    tf_severity.columns = ['Healthy', 'Mild', 'Moderate', 'Severe', 'pvalues']
        
    return projD, P, tf_severity


@st.cache
def load_references():
    dff = pd.read_csv('/ihome/hosmanbeyoglu/kor11/tools/spartan_webapp/litcovid.export.all.tsv', sep='\t', header=None)
    dff.columns = ['pmid', 'title', 'journal']
    
    return dff


@st.cache
def load_and_encode_images():
    images = []
    cell_images = list(Path('./assets/cells/').glob('*.png'))
    
    for image_file in cell_images:
            with open(image_file, "rb") as image:
                encoded = base64.b64encode(image.read()).decode()
                images.append(f"data:image/jpeg;base64, {encoded}")
                
    return images, cell_images

@st.cache
def litcov_search(search):
    lines = []
        
    with open(f'/ihome/hosmanbeyoglu/kor11/tools/spartan_webapp/litcovid/tsv?text={search}', 'r') as f:
        lines = f.readlines()[33:]
    
    if lines:
        litcovdf = pd.DataFrame([x.split('\t') for x in lines[1:]], 
                columns=['pmid', 'title', 'journal']).applymap(lambda x: x.replace('\n', ''))

    return litcovdf