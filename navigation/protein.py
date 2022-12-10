import random
import pandas as pd
import streamlit as st
import hydralit_components as hc
from navigation.protein_pages.expression import display_protein_expressions
from navigation.protein_pages.litcovid import display_litcovid_data
from navigation.protein_pages.protein_tf_corr import display_protein_tf_corr_data
from texts.references import CELL_NAMES

from utils.api import litcov_search
from utils.components import display_ppi_data

def generate_color():
    random_number = random.randint(0,16777215)
    hex_number = str(hex(random_number))
    hex_number ='#'+ hex_number[2:]
    return hex_number
        

protein_bar = {'txc_inactive': 'black','menu_background':'white','txc_active':'white','option_active':'blue'}


def protein_page(datacore):
    st.info('Search surface protein across COVID-19 patients and health individuals. For a single surface protein, SPaRTAN COVID-19db supports exploring its expression for each cell type, correlated transcription factors, protein-protein interactions and relevant literature.')
    
    _, _, edge = st.columns(3)
    
    checkbox = edge.checkbox('Show high correlations only')    
    a, b, c = st.columns(3)
    st.session_state['datasets'] = ["GSE155673"]
    datasets = datacore.name2ds.keys()
    p_ds = a.selectbox(f'Dataset ({len(datasets)})', datasets, 0)
    cell_types = datacore.name2ds[p_ds].celltypes
    cell_type = b.selectbox(f'Cell Type ({len(cell_types)})', cell_types, 0)
    
    if not checkbox:
        s_proteins = list(datacore.name2ds[p_ds].total_surface_proteins)
    else:
        s_proteins = list(datacore.name2ds[p_ds].surface_proteins(cell_type))

    option = c.selectbox(
        f"Surface protein of interest ({len(s_proteins)})",
        s_proteins)
            
    try:    
        litcovdf = litcov_search(option)
    except:
        litcovdf = pd.DataFrame([])

        
    subtabs = ['Protein expression', 'Protein-TF correlation', 'Drugs', f'Literature references ({len(litcovdf)})', 'PPI', 'Download']
        
    option_data2 = [{'icon': icon, 'label':label} for 
            label, icon in zip(
                subtabs, 
                ['📈', '🔗', '💊', '📚', '🔄','📩']
            )
    ]
    
    chosen_subtab = hc.option_bar(
        option_definition=option_data2,
        title='',
        key='Sub2',
        override_theme=protein_bar,
        horizontal_orientation=True)
        
        
    if chosen_subtab == 'Protein expression':
        display_protein_expressions(option, datacore.name2ds[p_ds], cell_type)
        
    elif chosen_subtab == 'Protein-TF correlation':
        display_protein_tf_corr_data(option, cell_type, datacore.name2ds[p_ds])
        
    elif chosen_subtab == 'Drugs':
        st.image('./assets/images/under_construction.png')
            
    elif 'Literature references' in chosen_subtab:
        display_litcovid_data(litcovdf, option)
    
    elif chosen_subtab == 'PPI':
        display_ppi_data(option)
        
        

            
            
        

