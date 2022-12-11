import streamlit as st

from navigation.datasets import dataset_page
from navigation.doc import doc_page
from navigation.home import home_page
from navigation.protein import protein_page
from navigation.stats import stats_page
from navigation.tf import tf_page
from navigation.viral_entry import viral_entry_page
from utils.dataloaders import Dataset
from utils.components import footer_style
from utils.dataloaders import make_datacore

from PIL import Image

import hydralit_components as hc


# st.set_page_config(
#         page_title='COVID-19db of Immune Cell States',
#         page_icon="./assets/logos/spartan.png",
#         # layout="wide",
#         initial_sidebar_state="expanded",
# )



Image.MAX_IMAGE_PIXELS = None

HOME = "Home"
DATASET = "Datasets"
TF = "Transcription factors"
PROTEINS = "Surface proteins"
VIRAL_ENTRY = "Viral entry related factors"
DOC = "Docs"
STATS = "Usage"



datacore =  make_datacore()()
ds = Dataset.metadata_df()

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.markdown(footer_style, unsafe_allow_html=True) ## Footer

# data = [
#     make_tab(HOME),
#     make_tab(DATASET),
#     make_tab("Analysis by", desc="surface proteins"),
#     make_tab("Analysis by", desc="transcription factors"),
#     make_tab("Analysis by", desc="viral entry related factors"),
#     make_tab('MultiDataset'),
#     make_tab(DOC),
#     make_tab(STATS),
# ]



tabs = [
    HOME,
    DATASET,
    PROTEINS,
    TF,
    VIRAL_ENTRY,
    DOC, 
    STATS
]

option_data = [
   {'icon': "🏠", 'label':HOME},
   {'icon':"💾",'label':DATASET},
   {'icon': "🔎", 'label':PROTEINS},
   {'icon': "🔎", 'label':TF},
   {'icon': "🔍", 'label':VIRAL_ENTRY},
   {'icon': "💼 💼", 'label':"Multi datasets"},
   
   {'icon': "📋", 'label':DOC},
   {'icon': "📈", 'label':STATS},
]

over_theme = {'txc_inactive': 'black','menu_background':'white','txc_active':'white','option_active':'red'}
font_fmt = {'font-class':'h3','font-size':'50%'}


chosen_tab = hc.option_bar(
    option_definition=option_data,
    title='',
    key='PrimaryOptionx',
    override_theme=over_theme,
    horizontal_orientation=True)

st.markdown('----')

    
if chosen_tab == "Multi datasets":
    
    st.info("""
        Discover transcription factors that are consistently and significantly different between healthy vs impacted patients
            
    """)
    
    thresh = st.slider('p-value threshold', min_value=0.0, max_value=0.5, value=0.05, step=0.01)
    
    names = list(datacore.name2ds.keys())
    datasets = st.multiselect('Datasets', names, [names[0], names[1]])
    
    if len(datasets) < 1:
        st.error('Please select at least one dataset.')
        
    else:
        common_celltypes = set.intersection(*[set(datacore.name2ds[ds].celltypes) for ds in datasets])    
        results = {} 
        
        my_bar = st.progress(0)
        
        with st.spinner(f'👀 Looking for tfs across {len(datasets)} datasets... (p-value < {thresh})'):
            for idx, ct in enumerate(common_celltypes):
                results[ct] = {}
                for ds in datasets:
                    results[ct][ds] = {}
                    tfs = list(datacore.name2ds[ds].transcription_factors(ct))
                    for tf in tfs:
                        try:
                            pval, adj_pval = datacore.name2ds[ds].get_tf_pvals(ct, tf)
                        except IndexError:
                            pval = 1.0
                        if pval < thresh:
                            results[ct][ds][tf] = pval
                my_bar.progress((idx)/(len(common_celltypes)-1))
                        
        celebrate = False                  
        for ct in common_celltypes:
            significant_tfs = set.intersection(*[set(results[ct][ds].keys()) for ds in datasets])
            if len(significant_tfs)>0:
                celebrate = True
                st.markdown('## '+ct)
                st.write(significant_tfs)
                
                cols = st.columns(len(datasets))
                
                for stf in significant_tfs:
                    for col, ds in zip(cols, datasets):
                        col.metric(label=f'{stf} | {ds}', value = round(results[ct][ds][stf], 4), help='p-value computed using wilcox test')
                        
                st.markdown('---')
                
        if celebrate:
            st.balloons()
        
    
if chosen_tab == HOME:
    home_page()
    
elif chosen_tab == DATASET:
    dataset_page(ds, datacore)
    
elif chosen_tab == TF:
    tf_page(datacore)
    
elif chosen_tab == PROTEINS:
    protein_page(datacore)
        
elif chosen_tab == VIRAL_ENTRY:
    viral_entry_page(datacore)
        
elif chosen_tab == DOC:
    doc_page()
    
elif chosen_tab == STATS:
    stats_page()
        
