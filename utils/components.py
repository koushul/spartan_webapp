import re
import uuid

import extra_streamlit_components as stx
import streamlit as st
from navigation.protein import generate_color, get_ppi_edge_list
from pyvis.network import Network
import streamlit.components.v1 as components


def create_st_button(link_text, link_url, hover_color="#e78ac3", st_col=None):    
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


def make_tab(name, desc=''):
    return stx.TabBarItemData(id=name, title=name, description=desc)


def ppi(option):
    st.subheader(f'Protein-Protein Interactions for {option}')
    left_col, right_col = st.columns(2)
    size = left_col.slider('Interactors', 2, 100, 10)
    neighbors = right_col.slider('Neighbors', 1, 10, 3)

    net = Network()
    caption, pairs = get_ppi_edge_list(option, neighbors, size)
    # st.caption(caption.preferredName.values[0])
    # st.caption(caption.annotation.values[0])

    for i, j, v in pairs:
        net.add_node(j, label=j, color=generate_color())
        
    # for n in net.nodes:
    #     if n['label'] == caption.preferredName.values[0]:
    #         n['color'] = 'red'
            
        
        
    for pair in pairs:
        net.add_edge(pair[0], pair[1], value=pair[2]/10)
    
    # net.show_buttons(filter_=['physics'])


    net.show('test.html')
    HtmlFile = open("test.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height = 700, width=1000)
    
    st.download_button(
        label='Download Graph',
        data=source_code,
        file_name = 'ppi.html'
    )