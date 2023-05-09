import streamlit as st

from utils.components import local_css
from texts.descriptions import DatasetDesc, Desc

import os
import hydralit_components as hc

option_data = [
   {'icon': "", 'label':i} for i in ['Metadata', 'Visualization']]

over_theme = {'txc_inactive': 'black','menu_background':'white','txc_active':'white','option_active':'darkviolet'}
font_fmt = {'font-class':'h3','font-size':'50%'}

def totags(tags):
    t = '<div>'
    for tag, color in zip(tags, ['red', 'blue', 'green', 'orange', 'purple', 'yellow']):
        t += f"<span class='highlight {color}'>{tag}</span>\t"
    t += '</div>'
    return t


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

    bbox = {}
    
    for name, patients, cells, proteins, tfs, pmid in ds2.values:
        bbox[name] = box.checkbox(f'{name}', key=f'datasets_{name}')  
        p.write(str(patients))  
        c.write(cells)
        pt.write(str(proteins))
        tf.write(str(tfs))
        pm.markdown(f'[{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)')
        

    st.markdown('---')

    
    page = hc.option_bar(
        option_definition=option_data,
        title='',
        override_theme=over_theme,
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
                st.caption('Note: UMAPs were generated using mRNA expression data.')
                try:
                    umap_img, severity_img = datacore.name2ds[name].get_umap_severity()
                    
                    f, _, sa = st.columns(3)          
                    s_proteins = list(datacore.name2ds[name].total_surface_proteins)
                    f.markdown(f'### {name}')
                    if os.path.isfile(umap_img):
                        selected_protein = sa.selectbox(
                            f"Surface protein of interest ({len(s_proteins)})",
                            s_proteins)
                        
                    umap, sev, prot = st.columns(3)
                    
                    if os.path.isfile(umap_img):
                        with umap:
                            with st.spinner('🎨 Coloring by Celltype...'):
                                umap.image(umap_img)
                                umap.caption('Color by Celltype')
                                
                        
                    if os.path.isfile(severity_img):
                        with sev:
                            with st.spinner('🎨 Coloring by Severity...'):
                                sev.image(severity_img)
                                sev.caption('Color by Severity')
                                
                            
                    with prot:
                        with st.spinner('🎨 Coloring by Protein...'):                    
                            prot.image(datacore.name2ds[name].get_feature_plots(selected_protein))
                            prot.caption('Color by Protein Expression')
                            
            
                except:
                    st.error('No UMAPs available for this dataset')
                
                st.markdown('---')
                

        
        
