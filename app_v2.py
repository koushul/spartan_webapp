# from navigation.datasets import dataset_page
# from navigation.doc import doc_page
# from navigation.home import home_page
# from navigation.multi_dataset_search import multi_dataset_page
# from navigation.protein import protein_page
# from navigation.stats import stats_page
# from navigation.tf import tf_page
# from navigation.viral_entry import viral_entry_page
# from utils.dataloaders import Dataset
# from utils.components import footer_style
# from utils.dataloaders import make_datacore

# from PIL import Image
import streamlit as st

# import hydralit_components as hc


# st.set_page_config(
#         page_title='COVID-19db of Immune Cell States',
#         page_icon="./assets/logos/spartan.png",
#         # layout="wide",
#         initial_sidebar_state="expanded",
# )

st.title('Testing 4551')


# max_width_str = f"max-width: {75}%;"
# st.markdown(f"""
#         <style>
#         .appview-container .main .block-container{{{max_width_str}}}
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# st.markdown("""
#         <style>
#                .block-container {
#                     padding-top: 0rem;
#                     padding-bottom: 0rem;
                    
#                 }
#         </style>
#         """, unsafe_allow_html=True)

    

# Image.MAX_IMAGE_PIXELS = None

# HOME = "Home"
# DATASET = "Datasets"
# TF = "Transcription factors"
# PROTEINS = "Surface proteins"
# VIRAL_ENTRY = "Viral-entry related factors"
# MULTI = "Multi datasets"
# DOC = "Docs"
# CONTACT = "Contact"
# STATS = "Usage"


# datacore =  make_datacore()()
# ds = datacore.metadata




# hide_menu_style = """
#         <style>
#         #MainMenu {visibility: hidden;}
#         </style>
#         """
# # st.markdown(hide_menu_style, unsafe_allow_html=True)


# icons = """<style>
#         img {
#             max-width: 100%;
        
#         }
        
#         .headerStyle {
#             transition: transform .2s;
#         }
        
#         .headerStyle:hover {
            
#              transform: scale(1.5);
#             transition: 0.2s;
#         }
#         .image1 { 
#             padding: 10px;
#              transition: transform .2s;
#         }
#         .image2 
#         { 
#             padding: 10px;
#              transition: transform .2s;
#         }
#         .image1:hover {  
#             ##border: 4px solid green;
#             ##border-radius: 15px;
#              transform: scale(1.5);
#             transition: 0.2s;
#         }

#         .image2:hover {  
#             ##border: 4px solid green;
#             ##border-radius: 15px;
#              transform: scale(1.5);
#             transition: 0.2s;
#         }
        
#         a:link,
#         a:visited {
#             color: blue;
#             background-color: transparent;
#             text-decoration: underline;
#         }

#         a2:hover {
#             border-style: solid;
#             },
#         a:active {
#             color: red;
#             background-color: transparent;
#             text-decoration: underline;
#         }
    
#         .footer {
#             position: fixed;
#             width: 100%;
#             background-color: white;
#             color: black;
#             display: block;
#             text-align: center;
#             padding: 100px;
#             top: 0px;
#         }
# </style
# <div class="footer">
#         <a href="https://scholar.google.com/citations?user=YzCsmdgAAAAJ&hl=en&inst=7044483460239389945"><img class="image2" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Google_Scholar_logo.svg/512px-Google_Scholar_logo.svg.png"
#                 alt="github" width="60" height="60">
#         </a>
#         <a href="https://www.instagram.com/osmanbeyoglulab/"><img class="image2" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/132px-Instagram_logo_2016.svg.png"
#                 alt="github" width="60" height="60">
#         </a>
#         <a href="https://github.com/osmanbeyoglulab"><img class="image2" src="https://cdn-icons-png.flaticon.com/512/25/25231.png"
#                 alt="github" width="60" height="60">
#         </a>
#         <a href="https://twitter.com/hosmanbeyoglu?lang=en"><img class="image2" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Twitter-logo.svg/292px-Twitter-logo.svg.png"
#             alt="twitter" width="65" height="60"></a>
# </div>
# """ ## Footer
# footer="""<style>
# img {
#             max-width: 100%;
        
#         }
        
#         .headerStyle {
#             transition: transform .2s;
#         }
        
#         .headerStyle:hover {
            
#              transform: scale(1.5);
#             transition: 0.2s;
#         }
#         .image1 { 
#             padding: 10px;
#              transition: transform .2s;
#         }
#         .image2 
#         { 
#             padding: 10px;
#              transition: transform .2s;
#         }
#         .image1:hover {  
#             ##border: 4px solid green;
#             ##border-radius: 15px;
#              transform: scale(1.5);
#             transition: 0.2s;
#         }

#         .image2:hover {  
#             ##border: 4px solid green;
#             ##border-radius: 15px;
#              transform: scale(1.5);
#             transition: 0.2s;
#         }
        
#         a:link,
#         a:visited {
#             color: blue;
#             background-color: transparent;
#             text-decoration: underline;
#         }

