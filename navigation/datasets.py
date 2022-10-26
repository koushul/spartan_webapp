import streamlit as st
import streamlit as st

from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from utils.components import local_css
from texts.descriptions import DatasetDesc, Desc

def totags(tags):
    t = '<div>'
    for tag, color in zip(tags, ['red', 'blue', 'green', 'orange']):
        t += f"<span class='highlight {color}'>{tag}</span>\t"
    t += '</div>'
    return t

def dataset_page(ds):
    st.header(f'Dataset Browser')
    st.info(Desc.ds)
    ds2 = ds[['name', 'title', 'organism', 'patients', 'cell count', 'platform', ]]
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
        height=149,
        width='100%',
        theme="streamlit",
        key='grid'
    )


        
    selected_row = grid_table["selected_rows"]

    st.session_state['datasets'] = [x['name'] for x in selected_row]

    for idx, row_json in enumerate(selected_row):
        # st.header(row_json['name'])
        st.header(row_json['name'] + ': ' + row_json['title'])
        st.markdown(DatasetDesc[row_json['name']])
        # cols = st.columns(3)
        # cols[0].info(row_json['patients'])  
        local_css()
        st.markdown(
            totags([
                row_json['organism'], 
                row_json['platform'], 
                row_json['cell count'], 
                row_json['patients']]), 
            unsafe_allow_html=True)
        st.markdown('---')