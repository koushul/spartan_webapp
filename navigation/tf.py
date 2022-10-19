import extra_streamlit_components as stx
import streamlit as st

from utils.components import make_tab


def tf_search():
    tabs = ['TF Activities', 'Tf-Protein Correlation', 'Litterature References', 'Download']
    chosen_tab = stx.tab_bar(data=[make_tab(t) for t in tabs], default=tabs[0]) 

def download_button(desc, data, label='Download', format='text/csv'):
    left_col, right_col = st.columns(2)
    right_col.download_button(
        label="Download",
        data=data,
        file_name='projD.csv',
        mime='text/csv',
    )
        
    left_col.write(desc)