#         a2:hover {
#             border-style: solid;
#             },
#         a:active {
#             color: red;
#             background-color: transparent;
#             text-decoration: underline;
#         }
# .footer {
# position: relative;
# width: 100%;
# left: 0;
# bottom: 0;
# background-color: white;
# margin-top: auto;
# color: black;
# padding: 24px;
# text-align: center;
# }
# </style>
# <div class="footer">
# <p style="font-size:  13px">© 2023 Osmanbeyoglulab.com. All rights reserved.</p>
# <a href="https://hillman.upmc.com/"><img class="image2" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7c7pXIkFgMPVM2csVE6MenUFLEsgF5beCeMJzogkPkXPC4xEo9OTHf6nVpqsb3PvisRk&usqp=CAU"alt="github" width="70" height=50"></a>
# <a href="https://www.pitt.edu/"><img class="image2" src="https://upload.wikimedia.org/wikipedia/en/thumb/f/fb/University_of_Pittsburgh_seal.svg/300px-University_of_Pittsburgh_seal.svg.png"alt="github" width="45" height="45"></a>
# </a><a href="https://github.com/osmanbeyoglulab"><img class="image2" src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="github" width="45" height="45"></a>
# <a href="https://twitter.com/hosmanbeyoglu?lang=en"><img class="image2" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Twitter-logo.svg/292px-Twitter-logo.svg.png"alt="twitter" width="45" height="40"></a>
# <a href="https://scholar.google.com/citations?user=YzCsmdgAAAAJ&hl=en&inst=7044483460239389945"><img class="image2" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Google_Scholar_logo.svg/512px-Google_Scholar_logo.svg.png"alt="github" width="45" height="45"></a>
# <a href="https://www.instagram.com/osmanbeyoglulab/"><img class="image2" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/132px-Instagram_logo_2016.svg.png"alt="github" width="45" height="45"></a>
# </div>
# """

# # """        """

# footer_style = """
#     <style>
#         MainMenu {visibility: hidden;}
#         footer {visibility: hidden;}
#     </style>
# """

# st.markdown(footer_style, unsafe_allow_html=True) ## Footer


# tabs = [
#     HOME,
#     DATASET,
#     PROTEINS,
#     TF,
#     VIRAL_ENTRY,
#     DOC, 
#     STATS,
#     CONTACT
# ]

# option_data = [
#    {'icon': "🏠", 'label':HOME},
#    {'icon':"💾",'label':DATASET},
#    {'icon': "🔎", 'label':PROTEINS},
#    {'icon': "🔎", 'label':TF},
#    {'icon': "🔍", 'label':VIRAL_ENTRY},
#    {'icon': "💼 💼", 'label':"Multi datasets"},
#    {'icon': "📋", 'label':DOC},
#    {'icon': "📩", 'label':CONTACT},
#    {'icon': "📈", 'label':STATS},
# ]

# over_theme = {'txc_inactive': 'black','menu_background':'white','txc_active':'white','option_active':'red'}
# font_fmt = {'font-class':'h3','font-size':'50%'}

# chosen_tab = hc.option_bar(
#     option_definition=option_data,
#     title='',
#     key='PrimaryOptionx',
#     override_theme=over_theme,
#     horizontal_orientation=True)

# # st.markdown('----')
    
# #######--------------------#######
# #######--------------------#######

# if chosen_tab == HOME:
#     home_page()
    
    

# if chosen_tab == CONTACT:
#     st.markdown("<h2 style='text-align: center; color: black;'>Contact Us</h1>", unsafe_allow_html=True)  
    
#     a, b = st.columns([0.8, 1.5])
#     a.image('https://images.squarespace-cdn.com/content/v1/60a2b00345921d78f1476b6f/0836bfa9-1dd9-4b79-b604-b411c63c7f9a/TheAssembly_TriggsPhotography_Wexford_Exterior-1.jpg')
#     a.markdown("""<span style="font-size:20px;">University of Pittsburgh, UPMC Hillman Cancer Center, Assembly Building</span>""", unsafe_allow_html=True)

#     b.markdown("""<div style="width: 100%"><iframe width="100%" height="700" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?width=100%25&amp;height=600&amp;hl=en&amp;q=5051%20Centre%20Avenue%20Pittsburgh,%20PA%2015213+(My%20Business%20Name)&amp;t=p&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed"><a href="https://www.maps.ie/distance-area-calculator.html">measure distance on map</a></iframe></div>""", unsafe_allow_html=True)
#     # b.write('Hillman Cancer Center, 5051 Centre Avenue Pittsburgh, PA 15213') 
    
#     a.markdown('##### If you have any questions or feedback, please feel free to contact us:')
#     a.markdown("""<span style="font-size:18px;">Hatice Osmanbeyoglu<br>Principal Investigator<br>✉️ osmanbeyogluhu@pitt.edu</span>""", unsafe_allow_html=True)
#     a.markdown("""<span style="font-size:18px;">Koushul Ramjattun<br>Graduate Researcher<br>✉️ kor11@pitt.edu</span>""", unsafe_allow_html=True)
#     a.markdown("""<span style="font-size:18px;">Xiaojun Ma<br>Senior Software Engineer<br>✉️ xim33@pitt.edu</span>""", unsafe_allow_html=True)
    
    
    
        
# elif chosen_tab == DATASET:
#     dataset_page(ds, datacore)
    
# elif chosen_tab == TF:
#     tf_page(datacore)
    
# elif chosen_tab == PROTEINS:
#     protein_page(datacore)
        
# elif chosen_tab == VIRAL_ENTRY:
#     viral_entry_page(datacore)
        
# elif chosen_tab == MULTI:
#     multi_dataset_page(datacore)
          
# elif chosen_tab == DOC:
#     doc_page()
    
# elif chosen_tab == STATS:
#     stats_page()

# for i in range(6):
#     st.markdown('#')
# st.markdown(footer,unsafe_allow_html=True)
        
# # st.markdown(icons, unsafe_allow_html=True)
