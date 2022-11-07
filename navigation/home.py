import streamlit as st
from PIL import Image
import datetime

@st.cache(allow_output_mutation=True)
def load_home_image():
    return Image.open('./assets/images/home_overview.png').resize((1000, 650))


def home_page():
    from texts.descriptions import Desc
    img = load_home_image()
    x, y, z = st.columns([1, 6, 1])
    
    with y:
        st.title('COVID-19db of Immune Cell States') 
        with open('./clock.time', 'r') as f:
            last_updated_on = f.readlines()[0]
        st.caption(last_updated_on)
        st.write(Desc.home)
        st.image(img)      
        st.write(Desc.intro_1)
        st.markdown(Desc.intro_2)
    
    
if __name__ == '__main__':
    t = datetime.datetime.now()
    with open('./clock.time', 'w') as f:
        f.write(f'Last updated at {t.time():%H:%M} on {t.date():%Y-%m-%d}\n')
        print(f'Last updated at {t.time():%H:%M} on {t.date():%Y-%m-%d}\n')
    
    
    