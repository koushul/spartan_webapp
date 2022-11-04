from pathlib import Path
import uuid

import extra_streamlit_components as stx
import pandas as pd
import streamlit as st
from navigation.datasets import dataset_page
from navigation.doc import doc_page

from navigation.home import home_page
from navigation.stats import stats_page
from utils.components import make_tab, ridge_plot
from utils.dataloaders import Dataset, litcov_search
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from utils.components import ppi, local_css, hide_streamlit_style
from texts.descriptions import DatasetDesc, Desc
from utils.dataloaders import make_datacore

from PIL import Image
Image.MAX_IMAGE_PIXELS = None
HOME = "Home"
DATASET = "Datasets"
TF = "Transcription Factors"
PROTEINS = "Surface Proteins"
DOC = "Documentation"
STATS = "Usage"

st.set_page_config(
    page_title="SPaRTAN COVID-19db",
    page_icon="./assets/logos/spartan.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

def totags(tags):
    t = '<div>'
    for tag, color in zip(tags, ['red', 'blue', 'green', 'orange']):
        t += f"<span class='highlight {color}'>{tag}</span>\t"
    t += '</div>'
    return t

tabs = [
    HOME,
    DATASET,
    PROTEINS,
    TF,
    DOC, 
    STATS
]


datacore =  make_datacore()()
ds = Dataset.metadata_df()



st.markdown(hide_streamlit_style, unsafe_allow_html=True) ## Footer

chosen_tab = stx.tab_bar(data=[make_tab(t) for t in tabs], default=tabs[0]) 

if chosen_tab == HOME:
    home_page()
    
elif chosen_tab == DATASET:
    dataset_page(ds, datacore)
          
elif chosen_tab == TF:
    st.header('TF Exploration')
    st.info(Desc.tf)
    ref = 'Literature References'
    
    aa, ba, ca = st.columns(3)
    
    st.session_state['datasets'] = ["GSE155673"]
    
    # if 'grid' in st.session_state and st.session_state['datasets']:
        # tf_ds = aa.multiselect(f'Dataset ({1})', datacore.name2ds.keys(), st.session_state['datasets'])
    # else:
    datasets = datacore.name2ds.keys()
    tf_ds = aa.selectbox(f'Dataset ({len(datasets)})', datasets, 0)
    cell_types = datacore.name2ds["GSE155673"].cell_types
    cell_type = ba.selectbox(f'Cell Type ({len(cell_types)})', cell_types, 3)
    tfs = datacore.name2ds["GSE155673"].total_transcription_factors
    option = ca.selectbox(
        f'Transcription Factor of interest ({len(tfs)})', tfs)   
    
    litcovdf = litcov_search(option)
   
    subtabs = ['TF Activities', 'TF-Target gene', 'TF-Protein Correlation', f'Literature References ({len(litcovdf)})', 'PPI', 'Download']
    # if 'current_tab_tf' in st.session_state:
    #     current_tab_tf = st.session_state['current_tab_tf']
    # else:
    current_tab_tf = subtabs[0]
        
    chosen_subtab = stx.tab_bar(data=[make_tab(t) for t in subtabs], default=current_tab_tf) 
    st.session_state['current_tab_tf'] = chosen_subtab
    
    if chosen_subtab == f'Literature References ({len(litcovdf)})':
        st.caption(Desc.litcovid)

        if len(litcovdf) > 0:  
            st.table(litcovdf)
            st.download_button(
                label='Download as CSV',
                data=litcovdf.to_csv(index=None),
                file_name=f'references_{option}.csv',
                mime='text/csv',
                key=uuid.uuid1()
            )
                
        else:
            st.warning('No literature references found')
    
    elif chosen_subtab == 'TF-Target gene':
        st.dataframe(pd.DataFrame(columns=['Gene Name', 'Correlation with TF', 'Gene Info']))
    
    elif chosen_subtab == 'PPI':
        ppi(option)
        
    elif chosen_subtab == 'TF Activities':  
        st.header(f'📈 Inferred {option} activity in {cell_type}')  
        try:    
            df_plt = datacore.name2ds["GSE155673"].get_tf_df(cell_type, option)
            c, d, e = st.columns([1, 6, 1])
            d.pyplot(ridge_plot(df_plt))
        except:
            st.warning('No high correlation matches found.')
        
    elif chosen_subtab == 'TF-Protein Correlation':
        st.header(f'🔗 Correlation between {option} and inferred surface protein expression in {cell_type}')

        
        csv, img = datacore.name2ds["GSE155673"].get_tf_protein_data(cell_type, option)
        try:
            st.image(img)
            exp = st.expander('Raw Data')
            exp.dataframe(pd.read_csv(csv))
        except:
            st.warning('No high correlation matches found.')
            
        
        

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
        
elif chosen_tab == PROTEINS:
    st.title('Surface Protein Exploration')
    st.info('Search surface protein across COVID-19 patients and health individuals. For a single surface protein, SPaRTAN COVID-19db supports exploring its expression for each cell type, correlated transcription factors, protein-protein interactions and relevant literature.')
    
    _, _, edge = st.columns(3)
    
    checkbox = edge.checkbox('Show high correlations only')
    
    a, b, c = st.columns(3)
        
    # if 'grid' in st.session_state and st.session_state['datasets']:
    #     p_ds = a.multiselect('Dataset', datacore.name2ds.keys(), st.session_state['datasets'])
    # else:
    
    datasets = datacore.name2ds.keys()
    p_ds = a.selectbox(f'Dataset ({len(datasets)})', datasets, 0)
    cell_types = datacore.name2ds[p_ds].cell_types
    cell_type = b.selectbox(f'Cell Type ({len(cell_types)})', cell_types, 0)
    
    try: 
        if not checkbox:
            s_proteins = list(datacore.name2ds[p_ds].total_surface_proteins)
        else:
            s_proteins = list(datacore.name2ds[p_ds].surface_proteins(cell_type))

        option = c.selectbox(
            f"Surface Protein of interest ({len(s_proteins)})",
            s_proteins)
        
            
        o = option.split('--')[0]
        
        try:    
            litcovdf = litcov_search(o)
        except:
            litcovdf = pd.DataFrame([])
            
    except:
        st.error('Error loading dataset', icon="🚨")
        litcovdf = pd.DataFrame([])
        
        
    subtabs = ['Protein Expression', 'Protein-TF Correlation', f'Literature References ({len(litcovdf)})', 'PPI', 'Download']
    if 'current_tab' in st.session_state:
        current_tab = st.session_state['current_tab']
    else:
        current_tab = subtabs[1]
        
    
    chosen_subtab = stx.tab_bar(data=[make_tab(t) for t in subtabs], default=current_tab) 
    st.session_state['current_tab'] = chosen_subtab
        
    
    if chosen_subtab == 'PPI':
        ppi(o)
        
        
    elif chosen_subtab == 'Protein-TF Correlation':
        st.header(f'🔗 Correlation between {o} and inferred TF activities in {cell_type}')
        
        csv, img = datacore.name2ds[p_ds].get_protein_tf_data(cell_type, option)
        try:
            st.image(img)
            exp = st.expander('Raw Data')
            exp.dataframe(pd.read_csv(csv))
        except:
            st.warning('No high correlation matches found.')
            
            
        
    elif chosen_subtab == 'Protein Expression':
        st.header(f'📈 Inferred {option} expression in {cell_type}')  
        
        # try:
        df_plt = datacore.name2ds[p_ds].get_protein_df(cell_type, option)
        c, d, e = st.columns([1, 6, 1])
        img = ridge_plot(df_plt)
        x = st.slider('x', int(img.size[0]/2), int(img.size[0]*2), img.size[0], 50)
        y = st.slider('y', int(img.size[1]/2), int(img.size[1]*2), img.size[1], 50)
        d.image(img.resize((x, y)))

        # except:
        #     st.warning('No high correlation matches found.')
        
        
    elif chosen_subtab == f'Literature References ({len(litcovdf)})':
        st.caption(Desc.litcovid)

        if len(litcovdf) > 0:  
            st.table(litcovdf)
            st.download_button(
                label='Download as CSV',
                data=litcovdf.to_csv(index=None),
                file_name=f'references_{option}.csv',
                mime='text/csv',
                key=uuid.uuid1()
            )
                
        else:
            st.warning('No literature references found')
        
elif chosen_tab == DOC:
    doc_page()
    
elif chosen_tab == STATS:
    stats_page()