import uuid

import extra_streamlit_components as stx
import pandas as pd
import streamlit as st
from navigation.datasets import dataset_page
from navigation.doc import doc_page

from navigation.home import home_page, TITLE
from navigation.stats import stats_page
from utils.components import create_st_button, local_css, make_tab, ridge_plot
from utils.dataloaders import Dataset
from utils.api import get_pubmed_article, litcov_search, severus_pair, load_drug_info, load_tftargets

from utils.components import ppi, hide_streamlit_style
from texts.descriptions import Desc
from utils.dataloaders import make_datacore

from texts.references import CELL_NAMES

from PIL import Image



Image.MAX_IMAGE_PIXELS = None



HOME = "Home"
DATASET = "Datasets"
TF = "Analysis by transcription factors"
PROTEINS = "Analysis by surface proteins"
VIRAL_ENTRY = "Analysis by viral entry related factors"
TF_PROTEINS = "TF-Protein Pairs"
DOC = "Documentation"
STATS = "Usage Statistics"

st.set_page_config(
    page_title=TITLE,
    page_icon="./assets/logos/spartan.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

def totags(tags):
    t = '<div>'
    for tag, color in zip(tags, ['red', 'blue', 'green', 'orange']):
        t += f"<span class='highlight {color}'>{tag}</span>\t"
    t += '</div>'
    return t


def st_url(text, link, tags='######'):
    st.write(tags+f" [{text}]({link})")



tabs = [
    HOME,
    DATASET,
    PROTEINS,
    TF,
    VIRAL_ENTRY,
    # TF_PROTEINS,
    DOC, 
    STATS
]


datacore =  make_datacore()()
ds = Dataset.metadata_df()
drugs = load_drug_info()



st.markdown(hide_streamlit_style, unsafe_allow_html=True) ## Footer

# chosen_tab = stx.tab_bar(data=[make_tab(t) for t in tabs], default=tabs[0]) 
chosen_tab = st.sidebar.radio('Page', tabs)

if chosen_tab == HOME:
    home_page()
    
    
elif chosen_tab == DATASET:
    x, y, z = st.columns([1, 6, 1])
    with y:
        dataset_page(ds, datacore)
    

    
elif chosen_tab == TF:
    
    # st.header('TF exploration')
    st.info(Desc.tf)
    ref = 'Literature References'
    
    _, _, edge = st.columns(3)
    checkbox = edge.checkbox('Show high correlations only')
    aa, ba, ca = st.columns(3)
    st.session_state['datasets'] = ["GSE155673"]
    

    datasets = datacore.name2ds.keys()
    tf_ds = aa.selectbox(f'Dataset ({len(datasets)})', datasets, 1)
    cell_types = datacore.name2ds[tf_ds].celltypes
    cell_type = ba.selectbox(f'Cell Type ({len(cell_types)})', cell_types, 0)

    if not checkbox:
        tfs = datacore.name2ds[tf_ds].total_transcription_factors            
    else:
        tfs = list(datacore.name2ds[tf_ds].transcription_factors(cell_type))
    
    option = ca.selectbox(
        f'Transcription factor of interest ({len(tfs)})', tfs)   
    
    
    litcovdf = litcov_search(option)
    
    targets = drugs[drugs.Target.apply(lambda x: option in x)]


    ## TF subtabs
    subtabs = [
        'TF activities', 
        'TF-Target gene', 
        'TF-protein correlation', 
        f'Drugs ({len(targets)})',
        f'Literature references ({len(litcovdf)})', 
        'PPI', 
        'Download'
    ]

    
    if 'current_tab_tf' in st.session_state:
        current_tab_tf = st.session_state['current_tab_tf']
    else:
        current_tab_tf = subtabs[1]
                
    chosen_subtab = stx.tab_bar(data=[make_tab(t) for t in subtabs], default=current_tab_tf) 
    st.session_state['current_tab_tf'] = chosen_subtab
    
    
    
    
    if 'Literature references' in chosen_subtab:
        # st.caption(Desc.litcovid)
        st.markdown(f'### 📄 Relevant publications for {option} based on LitCovid')
        
        if len(litcovdf) > 0: 
            for title in litcovdf.title:
                article = get_pubmed_article(title)
                if article:
                    pmid = article.pubmed_id.split()[0]
                    st_url(text=article.title, link=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}")
                    with st.expander('Abstract'):
                        st.write(article.abstract)
                    
                    local_css()
                    author = article.authors[0]
                    author = f"{author['lastname']} et al. ({article.publication_date.year})"
                    
                    st.markdown(totags([author, article.journal, "PMID:"+pmid]), unsafe_allow_html=True)
                    
                    st.markdown('---')
                
                
        # if len(litcovdf) > 0:  
        #     st.table(litcovdf)
        #     st.download_button(
        #         label='Download as CSV',
        #         data=litcovdf.to_csv(index=None),
        #         file_name=f'references_{option}.csv',
        #         mime='text/csv',
        #         key=uuid.uuid1()
        #     )
                
        else:
            st.warning('No literature references found')
    
    elif chosen_subtab == 'TF-Target gene':
        st.markdown(f'### 🎯 {option}-Target genes correlation in {CELL_NAMES.get(cell_type, cell_type)}') 
        
        with st.spinner('Loading heatmap...'):
            try:
                img = datacore.name2ds[tf_ds].get_tf_target_gene_img(cell_type, option)
                st.image(img)
            except:
                st.warning('No high correlation matches found.')
                
        st.markdown('---')
        targets = load_tftargets(option)
        st.subheader(f'{option} has {len(targets)} target genes')
        left, right = st.columns(2)
        
        if len(targets) > 0:
            with left:
                target_name = st.selectbox('Targets', targets.target_name.values)
                target_ensg = targets[targets.target_name==target_name].target_id.values[0]
            
            with left:
                _s = '!'
                create_st_button(
                    link_text=f'View epigenomic states for {target_name}', 
                    link_url=f'http://bioinfo.life.hust.edu.cn/hTFtarget#{_s}/epigenomic_states?gene={target_ensg}&tf={option}&scale=2')
            
            st.table(targets)
    
    elif chosen_subtab == f'Drugs ({len(targets)})':
        if len(targets) > 0:
            st.table(targets)
        else:
            st.warning('No drug targets found.')
    
    elif chosen_subtab == 'PPI':
        ppi(option)
        
        st.markdown(f'### Pathways & drugs associated with {option} derived from Wiki-CORONA')
        
        try:
            df = pd.read_html(f'http://severus.dbmi.pitt.edu/corona/index.php/search?q={option}')[0]
            df.columns = ['Interactant Symbol', 'Name', 'Associated Pathways', 'Binding Drugs', 'Associated Diseases']
            st.dataframe(df)
        except:
            st.warning('No interactors found from Wiki-CORONA')
            
        
    elif chosen_subtab == 'TF activities':              
        try:
            st.markdown(f'### 📈 Inferred {option} activity in {CELL_NAMES.get(cell_type, cell_type)}')  
            pval, adj_pval = datacore.name2ds[tf_ds].get_tf_pvals(cell_type, option)
            if pval < 0.05:
                st.success(f'Healthy vs Infected: p-value = {pval:.3f}')
            else:
                st.error(f'Healthy vs Infected: p-value = {pval:.3f}')
                
            
            df_plt = datacore.name2ds[tf_ds].get_tf_df(cell_type, option)
            c, d, e = st.columns([2, 6, 2])
            img = ridge_plot(df_plt, f'{option} inferred rank', column=c)
            # x = st.slider('x', int(img.size[0]/2), int(img.size[0]*2), img.size[0], 50)
            # y = st.slider('y', int(img.size[1]/2), int(img.size[1]*2), img.size[1], 50)
            # d.image(img.resize((x, y)))
            xx, yy = img.size
            dd = 2.5
            xx = int(xx/dd)
            yy = int(yy/dd)
            d.image(img.resize((xx, yy)))

        except:
            st.warning('No high correlation matches found.')

        
    elif chosen_subtab == 'TF-protein correlation':
        st.markdown(f'### 🔗 Correlation between {option} and surface protein expression in {CELL_NAMES.get(cell_type, cell_type)}')

        
        try:
            csv, img = datacore.name2ds[tf_ds].get_tf_protein_data(cell_type, option)
            st.image(img)
            exp = st.expander('Raw Data')
            exp.dataframe(pd.read_csv(csv))
        except:
            st.warning('No high correlation matches found.')
            
        
        

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
        
elif chosen_tab == PROTEINS:
    # st.title('Surface protein exploration')
    st.info('Search surface protein across COVID-19 patients and health individuals. For a single surface protein, SPaRTAN COVID-19db supports exploring its expression for each cell type, correlated transcription factors, protein-protein interactions and relevant literature.')
    
    _, _, edge = st.columns(3)
    
    checkbox = edge.checkbox('Show high correlations only')
    
    a, b, c = st.columns(3)
    
    st.session_state['datasets'] = ["GSE155673"]
    
        
    datasets = datacore.name2ds.keys()
    p_ds = a.selectbox(f'Dataset ({len(datasets)})', datasets, 0)
    cell_types = datacore.name2ds[p_ds].celltypes
    cell_type = b.selectbox(f'Cell Type ({len(cell_types)})', cell_types, 0)
    
    if not checkbox:
        s_proteins = list(datacore.name2ds[p_ds].total_surface_proteins)
    else:
        s_proteins = list(datacore.name2ds[p_ds].surface_proteins(cell_type))


    option = c.selectbox(
        f"Surface protein of interest ({len(s_proteins)})",
        s_proteins)
    
        
    o = option
    
    try:    
        litcovdf = litcov_search(o)
    except:
        litcovdf = pd.DataFrame([])

        
    subtabs = ['Protein expression', 'Protein-TF correlation', f'Literature references ({len(litcovdf)})', 'PPI', 'Download']
    if 'current_tab' in st.session_state:
        current_tab = st.session_state['current_tab']
    else:
        current_tab = subtabs[1]
        
    
    chosen_subtab = stx.tab_bar(data=[make_tab(t) for t in subtabs], default=current_tab) 
    
    st.session_state['current_tab'] = chosen_subtab
        
    
    if chosen_subtab == 'PPI':
        ppi(o)
        
        st.markdown(f'### Pathways & drugs associated with {o} derived from Wiki-CORONA')
        
        try:
            df = pd.read_html(f'http://severus.dbmi.pitt.edu/corona/index.php/search?q={o}')[0].dropna()
            df.columns = ['Interactant Symbol', 'Name', 'Associated Pathways', 'Binding Drugs', 'Associated Diseases']
            st.dataframe(df)
        except:
            st.warning('No interactors found from Wiki-CORONA')
        
        
    elif chosen_subtab == 'Protein-TF correlation':
        st.markdown(f'### 🔗 Correlation between {option} expression and inferred TF activities in {CELL_NAMES.get(cell_type, cell_type)}')
        
        try:
            csv, img = datacore.name2ds[p_ds].get_protein_tf_data(cell_type, option)            
            st.image(img)
            exp = st.expander('Raw Data')            
            exp.dataframe(pd.read_csv(csv))
        except:
            st.warning('No high correlation matches found.')
            
            
        
    elif chosen_subtab == 'Protein expression':
        
        try:
            st.markdown(f'### 📈 {o} expression in {CELL_NAMES.get(cell_type, cell_type)}')  
            
            pval, adj_pval = datacore.name2ds[p_ds].get_protein_pvals(cell_type, option)
                        
            if pval < 0.05:
                st.success(f'Healthy vs Infected: p-value = {pval:.3f}')
            else:
                st.error(f'Healthy vs Infected: p-value = {pval:.3f}')
                
            df_plt = datacore.name2ds[p_ds].get_protein_df(cell_type, option)
            c, d, e = st.columns([1, 6, 1])
            img = ridge_plot(df_plt, f'{option} expression', column=c)
            # x = st.slider('x', int(img.size[0]/2), int(img.size[0]*2), img.size[0], 50)
            # y = st.slider('y', int(img.size[1]/2), int(img.size[1]*2), img.size[1], 50)
            # d.image(img.resize((x, y)))
            xx, yy = img.size
            dd = 2.5
            xx = int(xx/dd)
            yy = int(yy/dd)
            d.image(img.resize((xx, yy)))

        except:
            st.warning('No high correlation matches found.')
        
        
    elif 'Literature references' in chosen_subtab:
        # st.caption(Desc.litcovid)
        st.markdown(f'### 📄 Relevant publications for {option} based on LitCovid')
        
        
        if len(litcovdf) > 0: 
            for title in litcovdf.title:
                article = get_pubmed_article(title)
                if article:
                    pmid = article.pubmed_id.split()[0]
                    st_url(text=article.title, link=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}")
                    with st.expander('Abstract'):
                        st.write(article.abstract)
                    
                    local_css()
                    author = article.authors[0]
                    author = f"{author['lastname']} et al. ({article.publication_date.year})"
                    
                    st.markdown(totags([author, article.journal, "PMID:"+pmid]), unsafe_allow_html=True)
                    
                    st.markdown('---')
        
        
        
        # if len(litcovdf) > 0:  
        #     st.table(litcovdf)
        #     st.download_button(
        #         label='Download as CSV',
        #         data=litcovdf.to_csv(index=None),
        #         file_name=f'references_{option}.csv',
        #         mime='text/csv',
        #         key=uuid.uuid1()
        #     )
                
        else:
            st.warning('No literature references found')
        
elif chosen_tab == VIRAL_ENTRY:
    st.image('./assets/images/under_construction.png')

        
elif chosen_tab == DOC:
    doc_page()
    
elif chosen_tab == STATS:
    stats_page()
        
