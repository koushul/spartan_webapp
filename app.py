from binascii import a2b_hex
from faulthandler import disable
import streamlit as st
from PIL import Image
import time
import pandas as pd
import re
import uuid
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

def create_st_button(link_text, link_url, hover_color="#e78ac3", st_col=None):

    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub("\d+", "", button_uuid)

    button_css = f"""
        <style>
            #{button_id} {{
                background-color: none;
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 2px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }}
            #{button_id}:hover {{
                border-color: {hover_color};
                color: {hover_color};
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: {hover_color};
                color: white;
                }}
        </style> """

    html_str = f'<a href="{link_url}" target="_blank" id="{button_id}";>{link_text}</a><br></br>'

    if st_col is None:
        st.markdown(button_css + html_str, unsafe_allow_html=True)
    else:
        st_col.markdown(button_css + html_str, unsafe_allow_html=True)

details = """\t Briefly, our model views the expression of surface proteins as a proxy of their activities; signaling emanating from these proteins converges on particular TFs, whose activities, in turn, regulate the expression of their target genes. \n\t Specifically, we use a regularized bilinear regression algorithm called affinity regression (AR), a general statistical framework for any problem where the observed data can be explained as interactions (W) between two kinds of inputs, to establish an interaction matrix between surface proteins (P) and TFs (D) that predicts target gene expression (Y).
\n\t Since the model captures statistical relationships between surface proteins, TFs, and gene expression. We can use the trained interaction matrix to obtain different views of a CITE-seq data set; e.g., to predict TF activity from a cell's surface protein expression profile or to predict surface protein expression from a cell’s gene expression profile. Intuitively, information flows down from observed surface protein levels through the learned interaction matrix to infer TF activities and observed mRNA expression levels or propagates up through the TF target-gene edges and interaction network to infer surface protein expression.
"""


st.title('Covid19-Database Demo ')

pages = st.tabs(["Home", "Dataset", "TF Search", "Protein Search", "Documentation", "Statistics"])



def home():
    left_col, right_col = st.columns(2)
    img = Image.open('./figure.png')


    right_col.image(img, output_format="PNG")
        
    # left_col.markdown("### Summary")
    left_col.markdown(
    "SPaRTAN (**S**ingle-cell **P**roteomic **a**nd **R**NA based **T**ranscription factor **A**ctivity **N**etwork)," 
    " is a tool for linking cell-surface receptors to transcription factors (TFs) by exploiting cellular indexing of transcriptomes and epitopes by sequencing (CITE-seq) datasets with cis-regulatory information.")

    # left_col.write("""**Reference:**
    # X. Ma, A. Somasundaram, Z. Qi, D. Hartman, H. Singh, and H. Osmanbeyoglu, 'SPaRTAN, a computational framework for linking cell-surface receptors to transcriptional regulators'""")
    create_st_button("Nucleic Acids Research: SPaRTAN", "https://academic.oup.com/nar/article/49/17/9633/6368058")

    tt = """Reference:
    X. Ma, A. Somasundaram, Z. Qi, D. Hartman, H. Singh, and H. Osmanbeyoglu, 'SPaRTAN, a computational framework for linking cell-surface receptors to transcriptional regulators'"""

    left_col.markdown(f'<p style="color:#B2BEB5;font-size:20px;">{f"{tt}”"}</p>', unsafe_allow_html=True)


    expander = st.expander("Detailed explanation")
    expander.write(details)
    expander.image("./SPaRTAN_fig.png")
    expander.write('Reference: https://github.com/osmanbeyoglulab/SPaRTAN/')
    
    st.subheader('Cell Types')
    st.image('./cells.png')
    

def tf():
    dff = pd.read_csv('/ihome/hosmanbeyoglu/kor11/tools/spartan_webapp/litcovid.export.all.tsv', sep='\t', header=None)
    dff.columns = ['pmid', 'title', 'journal']

    import random


    df = pd.read_csv('projD_ori.csv').set_index('Unnamed: 0')
    df.index.name = 'TF'
    df2 = pd.read_csv('P_1-1.csv').set_index('Unnamed: 0')
    df2.index.name='Cell'
    df3 = pd.read_excel('/ihome/hosmanbeyoglu/kor11/tools/spartan_webapp/CD16_Mono_projD_median_group_100_1500.xlsx', 
        engine='openpyxl').set_index('Unnamed: 0')
    df3.index.name = 'TF'
    df3.columns = ['Healthy', 'Mild', 'Moderate', 'Severe', 'pvalues']

    st.markdown("---")
    st.subheader('Analysis')

    tab1, tab2 = st.tabs(["Transcription Factors", "Surface Proteins"])
    with tab1:
        st.caption("Projected TF activities with Q TFs and M cells")
        st.dataframe(df.reset_index())
    
        
    with tab2:
        st.caption("Projected protein expression with S proteins and M cells")
        st.dataframe(df2.reset_index())
        
        
        
    st.markdown("---")
    option = st.multiselect(
        "Choose your favorite Transcription Factor(s)?",
        df.index, "IRF4")
    options = option
    with st.sidebar:
        st.header(f'LitCovid Publications Related to {option[0]}')

    for pmid, title, journal in dff.sample(random.randint(2, 6)).values:
        create_st_button(f'({journal}) {title}', f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/', st_col=st.sidebar)


    import seaborn as sns
    import matplotlib.pyplot as plt

    for o in options:
        fig = plt.figure(figsize=(12, 6), dpi=180)
        sns.kdeplot(data=df3.sample(100).drop('pvalues', 1), shade=True)
        plt.ylabel('TFs')
        plt.title(f'{o}')
        # st.write('You selected:', option)
        st.pyplot(fig)
  
import numpy as np
def data():
    tab1, tab2, tab3, tab4 = st.tabs(['Dataset 1', 'Dataset 2', 'Dataset 3', 'Dataset 4'])
    with tab1:
        st.info('Meta Statistics for Dataset 1')
    with tab2:
        st.info('Meta Statistics for Dataset 2')
    with tab3:
        st.info('Meta Statistics for Dataset 3')
    with tab4:
        st.info('Meta Statistics for Dataset 4')
    
        
if page == "Home Page":
    home()
    
if page == "TF Search":
    tf()
    
if page == "Documentation":
    a, b, c = st.columns(3)
    img1 = Image.open('./step1.png')
    img2 = Image.open('./step2.png')
    img3 = Image.open('./step3.png')
    
    a.image(img1, output_format="PNG")
    b.image(img2, output_format="PNG")
    c.image(img3, output_format="PNG")
    
    
    
if page == "Datasets":
    data()
    