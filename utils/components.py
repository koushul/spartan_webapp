import re
import uuid
import numpy as np

import extra_streamlit_components as stx
import streamlit as st
from navigation.protein import get_ppi_edge_list
from pyvis.network import Network
import streamlit.components.v1 as components
from matplotlib import colors


hide_streamlit_style = f"""
    <style>
        MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        footer:after {{
            content:'Created by Koushul using Streamlit and BioRender'; 
            visibility: visible;
            display: block;
            position: relative;
            #background-color: red;
            padding: 5px;
            top: 2px;
        }}
    </style>
"""

import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image


def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, color='black', fontsize=15,
            ha="left", va="center", transform=ax.transAxes)
    
sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0), 'axes.linewidth':2})

palette_mapper = {
    'healthy': colors.to_hex('green'),
    'mild': colors.to_hex('salmon'),
    'moderate': colors.to_hex('lightskyblue'),
    'critical': colors.to_hex('orchid'),
    'severe': colors.to_hex('magenta'),
    'stable': colors.to_hex('orange'),
    'progressive': colors.to_hex('blueviolet'),
}

def make_palette(column, groups):
    return [colors.to_rgb(column.color_picker(g, palette_mapper.get(g.lower(), colors.to_hex('black')))) for g in groups]    


def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

def ridge_plot(df_plt, xlabel, column):
    groups = np.sort(np.unique(df_plt.patient_group.values))
    g = sns.FacetGrid(df_plt, 
        palette = make_palette(column=column, groups=groups),
        row="patient_group", hue="patient_group", aspect=5)
    
    g.map_dataframe(sns.kdeplot, x="Pair_correlations", fill=True, alpha=1)
    g.map_dataframe(sns.kdeplot, x="Pair_correlations", color='black')
    g.map(label, "patient_group")
    g.fig.subplots_adjust(hspace=-.5)
    g.set_titles("")
    g.set(yticks=[], xlabel=xlabel)
    g.despine( left=True)
    g.set(yticks=[], ylabel="")
    g.despine(bottom=True, left=True)
    # g.savefig('ridge.png', dpi=180)    
    plt.xlabel(xlabel, fontsize=25)
    img = fig2img(g.fig)
    
    return img

def create_st_button(link_text, link_url, hover_color="#4EC5F1", st_col=None):    
    button_uuid = uuid.uuid1()
    button_id = re.sub("\d+", "", str(button_uuid))
    
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
                border-color: rgb(13, 242, 201);
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


def make_tab(name, desc=''):
    return stx.TabBarItemData(id=name, title=name, description=desc)


def ppi(option):
    st.header(f'Protein-Protein Interactions for {option} from StringDB')
    st.caption('Threshold of significance to include an interaction: 400')
    st.caption('Learn more: https://string-db.org/help/api/')
    left_col, right_col = st.columns(2)
    size = left_col.slider('Interactors', 2, 100, 10)
    neighbors = right_col.slider('Neighbors', 1, 10, 3)

    net = Network()
    try:
        caption, pairs = get_ppi_edge_list(option, neighbors, size)
        for i, j, v in pairs:
            net.add_node(j, label=j)
            
        for n in net.nodes:
            if n['label'] == option:
                n['color'] = 'red'
                 
        for pair in pairs:
            net.add_edge(pair[0], pair[1], value=pair[2]/10)
    except:
        st.warning('No PPI Information available from stringdb')
        return
    # net.show_buttons(filter_=['physics'])

    net.show('./utils/ppi.html')
    HtmlFile = open("./utils/ppi.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height = 700, width=1000)
    
    # st.download_button(
    #     label='Download Graph',
    #     data=source_code,
    #     file_name = 'ppi.html'
    # )
    
def download_button(desc, data, left_col, right_col, label='Download as CSV'):
    right_col.download_button(
        label=label,
        data=data,
        file_name='projD.csv',
        mime='text/csv',
        key=uuid.uuid1()
    )
        
    left_col.write(desc)
    
    
def local_css(file_name='./assets/style.css'):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)