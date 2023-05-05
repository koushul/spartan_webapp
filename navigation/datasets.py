from matplotlib import pyplot as plt
import streamlit as st

from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from texts.references import CELL_NAMES_REVERSE

from utils.components import local_css
from texts.descriptions import DatasetDesc, Desc

from PIL import Image
import seaborn as sns
import hydralit_components as hc

option_data = [
   {'icon': "", 'label':i} for i in ['Metadata', 'Visualization']]

# override the theme, else it will use the Streamlit applied theme
over_theme = {'txc_inactive': 'black','menu_background':'white','txc_active':'white','option_active':'darkviolet'}
font_fmt = {'font-class':'h3','font-size':'50%'}

def totags(tags):
    t = '<div>'
    for tag, color in zip(tags, ['red', 'blue', 'green', 'orange', 'purple', 'yellow']):
        t += f"<span class='highlight {color}'>{tag}</span>\t"
    t += '</div>'
    return t


from st_aggrid import JsCode

def dataset_page(ds, datacore):
        
    st.markdown(f'### Dataset Browser')
    st.info(Desc.ds)
    st.caption('Select one or more datasets')
    ds2 = ds[['name', 'patients', 'cell_count', 'surface_proteins', 'transcription_factors', 'pmid']]
    
    box, p, c, pt, tf, pm = st.columns([2, 1, 1, 1, 1, 1])
    box.markdown('##### Name')
    p.markdown('##### Patients')
    c.markdown('##### Cells')
    pt.markdown('##### Proteins')
    tf.markdown('##### TFs')
    pm.markdown('##### PMID')
    
    
    
    # st.write(ds2)
    
    bbox = {}
    
    for name, patients, cells, proteins, tfs, pmid in ds2.values:
        bbox[name] = box.checkbox(f'{name}', key=f'datasets_{name}')  
        p.write(str(patients))  
        c.write(cells)
        pt.write(str(proteins))
        tf.write(str(tfs))
        # pm.write(str(pmid))
        pm.markdown(f'[{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)')
        

    st.markdown('---')

    
    page = hc.option_bar(
        option_definition=option_data,
        title='',
        override_theme=over_theme,
        # font_styling=font_fmt,
        horizontal_orientation=True
    )
    
    # if page == 'Visualization':
    #     st.image('./assets/images/under_construction.png')

    for name, is_selected in bbox.items():
        if is_selected:

            if page == 'Metadata':
                st.markdown('#### ' + name + ': ' + ds[ds.name==name].title.values[0])
                st.markdown(DatasetDesc[name])
                st.markdown(ds[ds.name==name].url.values[0])
                
                local_css()
                row_json = ds[ds.name==name]
            
                st.markdown(
                    totags([
                        row_json['cell_count'].values[0] + ' cells', 
                        str(row_json['patients'].values[0]) + ' patients',
                        str(row_json['surface_proteins'].values[0]) + ' surface proteins',
                        str(row_json['transcription_factors'].values[0]) + ' transcription factors',
                        
                        ],
                    ), 
                    unsafe_allow_html=True)
                
                st.markdown('---')
                
                
            elif page == 'Visualization':
                                    
                s_proteins = list(datacore.name2ds[name].total_surface_proteins)

                st.markdown(f'#### {name}')
                
                try:
                    umap_img, severity_img = datacore.name2ds[name].get_umap_severity()
                    
                    umap, sev = st.columns(2)
                    
                    umap.caption('UMAP by Celltype')
                    umap.image(umap_img)
                    sev.caption('UMAP by Severity')
                    sev.image(severity_img)
                    
                    selected_protein = st.selectbox(
                            f"Surface protein of interest ({len(s_proteins)})",
                            s_proteins)
                    
                    st.image(datacore.name2ds[name].get_feature_plots(selected_protein))
                
                    

                    
                    
                except:
                    st.error('No UMAPs available for this dataset')
                
                st.markdown('---')
                

        
        
