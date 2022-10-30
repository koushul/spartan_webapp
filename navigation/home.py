import streamlit as st
from PIL import Image

from texts.descriptions import Desc

img = Image.open('./assets/images/home.png')


def home_page():
    st.title('Welcome to SPaRTAN COVID-19db') 
    st.write(Desc.home)
    st.image(img)        
    st.write(Desc.intro)
    
    
    