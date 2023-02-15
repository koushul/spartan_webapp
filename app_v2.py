from navigation.datasets import dataset_page
from navigation.doc import doc_page
from navigation.home import home_page
from navigation.multi_dataset_search import multi_dataset_page
from navigation.protein import protein_page
from navigation.stats import stats_page
from navigation.tf import tf_page
from navigation.viral_entry import viral_entry_page
from utils.dataloaders import Dataset
from utils.components import footer_style
from utils.dataloaders import make_datacore

from PIL import Image
import streamlit as st

import hydralit_components as hc


st.set_page_config(
        page_title='COVID-19db of Immune Cell States',
        page_icon="./assets/logos/spartan.png",
        # layout="wide",
        initial_sidebar_state="expanded",
)


max_width_str = f"max-width: {75}%;"
st.markdown(f"""
        <style>
        .appview-container .main .block-container{{{max_width_str}}}
        </style>
        """,
        unsafe_allow_html=True,
    )

st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    
                }
        </style>
        """, unsafe_allow_html=True)

    

Image.MAX_IMAGE_PIXELS = None

HOME = "Home"
DATASET = "Datasets"
TF = "Transcription factors"
PROTEINS = "Surface proteins"
VIRAL_ENTRY = "Viral-entry related factors"
MULTI = "Multi datasets"
DOC = "Docs"
CONTACT = "Contact"
STATS = "Usage"


datacore =  make_datacore()()
ds = datacore.metadata




hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


icons = """<style>
        img {
            max-width: 100%;
        
        }
        
        .headerStyle {
            transition: transform .2s;
        }
        
        .headerStyle:hover {
            
             transform: scale(1.5);
            transition: 0.2s;
        }
        .image1 { 
            padding: 10px;
             transition: transform .2s;
        }
        .image2 
        { 
            padding: 10px;
             transition: transform .2s;
        }
        .image1:hover {  
            ##border: 4px solid green;
            ##border-radius: 15px;
             transform: scale(1.5);
            transition: 0.2s;
        }

        .image2:hover {  
            ##border: 4px solid green;
            ##border-radius: 15px;
             transform: scale(1.5);
            transition: 0.2s;
        }
        
        a:link,
        a:visited {
            color: blue;
            background-color: transparent;
            text-decoration: underline;
        }

        a2:hover {
            border-style: solid;
            },
        a:active {
            color: red;
            background-color: transparent;
            text-decoration: underline;
        }
    
        .footer {
            position: fixed;
            width: 100%;
            background-color: white;
            color: black;
            display: block;
            text-align: center;
            padding: 100px;
            top: 0px;
        }
</style
<div class="footer">
        <a href="https://scholar.google.com/citations?user=YzCsmdgAAAAJ&hl=en&inst=7044483460239389945"><img class="image2" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Google_Scholar_logo.svg/512px-Google_Scholar_logo.svg.png"
                alt="github" width="60" height="60">
        </a>
        <a href="https://www.instagram.com/osmanbeyoglulab/"><img class="image2" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/132px-Instagram_logo_2016.svg.png"
                alt="github" width="60" height="60">
        </a>
        <a href="https://github.com/osmanbeyoglulab"><img class="image2" src="https://cdn-icons-png.flaticon.com/512/25/25231.png"
                alt="github" width="60" height="60">
        </a>
        <a href="https://twitter.com/hosmanbeyoglu?lang=en"><img class="image2" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Twitter-logo.svg/292px-Twitter-logo.svg.png"
            alt="twitter" width="65" height="60"></a>
