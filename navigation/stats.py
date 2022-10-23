import pandas as pd
import streamlit as st


def stats_page():
    st.header('Daily users worldwide')
    cities = pd.read_table('https://gist.githubusercontent.com/weshi/03c92ae63ad5554baff487dfd866b0b5/raw/fd875dea90d3d3407d95e11bac19fc3b4d1f6bfc/worldcities.csv', sep=',')
    cities = cities[['Latitude', 'Longitude']]
    cities.columns = ['lat', 'lon']
    st.map(cities, zoom=2)