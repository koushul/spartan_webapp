import uuid

import extra_streamlit_components as stx
import pandas as pd
import streamlit as st

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


datacore =  make_datacore()()
ds = Dataset.metadata_df()


st.markdown(hide_streamlit_style, unsafe_allow_html=True) ## Footer

chosen_tab = stx.tab_bar(data=[make_tab(t) for t in tabs], default=tabs[0]) 

if chosen_tab == 'Home':
    home_page()
    
    
elif chosen_tab == 'Dataset':
    st.header(f'Dataset Browser')
    st.info(Desc.ds)
    st.caption('Select one or more datasets')
    ds2 = ds[['name', 'organism', 'patients', 'cell count', 'assay', 'pmid']]
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
        st.header(row_json['name'] + ': ' + ds[ds.name==row_json['name']].title.values[0])
        st.markdown(DatasetDesc[row_json['name']])
        st.markdown(ds[ds.name==row_json['name']].url.values[0])
        
        exp = st.expander('View UMAP')
        try:
            exp.image(datacore.name2ds['GSE155673'].umap)
        except FileNotFoundError:
            exp.write('No UMAP available.')

        local_css()
        
        st.markdown(
            totags([
                row_json['organism'], 
                row_json['assay'], 
                row_json['cell count'] + ' cells', 
                str(row_json['patients']) + ' patients']), 
            unsafe_allow_html=True)
        
        st.markdown('---')
          
elif chosen_tab == 'Transcription Factors':
    st.header('TF Exploration')
    st.info(Desc.tf)
    ref = 'Literature References'
    
    aa, ba, ca = st.columns(3)
    
    if 'grid' in st.session_state and st.session_state['datasets']:
        tf_ds = aa.multiselect('Dataset', datacore.name2ds.keys(), st.session_state['datasets'])
    else:
        tf_ds = aa.multiselect('Dataset', datacore.name2ds.keys(), ["GSE155673"])
        
    cell_type = ba.selectbox('Cell Type', datacore.name2ds["GSE155673"].cell_types, 2)
    option = ca.selectbox(
        "Transcription Factor of interest",
        datacore.name2ds["GSE155673"].transcription_factors(cell_type))
    

    

            
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
            st.table(litcovdf)
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
        
    elif chosen_tab == 'TF Activities':
        st.write(datacore.name2ds)
        st.write(datacore.name2ds.keys())
        

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
    st.title('Surface Protein Exploration')
    st.info('Search surface protein across COVID-19 patients and health individuals. For a single surface protein, SPaRTAN COVID-19db supports exploring its expression for each cell type, correlated transcription factors, protein-protein interactions and relevant literature.')
    a, b, c = st.columns(3)
        
    if 'grid' in st.session_state and st.session_state['datasets']:
        p_ds = a.multiselect('Dataset', datacore.name2ds.keys(), st.session_state['datasets'])
    else:
        p_ds = a.multiselect('Dataset', datacore.name2ds.keys(), ["GSE155673"])
    
    
    cell_type = b.selectbox('Cell Type', datacore.name2ds[p_ds[0]].cell_types, 2)
    
    s_proteins = list(datacore.name2ds[p_ds[0]].surface_proteins(cell_type))
    
    option = c.selectbox(
        "Surface Protein of interest",
        s_proteins)
        
    o = option.split('--')[0]
    
    try:    
        litcovdf = litcov_search(o)
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
        ppi(o)
        
        
    elif chosen_subtab == 'Protein-TF Correlation':
        st.header(f'🔎 {o}')
        
        csv, img = datacore.name2ds[p_ds[0]].get_protein_tf_data(cell_type, option)
        st.image(img)
        exp = st.expander('Raw Data')
        exp.dataframe(pd.read_csv(csv))
        
    elif chosen_subtab == 'Protein Expression':
        df_plt = datacore.name2ds[p_ds[0]].get_protein_df(cell_type, option)
        st.pyplot(ridge_plot(df_plt))
        
        
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
    


