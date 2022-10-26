import uuid

import extra_streamlit_components as stx
import pandas as pd
import streamlit as st

from navigation.home import home_page
from navigation.stats import stats_page
from utils.components import make_tab
from utils.dataloaders import load_data, litcov_search


from utils.components import ppi
from texts.descriptions import Desc

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



# @st.cache
# def load_and_encode_images():
#     images = []
#     cell_images = list(Path('./assets/cells/').glob('*.png'))
#     for image_file in cell_images:
#             with open(image_file, "rb") as image:
#                 encoded = base64.b64encode(image.read()).decode()
#                 images.append(f"data:image/jpeg;base64, {encoded}")
                
#     return images, cell_images

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
    "Transcription Factors",
    "Surface Protein",
    "Documentation",
    "Statistics"
]

st.markdown(hide_streamlit_style, unsafe_allow_html=True) ## Footer

## create navigation tabs
chosen_tab = stx.tab_bar(data=[make_tab(t) for t in tabs], default=tabs[0]) 
P, tf_severity = load_data()

if chosen_tab == 'Home':
    st.title('Welcome to SPaRTAN COVID-19db') ## Title
    st.markdown('#### ' + Desc.home)
    home_page()
    
elif chosen_tab == 'Dataset':
    st.header('Dataset Browser')
    st.markdown('##### ' + Desc.ds)
    
    
    
elif chosen_tab == 'Transcription Factors':
    st.header('TF Exploration')
    st.markdown('##### ' + Desc.tf)
    
    ref = 'Literature References'
    default_idx = list(tf_severity.index).index('IRF4')

    
    aa, ba, ca = st.columns(3)
    option = aa.selectbox(
        "Choose your Transcription Factor of interest",
        tf_severity.index, default_idx)
    cell_type = ba.selectbox('Cell Type', ('B', 'NK', 'CD4+', 'CD8+', 'CD16+', 'CD14+'), 2)
    tf_ds = ca.multiselect('Dataset', ('A', 'B', 'C', 'D'), ['A'])
    
    try:
        litcovdf = litcov_search(option)
    except:
        litcovdf = pd.DataFrame([])
        
    subtabs = ['TF Activities', 'TF-Protein Correlation', f'Literature References ({len(litcovdf)})', 'PPI', 'Download']
    chosen_subtab = stx.tab_bar(data=[make_tab(t) for t in subtabs], default=subtabs[2]) 
    
    
    if chosen_subtab == f'Literature References ({len(litcovdf)})':
        st.caption(Desc.litcovid)

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
    
    elif chosen_subtab == 'PPI':
        ppi(option)

    elif chosen_subtab == 'Download':
        left_col, right_col = st.columns(2)        
        # download_button('Transcription factors activity distributions\n', 
        #         tf_severity.to_csv(), left_col, right_col)
        # download_button('Transcription factors and surface protein correlation\n', 
        #         tf_severity.to_csv(), left_col, right_col)
        # download_button(f'Density Plot for {option}\n', 
        #         tf_severity.to_csv(), left_col, right_col, label='Download as PNG')
        # download_button('Heatmap\n', 
        #         tf_severity.to_csv(), left_col, right_col, label='Download as PNG')
        
    else:
        st.image('./assets/images/under_construction.png')
        
elif chosen_tab == 'Surface Protein':
    a, b, c = st.columns(3)
    option = a.selectbox(
        "Choose your Surface Protein of interest",
        P.index)
    cell_type = b.selectbox('Cell Type', ('B', 'NK', 'CD4+', 'CD8+', 'CD16+', 'CD14+'), 2)
    p_ds = c.multiselect('Dataset', ('A', 'B', 'C', 'D'), ['A'])
    
    

    try:    
        litcovdf = litcov_search(option)
    except:
        litcovdf = pd.DataFrame([])
        
    subtabs = ['Protein Expression', 'Protein-TF Correlation', f'Literature References ({len(litcovdf)})', 'PPI', 'Download']
    chosen_subtab = stx.tab_bar(data=[make_tab(t) for t in subtabs], default=subtabs[2]) 
    
    if chosen_subtab == 'PPI':
        ppi(option)
        
    elif chosen_subtab == f'Literature References ({len(litcovdf)})':
        st.caption(Desc.litcovid)

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
    


