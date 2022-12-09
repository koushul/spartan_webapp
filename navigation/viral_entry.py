import streamlit as st

from utils.components import ridge_plot
import hydralit_components as hc

import time


def viral_entry_page(datacore):
    """
    protein-TFs_higCorr_viral/Figure
    mRNA-TFs_higCorr_viral/Figure
    generate density plots for mRNA(viral entry) from mRNAs_all_…viral.csv and get pvalue from mRNA_wilcox…_viral.csv
    generate density plots for protein(viral entry) from proteinss_all_…viral.csv and get pvalue from protein_wilcox…_viral.csv
        some of the data file may not exist sine no viral protein or genes for that dataset or celltype
    
    """
    a, b = st.columns(2)
    
    datasets = datacore.name2ds.keys()
    

    a.markdown('##### &nbsp;')            
    sbs = b.checkbox('Side-by-Side Plots', value=True)    
        
    p_ds = a.selectbox(f'Dataset ({len(datasets)})', datasets, 0)
    cell_types = datacore.name2ds[p_ds].celltypes
    cell_type = b.selectbox(f'Cell Type ({len(cell_types)})', cell_types, 0)
    
    s_proteins = list(datacore.name2ds[p_ds].get_viral_proteins(cell_type))

    
    show_protein_tf = b.checkbox('Viral protein-TF correlations')
    show_mrna_tf = b.checkbox('Viral mRNA-TF correlations')
    
    show_mrna_density = a.checkbox('Viral mRNA distributions')
    show_protein_density  = a.checkbox('Viral protein distributions')
    
    
    st.markdown('---')    

    if sbs:
        if show_protein_tf or show_mrna_tf:
            st.markdown('#### Viral protein-TF correlations')
            st.caption('Click on image corner to enlarge')
        
        columns = st.columns(len(s_proteins))
        
        for c, p in zip(columns, s_proteins):
            c.markdown('##### ' + p)
          
        if show_protein_tf:
            for cols, option_protein in zip(columns, s_proteins):
                with cols:
                    with hc.HyLoader(f'🎨 Painting {option_protein}', hc.Loaders.standard_loaders,index=[3]):
                        csv, img = datacore.name2ds[p_ds].get_viral_protein_data(cell_type, option_protein)
                        st.image(img)
                        
            st.markdown('---')
    
    else:
        if show_protein_tf:
            for option_protein in s_proteins:
                st.markdown('##### '+option_protein)
                
                with hc.HyLoader(f'🎨 Painting {option_protein}', hc.Loaders.standard_loaders,index=[3]):
                    csv, img = datacore.name2ds[p_ds].get_viral_protein_data(cell_type, option_protein)
                    st.image(img)
                    
        st.markdown('---')
        
                    
                    

                    
                    
                    
                                # df_plt = datacore.name2ds[p_ds].get_protein_df(cell_type, option_protein)
                    # img_ridge = ridge_plot(df_plt, f'{option_protein} expression', column=None)
                    
                                
    
    
            

    
    
    # if show_density or show_heatmap:
    #     title = 
        
    #     with hc.HyLoader(title, hc.Loaders.standard_loaders,index=[3]):

    #         for option_protein in s_proteins:
    #             csv, img = datacore.name2ds[p_ds].get_viral_protein_data(cell_type, option_protein)
            
    #             df_plt = datacore.name2ds[p_ds].get_protein_df(cell_type, option_protein)
    #             img_ridge = ridge_plot(df_plt, f'{option_protein} expression', column=None)
                
    #             if show_density: st.image(img)
    #             if show_heatmap: st.image(img_ridge)
                
    #             st.markdown('---')

            
            
    
        
    