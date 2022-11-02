import streamlit as st

from texts.descriptions import Desc

def doc_page():
    st.sidebar.header('Content')
    page = st.sidebar.radio('', ['Introduction', 'Usage', 'FAQ'])
    st.header(page)
    if page == 'Introduction':
        st.header('SPaRTAN')
        st.write(Desc.spartan)
        
        with st.expander("Model Overview"):
            st.write(Desc.spartan_model)
            st.image('./assets/images/SPaRTAN_fig.png')
        
        with st.expander("Data Collection and Processing", expanded=True):
            st.image('./assets/images/documentation.png')
            
        with st.expander("Functions of SPaRTAN COVID-19db"):
            st.write("")
            
    if page == 'Usage':
        tab1, tab2 = st.tabs(["Starting from TF", "Starting from surface protein"])
    