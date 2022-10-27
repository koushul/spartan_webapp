import streamlit as st
from PIL import Image

from texts.descriptions import Desc

@st.experimental_singleton
def load_overview_image():
    return Image.open('./assets/images/home.png')


def home_page():
    img = load_overview_image()
    st.title('Welcome to SPaRTAN COVID-19db') 
    st.write(Desc.home)
    st.image(img, output_format="png")        
    
    