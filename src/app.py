import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy


# Add title and header
st.title("Swiss Renewable Energy")
st.header("Beta version feel free to write me an opinion ") #Information abailable about all renewable production in Switzerland by Canton

@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

renew_df_raw = load_data(path="./data/renewable_power_plants_CH.csv")
mpg_df = deepcopy(renew_df_raw)


# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("See our information source"):
    st.subheader("Renewable sources:")
    st.dataframe(data=mpg_df)
    # st.table(data=mpg_df)

left_column, middle_column, right_column = st.columns([3, 1, 1]) # This means that I want 3 columns and the first one will be 3 times wider than the rest

st.subheader("Plotly Map")





df = pd.read_csv("./data/renewable_power_plants_CH.csv")
with open('./data/georef-switzerland-kanton.geojson') as response:
    counties = json.load(response)
cantons_dict = {'TG':'Thurgau', 'GR':'Graubünden', 'LU':'Luzern', 'BE':'Bern', 'VS':'Valais',
                'BL':'Basel-Landschaft', 'SO':'Solothurn', 'VD':'Vaud', 'SH':'Schaffhausen', 'ZH':'Zürich',
                'AG':'Aargau', 'UR':'Uri', 'NE':'Neuchâtel', 'TI':'Ticino', 'SG':'St. Gallen', 'GE':'Genève',
                'GL':'Glarus', 'JU':'Jura', 'ZG':'Zug', 'OW':'Obwalden', 'FR':'Fribourg', 'SZ':'Schwyz',
                'AR':'Appenzell Ausserrhoden', 'AI':'Appenzell Innerrhoden', 'NW':'Nidwalden', 'BS':'Basel-Stadt'}
df = df.replace({"canton": cantons_dict})
df_2 = df.groupby(by=['energy_source_level_2','canton'])['production'].sum().reset_index()
df_2[df_2['canton'] == 'Vaud']['production'].max()
df_2['source_more_produced'] = '0'
cant = list(df_2['canton'].unique())
for i in cant:
    df_2['source_more_produced'].loc[df_2.index[df_2['canton'] == f'{i}'].tolist()] = df_2[df_2['production'] == df_2[df_2['canton'] == f'{i}']['production'].max()]['energy_source_level_2'].values[0]
plotly_map = px.choropleth_mapbox(df_2,
                           geojson=counties,
                           locations='canton',
                           color='source_more_produced',
                           featureidkey='properties.kan_name' ,
                           mapbox_style="carto-positron",
                           zoom=5.8,
                           center = {"lat": 46.798333, "lon": 8.231944}, #Using info about Centroid in Switzerland
                           opacity=0.5,
                           title='The highest Installed Power of Renewable Energy',
                           labels={'source_more_produced': 'The most produced source of energy'},
                            )
st.plotly_chart(plotly_map)