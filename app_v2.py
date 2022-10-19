import base64
import random
import re
import uuid
from pathlib import Path

import extra_streamlit_components as stx
import pandas as pd
import streamlit as st
from PIL import Image
from st_clickable_images import clickable_images

from texts.references import cell_desc
from utils.components import create_st_button, make_tab
from utils.dataloaders import load_data

st.set_page_config(
    page_title="Covid19-Database Demo",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

hide_streamlit_style = """
<style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    footer:after {
        content:'Created by Koushul using Streamlit and BioRender'; 
        visibility: visible;
        display: block;
        position: relative;
        #background-color: red;
        padding: 5px;
        top: 2px;
    }
</style>
"""

@st.cache
def litcov_search(search):
    lines = []
    with open(f'/ihome/hosmanbeyoglu/kor11/tools/spartan_webapp/litcovid/tsv?text={search}', 'r') as f:
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

def home_page():
    images, cell_images = load_and_encode_images()
    left_col, right_col = st.columns(2)
    img = Image.open('./assets/logos/overview_light.png')

    left_col.image(img, output_format="SVG")        
    tt = """Reference:
    X. Ma, A. Somasundaram, Z. Qi, D. Hartman, H. Singh, and H. Osmanbeyoglu, 'SPaRTAN, a computational framework for linking cell-surface receptors to transcriptional regulators'"""
    left_col.markdown(f'<p style="color:#B2BEB5;font-size:15px;">{f"{tt}”"}</p>', unsafe_allow_html=True)

    
    with right_col:
        st.caption('Click to select cell type.')
        clicked = clickable_images(
            images,
            titles=[],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "8px", "height": "150px"},
        )
        
        cell_type = [i.name[:-4] for i in cell_images][clicked]
        

    right_col.markdown(f"{cell_desc[cell_type]}")
    
    st.write("[Github](https://github.com/Koushul/spartan_webapp)")

def download_button(desc, data, left_col, right_col, label='Download as CSV'):
    right_col.download_button(
        label=label,
        data=data,
        file_name='projD.csv',
        mime='text/csv',
        key=uuid.uuid1()
    )
        
    left_col.write(desc)

tabs = [
    "Home",
    "Dataset",
    "TF",
    "Protein",
    "Documentation",
    "Statistics"
]

st.title('Covid19-Database Demo')

## create navigation tabs
chosen_tab = stx.tab_bar(data=[make_tab(t) for t in tabs], default=tabs[0]) 
projD, P, tf_severity = load_data()

if chosen_tab == 'Home':
    home_page()
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    
elif chosen_tab == 'TF':
    ref = 'Literature References'
    default_idx = list(projD.index).index('IRF4')
    option = st.selectbox(
        "Choose your Transcription Factor of interest",
        projD.index, default_idx)
    
    try:
        litcovdf = litcov_search(option)
    except:
        litcovdf = pd.DataFrame([])
        
    subtabs = ['TF Activities', 'TF-Protein Correlation', f'Literature References ({len(litcovdf)})', 'Download']
    chosen_subtab = stx.tab_bar(data=[make_tab(t) for t in subtabs], default=subtabs[2]) 
    
    
    if chosen_subtab == f'Literature References ({len(litcovdf)})':
        st.caption("LitCovid is a literature hub for tracking up-to-date scientific information about the 2019 novel Coronavirus. It is the most comprehensive resource on the subject, providing a central access to 298,429 (and growing) relevant articles in PubMed. The articles are updated daily and are further categorized by different research topics (e.g. transmission) and geographic locations. https://www.ncbi.nlm.nih.gov/research/coronavirus/")

        if len(litcovdf) > 0:  
            st.dataframe(litcovdf)
            st.download_button(
                label='Download as CSV',
                data=litcovdf.to_csv(index=None),
                file_name=f'references_{option}.csv',
                mime='text/csv',
                key=uuid.uuid1()
            )
                
        else:
            st.markdown('No literature references found')
            
        
    elif chosen_subtab == 'Download':
        left_col, right_col = st.columns(2)        
        download_button('Transcription factors activity distributions\n', 
                projD.to_csv(), left_col, right_col)
        download_button('Transcription factors and surface protein correlation\n', 
                projD.to_csv(), left_col, right_col)
        download_button(f'KDE Plot for {option}\n', 
                projD.to_csv(), left_col, right_col, label='Download as PNG')
        download_button('Heatmap\n', 
                projD.to_csv(), left_col, right_col, label='Download as PNG')
        
    else:
        st.image('./assets/images/under_construction.png')
        
elif chosen_tab == 'Protein':
    option = st.selectbox(
        "Choose your Surface Protein of interest",
        P.columns)
    
    try:
        litcovdf = litcov_search(option)
    except:
        litcovdf = pd.DataFrame([])
        
    subtabs = ['TF Activities', 'TF-Protein Correlation', f'Literature References ({len(litcovdf)})', 'Download']
    chosen_subtab = stx.tab_bar(data=[make_tab(t) for t in subtabs], default=subtabs[2]) 
    
    
    if chosen_subtab == f'Literature References ({len(litcovdf)})':
        st.caption("LitCovid is a literature hub for tracking up-to-date scientific information about the 2019 novel Coronavirus. It is the most comprehensive resource on the subject, providing a central access to 298,429 (and growing) relevant articles in PubMed. The articles are updated daily and are further categorized by different research topics (e.g. transmission) and geographic locations. https://www.ncbi.nlm.nih.gov/research/coronavirus/")

        if len(litcovdf) > 0:  
            st.dataframe(litcovdf)
            st.download_button(
                label='Download as CSV',
                data=litcovdf.to_csv(index=None),
                file_name=f'references_{option}.csv',
                mime='text/csv',
                key=uuid.uuid1()
            )
                
        else:
            st.markdown('No literature references found')
        
    
        
    else:
        st.image('./assets/images/under_construction.png')
        
elif chosen_tab == 'Statistics':
    st.map() 
    
elif chosen_tab == 'Documentation':
    page = st.sidebar.radio('Content', ['Introduction', 'Data Processing', 'Dataset Summary', 'Usage', 'FAQ'])
    st.header(page)
    st.image('./assets/images/under_construction.png')
    
else:
    st.image('./assets/images/under_construction.png')
    