</div>
""" ## Footer
footer="""<style>
img {
            max-width: 100%;
        
        }
        
        .headerStyle {
            transition: transform .2s;
        }
        
        .headerStyle:hover {
            
             transform: scale(1.5);
            transition: 0.2s;
        }
        .image1 { 
            padding: 10px;
             transition: transform .2s;
        }
        .image2 
        { 
            padding: 10px;
             transition: transform .2s;
        }
        .image1:hover {  
            ##border: 4px solid green;
            ##border-radius: 15px;
             transform: scale(1.5);
            transition: 0.2s;
        }

        .image2:hover {  
            ##border: 4px solid green;
            ##border-radius: 15px;
             transform: scale(1.5);
            transition: 0.2s;
        }
        
        a:link,
        a:visited {
            color: blue;
            background-color: transparent;
            text-decoration: underline;
        }

        a2:hover {
            border-style: solid;
            },
        a:active {
            color: red;
            background-color: transparent;
            text-decoration: underline;
        }

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
padding: 24px;
text-align: center;
}
</style>
<div class="footer">
<p style="font-size:  13px">© 2023 Osmanbeyoglulab.com. All rights reserved.</p>
<a href="https://hillman.upmc.com/"><img class="image2" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7c7pXIkFgMPVM2csVE6MenUFLEsgF5beCeMJzogkPkXPC4xEo9OTHf6nVpqsb3PvisRk&usqp=CAU"alt="github" width="70" height=50"></a>
<a href="https://www.pitt.edu/"><img class="image2" src="https://upload.wikimedia.org/wikipedia/en/thumb/f/fb/University_of_Pittsburgh_seal.svg/300px-University_of_Pittsburgh_seal.svg.png"alt="github" width="45" height="45"></a>
</a><a href="https://github.com/osmanbeyoglulab"><img class="image2" src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="github" width="45" height="45"></a>
<a href="https://twitter.com/hosmanbeyoglu?lang=en"><img class="image2" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Twitter-logo.svg/292px-Twitter-logo.svg.png"alt="twitter" width="45" height="40"></a>
<a href="https://scholar.google.com/citations?user=YzCsmdgAAAAJ&hl=en&inst=7044483460239389945"><img class="image2" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Google_Scholar_logo.svg/512px-Google_Scholar_logo.svg.png"alt="github" width="45" height="45"></a>
<a href="https://www.instagram.com/osmanbeyoglulab/"><img class="image2" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/132px-Instagram_logo_2016.svg.png"alt="github" width="45" height="45"></a>
</div>
"""

# """        """

# footer_style = f"""
#     <style>
#         MainMenu {{visibility: hidden;}}
#         footer {{visibility: hidden;}}
#         footer:after {{
#             content:''; 
#             visibility: visible;
#             display: block;
#             position: relative;
#             # background-color: red;
#             padding: 5px;
#             top: 2px;
#         }}
#     </style>
# """

# st.markdown(footer_style, unsafe_allow_html=True) ## Footer


tabs = [
    HOME,
    DATASET,
    PROTEINS,
    TF,
    VIRAL_ENTRY,
    DOC, 
    STATS,
    CONTACT
]

option_data = [
   {'icon': "🏠", 'label':HOME},
   {'icon':"💾",'label':DATASET},
   {'icon': "🔎", 'label':PROTEINS},
   {'icon': "🔎", 'label':TF},
   {'icon': "🔍", 'label':VIRAL_ENTRY},
   {'icon': "💼 💼", 'label':"Multi datasets"},
   {'icon': "📋", 'label':DOC},
   {'icon': "📩", 'label':CONTACT},
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

# st.markdown('----')
    
#######--------------------#######
#######--------------------#######

if chosen_tab == HOME:
    home_page()
    
    
if chosen_tab == CONTACT:
    import numpy as np
    import pandas as pd
    data = pd.DataFrame([40.454657, -79.943872], index=['lat', 'lon']).T
    
    a, b = st.columns([1, 1.5])
    b.map(data=data, zoom=13, use_container_width=True)  
    
    a.markdown('## Contact Information')  
    a.markdown('#####  Koushul Ramjattun (Graduate Researcher)')
    a.markdown('###### kor11@pitt.edu')    
    a.markdown('##### Xiaojun Ma (Senior Software Engineer)')
    a.markdown('###### xim33@pitt.edu')
    
    a.markdown('---')
    a.markdown('#### Location')  
    a.markdown('5051 Centre Avenue Pittsburgh, PA 15213')
    
    
    
        
elif chosen_tab == DATASET:
    dataset_page(ds, datacore)
    
elif chosen_tab == TF:
    tf_page(datacore)
    
elif chosen_tab == PROTEINS:
    protein_page(datacore)
        
elif chosen_tab == VIRAL_ENTRY:
    viral_entry_page(datacore)
        
elif chosen_tab == MULTI:
    multi_dataset_page(datacore)
          
elif chosen_tab == DOC:
    doc_page()
    
elif chosen_tab == STATS:
    stats_page()

st.markdown(footer,unsafe_allow_html=True)
        
# st.markdown(icons, unsafe_allow_html=True)
