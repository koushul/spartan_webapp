import streamlit as st

from utils.components import ridge_plot



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


    option_protein = c.selectbox(
        f"Surface protein of interest ({len(s_proteins)})",
        s_proteins)
    
    csv, img = datacore.name2ds[p_ds].get_viral_protein_data(cell_type, option_protein)
    df_plt = datacore.name2ds[p_ds].get_protein_df(cell_type, option_protein)
    
    left, right = st.columns(2)
    img_ridge = ridge_plot(df_plt, f'{option_protein} expression', column=None)
    
    right.image(img_ridge)
    
    
    with st.spinner('Loading heatmap...'):
        left.image(img)
    