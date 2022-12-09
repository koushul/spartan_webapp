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
    sbs = b.checkbox('Side-by-Side Plots')    
        
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
        columns = st.columns(len(s_proteins))
        
        for c, p in zip(columns, s_proteins):
            c.markdown('##### ' + p)
        
        # option_data = [{'icon': "", 'label':p} for p in s_proteins]

        # over_theme = {'txc_inactive': 'black','menu_background':'white','txc_active':'black','option_active':'white'}

        # font_fmt = {'font-class':'h3','font-size':'50%'}


        # option_protein = hc.option_bar(
        #     option_definition=option_data,
        #     title='',
        #     override_theme=over_theme,
        #     horizontal_orientation=True)    
        
        if show_protein_tf:
            with hc.HyLoader('🎨 Generating plots', hc.Loaders.standard_loaders,index=[3]):
                for option_protein in s_proteins:
                    csv, img = datacore.name2ds[p_ds].get_viral_protein_data(cell_type, option_protein)
                
                    # df_plt = datacore.name2ds[p_ds].get_protein_df(cell_type, option_protein)
                    # img_ridge = ridge_plot(df_plt, f'{option_protein} expression', column=None)
                    
                    st.image(img)
                                
    
    
            

    
    
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

            
            
    
        
    