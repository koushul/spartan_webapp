import streamlit as st
import streamlit as st

from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from utils.components import local_css
from texts.descriptions import DatasetDesc, Desc

@st.cache
def totags(tags):
    t = '<div>'
    for tag, color in zip(tags, ['red', 'blue', 'green', 'orange']):
        t += f"<span class='highlight {color}'>{tag}</span>\t"
    t += '</div>'
    return t


from st_aggrid import JsCode


def dataset_page(ds, datacore):
    st.header(f'Dataset Browser')
    st.info(Desc.ds)
    st.caption('Select one or more datasets')
    ds2 = ds[['name', 'organism', 'patients', 'cell count', 'assay', 'pmid', 'severity']]
    gd = GridOptionsBuilder.from_dataframe(ds2)
    
    if 'datasets' in st.session_state:
        pre_selected_rows = [list(ds.name).index(i) for i in st.session_state['datasets']]
    else:
        pre_selected_rows = []
                
                
    gd.configure_selection(selection_mode='multiple', use_checkbox=True, pre_selected_rows=pre_selected_rows)
    
    js = JsCode("""function(params) {return '<a href="https://www.google.com">888</a>'}""")     

    grid_table = AgGrid(ds2, 
        gridOptions=gd.build(),
        update_mode=GridUpdateMode.SELECTION_CHANGED, 
        fit_columns_on_grid_load=True,
        height=155,
        width='100%',
        theme="streamlit",
    )

        
    selected_row = grid_table["selected_rows"]
    
    st.session_state['datasets'] = [x['name'] for x in selected_row]
    
    for idx, row_json in enumerate(selected_row):
        
        st.header(row_json['name'] + ': ' + ds[ds.name==row_json['name']].title.values[0])
        st.markdown(DatasetDesc[row_json['name']])
        st.markdown(ds[ds.name==row_json['name']].url.values[0])
        
        exp = st.expander('View UMAP')
        try:
            exp.image(datacore.name2ds[row_json['name']].umap)
        except:
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