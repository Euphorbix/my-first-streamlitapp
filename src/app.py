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
st.header("Beta version") #Information abailable about all renewable production in Switzerland by Canton

def main():
    menu = ['Home','Renewable Data', 'Choropleth Visualizations', "About"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice == 'Home':
        st.subheader("Renewable Energies in Switzerland")
        left_column, right_column = st.columns(2)
        with left_column:
            st.image(
                "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Saul%C4%97s_elektrin%C4%97.jpg/1280px-Saul%C4%97s_elektrin%C4%97.jpg")

        with right_column:
            st.image(
                "http://www.horizonte-magazin.ch/wp-content/uploads/2020/02/ho-124-reformstau-bei-der-wasserkraft-1170x780-1.jpg")

        middle_left_column, middle_right_column = st.columns(2)
        with middle_left_column:
            st.image(
                "https://www.gurit.com/-/media/gurit/images/key-visuals/carousel01wind2x/web_wind-energy.jpg?h=400&la=en&mh=468&mw=1382&w=1180&hash=C7281F03643051870E0BEC754C6C0185456D7A86")
        with middle_right_column:
            st.image(
                "https://www.fhnw.ch/en/about-fhnw/schools/school-of-engineering/institutes/institute-of-bioenergy-and-resource-efficiency/media/topbild-ibre.jpg/@@images/image/f_fullwidthtop")
    elif choice == 'Renewable Data':
        st.subheader("Data Frame")
        @st.cache
        def load_data(path):
            df = pd.read_csv(path)
            return df
        renew_df_raw = load_data(path="./data/renewable_power_plants_CH.csv")
        mpg_df = deepcopy(renew_df_raw)
        # Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
        st.subheader("Renewable power plants in Switzerland:")
        st.dataframe(data=mpg_df)
            # st.table(data=mpg_df)
    elif choice == 'Choropleth Visualizations':
        st.subheader("Choropleth Visualizations")
        df = pd.read_csv("./data/renewable_power_plants_CH.csv")

        with open('./data/georef-switzerland-kanton.geojson') as response:
            counties = json.load(response)
        cantons_dict = {'TG': 'Thurgau', 'GR': 'Graubünden', 'LU': 'Luzern', 'BE': 'Bern', 'VS': 'Valais',
                        'BL': 'Basel-Landschaft', 'SO': 'Solothurn', 'VD': 'Vaud', 'SH': 'Schaffhausen', 'ZH': 'Zürich',
                        'AG': 'Aargau', 'UR': 'Uri', 'NE': 'Neuchâtel', 'TI': 'Ticino', 'SG': 'St. Gallen',
                        'GE': 'Genève',
                        'GL': 'Glarus', 'JU': 'Jura', 'ZG': 'Zug', 'OW': 'Obwalden', 'FR': 'Fribourg', 'SZ': 'Schwyz',
                        'AR': 'Appenzell Ausserrhoden', 'AI': 'Appenzell Innerrhoden', 'NW': 'Nidwalden',
                        'BS': 'Basel-Stadt'}
        df = df.replace({"canton": cantons_dict})
        df_2 = df.groupby(by=['energy_source_level_2', 'canton'])['production'].sum().reset_index()
        df_2[df_2['canton'] == 'Vaud']['production'].max()
        df_2['source_more_produced'] = '0'
        cant = list(df_2['canton'].unique())

        for i in cant:
            df_2['source_more_produced'].loc[df_2.index[df_2['canton'] == f'{i}'].tolist()] = \
            df_2[df_2['production'] == df_2[df_2['canton'] == f'{i}']['production'].max()][
                'energy_source_level_2'].values[0]
        plotly_map = px.choropleth_mapbox(df_2,
                                          geojson=counties,
                                          locations='canton',
                                          color='source_more_produced',
                                          featureidkey='properties.kan_name',
                                          mapbox_style="carto-positron",
                                          zoom=6.1,
                                          center={"lat": 46.798333, "lon": 8.231944},
                                          # Using info about Centroid in Switzerland
                                          opacity=0.5,
                                          title='The highest Installed Power of Renewable Energy',
                                          labels={'source_more_produced': 'Most Produced\nEnergy Sources'},
                                          )
        plotly_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        df_new = df[
            ['electrical_capacity', 'energy_source_level_2', 'energy_source_level_3', 'canton', 'production', 'address',
             'municipality_code']]
        df_new_grouped = df_new.groupby(['canton', 'energy_source_level_2']).production.sum().reset_index()
        df_production = df_new_grouped.groupby('canton').production.sum().reset_index()
        plotly_map_2 = px.choropleth_mapbox(df_production, geojson=counties,
                                            locations='canton',
                                            color='production',
                                            featureidkey='properties.kan_name',
                                            mapbox_style="carto-positron",
                                            zoom=6.4,
                                            center={"lat": 46.798333, "lon": 8.231944},
                                            # Using info about Centroid in Switzerland
                                            opacity=0.5,
                                            color_continuous_scale="YlGn",
                                            labels={'production': 'Production [KW]'},
                                            )
        plotly_map_2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.subheader("Dominant Renewable Source")
        st.plotly_chart(plotly_map)
        st.subheader("Green production [KW] in each Canton")
        st.plotly_chart(plotly_map_2)
    else:
        st.date_input('Last update: ')
        st.success(f"SIT Academy mini-project.")

if __name__ == '__main__':
    main()





