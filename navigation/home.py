import streamlit as st
from PIL import Image
import datetime

@st.cache(allow_output_mutation=True)
def load_home_image():
    return Image.open('./assets/images/home.png').resize((1000, 650))


def home_page():
    from texts.descriptions import Desc
    st.title('Welcome to SPaRTAN COVID-19db') 
    with open('./clock.time', 'r') as f:
        last_updated_on = f.readlines()[0]
    st.caption(last_updated_on)
    img = load_home_image()
    st.write(Desc.home)
    _, c, _ = st.columns([1, 6, 1])
    c.image(img)      
    st.markdown("<style>.element-container{opacity:1 !important}</style>", unsafe_allow_html=True)  
    st.write(Desc.intro)
    
    
if __name__ == '__main__':
    t = datetime.datetime.now()
    with open('./clock.time', 'w') as f:
        f.write(f'Last updated at {t.time():%H:%M} on {t.date():%Y-%m-%d}\n')
        print(f'Last updated at {t.time():%H:%M} on {t.date():%Y-%m-%d}\n')
    
    
    