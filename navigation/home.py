import streamlit as st
from PIL import Image

from texts.descriptions import Desc

# def home_page():
#     images, cell_images = load_and_encode_images()
#     left_col, right_col = st.columns(2)
#     img = Image.open('./assets/logos/overview_light.png')

#     left_col.image(img, output_format="SVG")        
#     tt = """Reference:
#     X. Ma, A. Somasundaram, Z. Qi, D. Hartman, H. Singh, and H. Osmanbeyoglu, 'SPaRTAN, a computational framework for linking cell-surface receptors to transcriptional regulators'"""
#     left_col.markdown(f'<p style="color:#B2BEB5;font-size:17px;">{f"{tt}”"}</p>', unsafe_allow_html=True)

    
#     with right_col:
#         st.caption('Click to select cell type.')
#         clicked = clickable_images(
#             images,
#             titles=[],
#             div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
#             img_style={"margin": "8px", "height": "150px"},
#         )
        
#         cell_type = [i.name[:-4] for i in cell_images][clicked]
        
#     right_col.subheader(cell_type)
#     right_col.markdown(f"{cell_desc[cell_type]}")
    
#     st.write("[Github](https://github.com/Koushul/spartan_webapp)")


def home_page():
    # Creating a title for the page.
    st.title('Welcome to SPaRTAN COVID-19db') ## Title
    st.write(Desc.home)
    img = Image.open('./assets/images/home.png')
    st.image(img, output_format="SVG")        
    
    