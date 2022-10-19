import re
import uuid

import streamlit as st
from PIL import Image


def home_page():
    left_col, right_col = st.columns(2)
    img = Image.open('./assets/logos/overview.png')

    right_col.image(img, output_format="SVG")        
    left_col.markdown("")
    # tt = """Reference:
    # X. Ma, A. Somasundaram, Z. Qi, D. Hartman, H. Singh, and H. Osmanbeyoglu, 'SPaRTAN, a computational framework for linking cell-surface receptors to transcriptional regulators'"""
    tt = ''
    left_col.markdown(f'<p style="color:#B2BEB5;font-size:20px;">{f"{tt}”"}</p>', unsafe_allow_html=True)
