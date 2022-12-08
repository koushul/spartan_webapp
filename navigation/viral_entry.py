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
    
    a, b, c = st.columns(3)
    
    st.session_state['datasets'] = ["GSE155673"]
    
        
    datasets = datacore.name2ds.keys()
    p_ds = a.selectbox(f'Dataset ({len(datasets)})', datasets, 0)
    cell_types = datacore.name2ds[p_ds].celltypes
    cell_type = b.selectbox(f'Cell Type ({len(cell_types)})', cell_types, 0)
    
    s_proteins = list(datacore.name2ds[p_ds].get_viral_proteins(cell_type))

    show_density = a.checkbox('Show all density plots')
    show_heatmap = b.checkbox('Show all heatmaps')
    # option_protein = c.selectbox(
    #     f"Surface protein of interest ({len(s_proteins)})",
    #     s_proteins)
    
    option_data = [{'icon': "", 'label':p} for p in s_proteins]

    over_theme = {'txc_inactive': 'black','menu_background':'white','txc_active':'white','option_active':'red'}

    font_fmt = {'font-class':'h3','font-size':'50%'}


    option_protein = hc.option_bar(
        option_definition=option_data,
        title='',
        override_theme=over_theme,
        horizontal_orientation=True)
    
    csv, img = datacore.name2ds[p_ds].get_viral_protein_data(cell_type, option_protein)
    
    
    # for option_protein in s_proteins:
    #     csv, img = datacore.name2ds[p_ds].get_viral_protein_data(cell_type, option_protein)
    #     df_plt = datacore.name2ds[p_ds].get_protein_df(cell_type, option_protein)
        
    #     img_ridge = ridge_plot(df_plt, f'{option_protein} expression', column=None)
    
    #     st.image(img_ridge)
    
    if show_density or show_heatmap:
        left, right = st.columns(2)
        title = '🎨 Generating plots'
        
        with hc.HyLoader(title, hc.Loaders.standard_loaders,index=[3]):
            # time.sleep(10)
            # st.write(img)
            for option_protein in s_proteins:
                csv, img = datacore.name2ds[p_ds].get_viral_protein_data(cell_type, option_protein)
            
                df_plt = datacore.name2ds[p_ds].get_protein_df(cell_type, option_protein)
                img_ridge = ridge_plot(df_plt, f'{option_protein} expression', column=None)
                
                if show_density: left.image(img)
                if show_heatmap: right.image(img_ridge)
                
                left.markdown('---')
                right.markdown('---')
            
            
    
        
    