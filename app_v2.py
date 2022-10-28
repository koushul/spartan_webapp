import uuid

import extra_streamlit_components as stx
import pandas as pd
import streamlit as st

from navigation.home import home_page
from navigation.stats import stats_page
from utils.components import make_tab
from utils.dataloaders import load_data, litcov_search
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from utils.components import ppi, download_button, local_css, hide_streamlit_style
from texts.descriptions import DatasetDesc, Desc

from pathlib import Path
from navigation.protein import load_pairs
import seaborn as sns
import matplotlib.pyplot as plt
### Housekeeping ###

st.set_page_config(
    page_title="SPaRTAN COVID-19db",
    page_icon="./assets/logos/spartan.png",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={}
)

def totags(tags):
    t = '<div>'
    for tag, color in zip(tags, ['red', 'blue', 'green', 'orange']):
        t += f"<span class='highlight {color}'>{tag}</span>\t"
    t += '</div>'
    return t

tabs = [
    "Home",
    "Dataset",
    "Transcription Factors",
    "Surface Protein",
    "Documentation",
    "Statistics"
]

P, tf_severity, ds = load_data()
default_idx = list(tf_severity.index).index('IRF4')

st.markdown(hide_streamlit_style, unsafe_allow_html=True) ## Footer

@st.cache
def high_corr():
    return list(i.name.split('-TFs')[0] for i in Path('./data/data_created/protein-TFs_higCorr/').glob('*.csv'))


chosen_tab = stx.tab_bar(data=[make_tab(t) for t in tabs], default=tabs[0]) 

if chosen_tab == 'Home':
    home_page()
    
elif chosen_tab == 'Dataset':
    st.header(f'Dataset Browser')
    st.info(Desc.ds)
    ds2 = ds[['name', 'title', 'organism', 'patients', 'cell count', 'platform']]
    gd = GridOptionsBuilder.from_dataframe(ds2)
    
    if 'datasets' in st.session_state:
        pre_selected_rows = [list(ds.name).index(i) for i in st.session_state['datasets']]
    else:
        pre_selected_rows = []
                
                
    gd.configure_selection(selection_mode='multiple', use_checkbox=True, pre_selected_rows=pre_selected_rows)
    gridoptions = gd.build()

    grid_table = AgGrid(ds2, 
        gridOptions=gridoptions,
        update_mode=GridUpdateMode.SELECTION_CHANGED, 
        fit_columns_on_grid_load=True,
        height=155,
        width='100%',
        theme="streamlit",
        key='grid'
    )


        
    selected_row = grid_table["selected_rows"]
    
    st.session_state['datasets'] = [x['name'] for x in selected_row]
    
    for idx, row_json in enumerate(selected_row):
        st.header(row_json['name'] + ': ' + row_json['title'])
        st.markdown(DatasetDesc[row_json['name']])
        st.markdown(ds[ds.name==row_json['name']].url.values[0])
        
        exp = st.expander('View UMAP')
        exp.image('./assets/umaps/umap.png')

        local_css()
        st.markdown(
            totags([
                row_json['organism'], 
                row_json['platform'], 
                row_json['cell count'], 
                row_json['patients']]), 
            unsafe_allow_html=True)
        
        st.markdown('---')
        
      
    
    
    
elif chosen_tab == 'Transcription Factors':
    st.header('TF Exploration')
    st.info(Desc.tf)
    
    ref = 'Literature References'

    
    aa, ba, ca = st.columns(3)
    option = aa.selectbox(
        "Choose your Transcription Factor of interest",
        tf_severity.index, default_idx)
    cell_type = ba.selectbox('Cell Type', ('B', 'NK', 'CD4+', 'CD8+', 'CD16+', 'CD14+'), 2)

    
    if 'grid' in st.session_state and st.session_state['datasets']:
        tf_ds = ca.multiselect('Dataset', ds.name, st.session_state['datasets'])
    else:
        tf_ds = ca.multiselect('Dataset', ds.name)
            
    # st.session_state['datasets'] = tf_ds
   
    
    try:
        litcovdf = litcov_search(option)
    except:
        litcovdf = pd.DataFrame([])
        
    subtabs = ['TF Activities', 'TF-Protein Correlation', f'Literature References ({len(litcovdf)})', 'PPI', 'Download']
    if 'current_tab_tf' in st.session_state:
        current_tab_tf = st.session_state['current_tab_tf']
    else:
        current_tab_tf = subtabs[2]
        
    chosen_subtab = stx.tab_bar(data=[make_tab(t) for t in subtabs], default=current_tab_tf) 
    st.session_state['current_tab_tf'] = chosen_subtab
    
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
        P.columns, list(P.columns).index('CD11C'))
        
    cell_type = b.selectbox('Cell Type', ('B', 'NK', 'CD4+', 'CD8+', 'CD16+', 'CD14+'), 2)
    
    if 'grid' in st.session_state and st.session_state['datasets']:
        p_ds = c.multiselect('Dataset', ds.name, st.session_state['datasets'])
    else:
        p_ds = c.multiselect('Dataset', ds.name)
            
    # st.session_state['datasets'] = p_ds

    try:    
        litcovdf = litcov_search(option)
    except:
        litcovdf = pd.DataFrame([])
        
    
        
        
    subtabs = ['Protein Expression', 'Protein-TF Correlation', f'Literature References ({len(litcovdf)})', 'PPI', 'Download']
    if 'current_tab' in st.session_state:
        current_tab = st.session_state['current_tab']
    else:
        current_tab = subtabs[1]
    chosen_subtab = stx.tab_bar(data=[make_tab(t) for t in subtabs], default=current_tab) 
    st.session_state['current_tab'] = chosen_subtab
    
    if chosen_subtab == 'PPI':
        ppi(option)
        
    elif chosen_subtab == 'Protein Expression':
        _df = load_pairs().drop('pval_sel', axis=1)
        _df = _df[_df['Unnamed: 0'].str.contains(f'{option}_')]
        _df = _df.set_index('Unnamed: 0')
        _df.index.name = None
        
        st.table(_df)
        
        fig = plt.figure(figsize=(10, 5), dpi=120)
        sns.kdeplot(data=_df.drop(['pval_adj'], axis=1), shade=True)
        st.pyplot(fig)
        
    elif chosen_subtab == 'Protein-TF Correlation':
        if option in high_corr():
            st.header(f'🔎 {option}')
            expander = st.expander("See raw data")
            data = pd.read_csv(f'./data/data_created/protein-TFs_higCorr/{option}-TFs_highCorr.csv')
            expander.dataframe(data)
            
            st.image(f'./data/data_created/protein-TFs_higCorr/Figure/{option}-TFs_highCorr.csv.png')
            
                
    
        
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
    


