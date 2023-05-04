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

from utils.dataloaders import get_umap
option_data = [
   {'icon': "", 'label':i} for i in ['Metadata', 'Visualization']]

# override the theme, else it will use the Streamlit applied theme
over_theme = {'txc_inactive': 'black','menu_background':'white','txc_active':'white','option_active':'skyblue'}
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
                st.image('./assets/images/under_construction.png')
                # umap = get_umap(datacore.name2ds[name].name) 
                # if umap is not None:
                #     a, b = st.columns(2)
                    
                #     cell_types = datacore.name2ds[name].celltypes
                #     cell_type = a.selectbox(f'Cell Type ({len(cell_types)})', cell_types, 0)
    
                #     s_proteins = list(datacore.name2ds[name].surface_proteins(cell_type))
                #     option = b.selectbox(
                #             f"Surface protein of interest ({len(s_proteins)})",
                #             s_proteins)
                #     f = plt.figure(figsize=(5, 3.5), dpi=80)
                #     umap.celltypes_sub = umap.celltypes_sub.astype('category')
                #     # norm = plt.Normalize(umap[option].min(), umap[option].max())
                #     # sm = plt.cm.ScalarMappable(cmap='plasma', norm=norm)
                #     # sm.set_array([])
                #     # alpha = [1 if i else 0.2 for i in (umap.celltypes_sub==CELL_NAMES_REVERSE.get(cell_type)).values]
                #     ax = sns.scatterplot(data=umap, x='UMAP_1', y='UMAP_2', hue='celltypes_sub', size=1)
                    
                #     plt.box(False)
                #     ax.get_legend().remove()
                #     # ax.figure.colorbar(sm)
                #     ax.set_xticks([])
                #     ax.set_yticks([])
                #     ax.set_title(f'Dataset: {name}', fontsize=9)
                #     ax.set_xlabel('UMAP_1', fontsize=7)
                #     ax.set_ylabel('UMAP_2', fontsize=7)
                    

                #     st.pyplot(f)

        
        
