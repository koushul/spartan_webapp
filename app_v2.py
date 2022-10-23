import base64
from fileinput import filename
import uuid
from pathlib import Path

import extra_streamlit_components as stx
import pandas as pd
import streamlit as st

from navigation.home import home_page
from navigation.stats import stats_page
from utils.components import make_tab
from utils.dataloaders import load_data
from navigation.protein import get_ppi_edge_list

import streamlit.components.v1 as components
from pyvis.network import Network
import numpy as np

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

# st.markdown("""<img src="file:///ihome/hosmanbeyoglu/kor11/tools/spartan_webapp/assets/cells/Monocytes.png"></img>
# <style>
# body {background:midnightblue;}
# img {width:100%;}
# img:hover {-webkit-filter: brightness(150%); }
# </style>
# """, unsafe_allow_html=True)

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

st.title('Covid19-Database Demo') ## Title
st.markdown(hide_streamlit_style, unsafe_allow_html=True) ## Footer

## create navigation tabs
chosen_tab = stx.tab_bar(data=[make_tab(t) for t in tabs], default=tabs[0]) 
projD, P, tf_severity = load_data()

if chosen_tab == 'Home':
    home_page()
    
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
        
    subtabs = ['TF Activities', 'TF-Protein Correlation', f'Literature References ({len(litcovdf)})', 'PPI', 'Download']
    chosen_subtab = stx.tab_bar(data=[make_tab(t) for t in subtabs], default=subtabs[2]) 

    import stringdb

    def get_ppi_edge_list(gene, neighbors, size):
        
        genes = [gene]
        string_ids = stringdb.get_string_ids(genes)
        enrichment_df = stringdb.get_interaction_partners(string_ids.queryItem, limit=size)
        extras = list(enrichment_df['preferredName_B'].values[:neighbors])
        string_ids = stringdb.get_string_ids(extras+genes)
        enrichment_df = stringdb.get_interaction_partners(string_ids.queryItem, limit=size)
        
        return string_ids, enrichment_df[['preferredName_A',	'preferredName_B', 'score']].values
    
    if chosen_subtab == 'PPI':
        st.subheader(f'Protein-Protein Interactions for {option}')
        left_col, right_col = st.columns(2)
        size = left_col.slider('Interactors', 2, 100, 10)
        neighbors = right_col.slider('Neighbors', 1, 10, 3)

        net = Network()
        caption, pairs = get_ppi_edge_list(option, neighbors, size)
        st.caption(caption.preferredName.values[0])
        st.caption(caption.annotation.values[0])
        # st.write(caption.preferredName.values[0])
        
        import random
        def generate_color():
            random_number = random.randint(0,16777215)
            hex_number = str(hex(random_number))
            hex_number ='#'+ hex_number[2:]
            return hex_number
    
        for i, j, v in pairs:
            net.add_node(j, label=j, color=generate_color())
            
        # for n in net.nodes:
        #     if n['label'] == caption.preferredName.values[0]:
        #         n['color'] = 'red'
                
            
            
        for pair in pairs:
           net.add_edge(pair[0], pair[1], value=pair[2]/10)
        
        # net.show_buttons(filter_=['physics'])


        net.show('test.html')
        HtmlFile = open("test.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        components.html(source_code, height = 600, width=900)
        
        st.download_button(
            label='Download Graph',
            data=source_code,
            file_name = 'ppi.html'
        )
    
    elif chosen_subtab == f'Literature References ({len(litcovdf)})':
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
    stats_page()

    
elif chosen_tab == 'Documentation':
    st.sidebar.header('Content')
    page = st.sidebar.radio('', ['Introduction', 'Data Processing', 'Dataset Summary', 'Usage', 'FAQ'])
    st.header(page)
    st.image('./assets/images/under_construction.png')
    
else:
    st.image('./assets/images/under_construction.png')
    


