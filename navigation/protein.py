import random
import pandas as pd
import streamlit as st
import hydralit_components as hc
from texts.references import CELL_NAMES

from utils.api import get_pubmed_article, litcov_search
from utils.components import local_css, ppi, ridge_plot, st_url, totags

def generate_color():
    random_number = random.randint(0,16777215)
    hex_number = str(hex(random_number))
    hex_number ='#'+ hex_number[2:]
    return hex_number
        

protein_bar = {'txc_inactive': 'black','menu_background':'white','txc_active':'white','option_active':'blue'}


def protein_page(datacore):
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

        
    subtabs = ['Protein expression', 'Protein-TF correlation', 'Drugs', f'Literature references ({len(litcovdf)})', 'PPI', 'Download']
    if 'current_tab' in st.session_state:
        current_tab = st.session_state['current_tab']
    else:
        current_tab = subtabs[1]
        
        
    option_data2 = [{'icon': icon, 'label':label} for label, icon in zip(subtabs, ['📈', '🔗', '💊', '📚', '🔄','📩'])]
    
    chosen_subtab = hc.option_bar(
        option_definition=option_data2,
        title='',
        key='Sub2',
        override_theme=protein_bar,
        # font_styling=font_fmt,
        horizontal_orientation=True)
    
    # chosen_subtab = stx.tab_bar(data=[make_tab(t) for t in subtabs], default=current_tab) 
    
    st.session_state['current_tab'] = chosen_subtab
        
    if chosen_subtab == 'Drugs':
        st.image('./assets/images/under_construction.png')
    
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
            
            df_plt = datacore.name2ds[p_ds].get_protein_df(cell_type, option)
            
            groups = list(set(df_plt['patient_group'].values))

            if 'healthy' in groups:
                good = 'healthy'
                bad = ', '.join(list(set(groups).difference([good])))
                bad = f'impacted ({bad})'
            elif 'Healthy' in groups:
                good = 'Healthy'
                bad = ', '.join(list(set(groups).difference([good])))
                bad = f'Impacted ({bad})'
                
            else:
                good = groups[0]
                bad = groups[1]
            
            
            # pval, adj_pval = datacore.name2ds[p_ds].get_protein_pvals(cell_type, option)
            # if pval < 0.05:
            #     st.success(f'{good} vs {bad}: p-value = {pval:.3f}')
            # else:
            #     st.error(f'{good} vs {bad}: p-value = {pval:.3f}')
            
                    

            
            c, d, e = st.columns([2.5, 6, 1])
            img = ridge_plot(df_plt, f'{option} expression', column=c)
            # x = st.slider('x', int(img.size[0]/2), int(img.size[0]*2), img.size[0], 50)
            # y = st.slider('y', int(img.size[1]/2), int(img.size[1]*2), img.size[1], 50)
            # d.image(img.resize((x, y)))
            xx, yy = img.size
            dd = 2
            xx = int(xx/dd)
            yy = int(yy/dd)
            d.image(img.resize((xx, yy)))

        except FileNotFoundError:
            st.warning('No high correlation matches found.')
        
        
    elif 'Literature references' in chosen_subtab:
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
        
                
        else:
            st.warning('No literature references found')