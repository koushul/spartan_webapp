import streamlit as st

from texts.descriptions import Desc
from .home import TITLE

def doc_page():
    st.sidebar.header('Content')
    page = st.sidebar.radio('', ['Introduction', 'Usage', 'Database Implementation', 'FAQ'])
    st.header(page)
    if page == 'Introduction':
        st.header('SPaRTAN')
        st.write(Desc.spartan)
        
        with st.expander("Model Overview"):
            st.write(Desc.spartan_model)
            st.image('./assets/images/SPaRTAN_fig.png')
        
        with st.expander("Data Collection and Processing", expanded=True):
            st.image('./assets/images/documentation.png')
            
        with st.expander(f"Functions of {TITLE}"):
            st.write("")
            
    elif page == 'Usage':
        st.caption(f'Example usage of the {TITLE}')
        video_file = open('./assets/video/video.webm', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
        
    
    elif page == 'Database Implementation':
        st.caption(f'Detailed implementation of the {TITLE}')
    
        