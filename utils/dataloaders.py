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