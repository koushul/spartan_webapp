import streamlit as st
from PIL import Image

from texts.descriptions import Desc

@st.experimental_singleton
def load_overview_image():
    return Image.open('./assets/images/home.png')


def home_page():
    # Creating a title for the page.
    st.title('Welcome to SPaRTAN COVID-19db') ## Title
    st.write(Desc.home)
    img = load_overview_image()
    st.image(img, output_format="png")        
    
    