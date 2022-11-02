import streamlit as st

def doc_page():
    st.sidebar.header('Content')
    page = st.sidebar.radio('', ['Introduction', 'Usage', 'FAQ'])
    st.header(page)
    if page == 'Introduction':
        tab1, tab2 = st.tabs(["Data collection and processing", "Functions of SPaRTAN COVID-19db"])
        with tab1:
            st.subheader("Data collection and processing")    
            st.image('./assets/images/documentation.png')
            
        with tab2:
            st.subheader("Functions of SPaRTAN COVID-19db")
            
    if page == 'Usage':
        tab1, tab2 = st.tabs(["Starting from TF", "Starting from surface protein"])
    