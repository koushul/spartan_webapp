import streamlit as st
from navigation.tf_pages.activities import display_tf_activities
from navigation.tf_pages.litcovid import display_litcovid_data
from navigation.tf_pages.mrna import display_tf_target_data
from navigation.tf_pages.tf_protein_corr import display_tf_protein_corr_data
from texts.descriptions import Desc
from texts.references import CELL_NAMES
from utils.api import litcov_search, load_drug_info

from utils.components import display_ppi_data
import hydralit_components as hc
import pandas as pd


def download_button(desc, data, label='Download', format='text/csv'):
    left_col, right_col = st.columns(2)
    right_col.download_button(
        label="Download",
        data=data,
        file_name='projD.csv',
        mime='text/csv',
    )
        
    left_col.write(desc)
    
    
tf_bar = {'txc_inactive': 'black','menu_background':'white','txc_active':'white','option_active':'blueviolet'}

drugs = load_drug_info()

    
def tf_page(datacore):
       
    st.info(Desc.tf)
    
    _, _, edge = st.columns(3)
    checkbox = edge.checkbox('Show high correlations only')
    aa, ba, ca = st.columns(3)
    st.session_state['datasets'] = ["GSE155673"]
    
    datasets = datacore.name2ds.keys()
    tf_ds = aa.selectbox(f'Dataset ({len(datasets)})', datasets, 1)
    cell_types = datacore.name2ds[tf_ds].celltypes
    cell_type = ba.selectbox(f'Cell Type ({len(cell_types)})', cell_types, 0)

    if not checkbox:
        tfs = datacore.name2ds[tf_ds].total_transcription_factors            
    else:
        tfs = list(datacore.name2ds[tf_ds].transcription_factors(cell_type))
    
    option = ca.selectbox(
        f'Transcription factor of interest ({len(tfs)})', tfs)   
    
    litcovdf = litcov_search(option)
    targets = drugs[drugs.Target.apply(lambda x: option in x)]

    subtabs = [
        'TF activities', 
        'TF-Target gene', 
        'TF-protein correlation', 
        f'Drugs ({len(targets)})',
        f'Literature references ({len(litcovdf)})', 
        'PPI', 
        'Download'
    ]

    option_data2 = [
        {'icon': icon, 'label':label}
            for label, icon in zip(
                            subtabs, 
                            ['📈', '🎯', '🔗', '💊', '📚','🔄', '📩']
                        )
    ]
    
    chosen_subtab = hc.option_bar(
        option_definition=option_data2,
        title='',
        key='Sub1',
        override_theme=tf_bar,
        horizontal_orientation=True)
    
        
    if 'Literature references' in chosen_subtab:
        display_litcovid_data(litcovdf, option)
        
    elif chosen_subtab == 'TF-Target gene':
        display_tf_target_data(option, cell_type, ds=datacore.name2ds[tf_ds])
    
    elif chosen_subtab == f'Drugs ({len(targets)})':
        if len(targets) > 0:
            st.table(targets)
        else:
            st.warning('No drug targets found.')
    
    elif chosen_subtab == 'PPI':
        display_ppi_data(option)
        
    elif chosen_subtab == 'TF activities':  
        display_tf_activities(option, datacore.name2ds[tf_ds], cell_type)            
        
    elif chosen_subtab == 'TF-protein correlation':
        display_tf_protein_corr_data(option, cell_type, datacore.name2ds[tf_ds])
            
        
        

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