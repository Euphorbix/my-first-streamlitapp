import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import pandas as pd
from urllib.request import urlopen
import json
from tabulate import tabulate

df = pd.read_csv("renewable_power_plants_CH.csv")

with open('georef-switzerland-kanton.geojson') as response:
    counties = json.load(response)

cantons_dict = {'TG':'Thurgau', 'GR':'Graubünden', 'LU':'Luzern', 'BE':'Bern', 'VS':'Valais',
                'BL':'Basel-Landschaft', 'SO':'Solothurn', 'VD':'Vaud', 'SH':'Schaffhausen', 'ZH':'Zürich',
                'AG':'Aargau', 'UR':'Uri', 'NE':'Neuchâtel', 'TI':'Ticino', 'SG':'St. Gallen', 'GE':'Genève',
                'GL':'Glarus', 'JU':'Jura', 'ZG':'Zug', 'OW':'Obwalden', 'FR':'Fribourg', 'SZ':'Schwyz',
                'AR':'Appenzell Ausserrhoden', 'AI':'Appenzell Innerrhoden', 'NW':'Nidwalden', 'BS':'Basel-Stadt'}

df = df.replace({"canton": cantons_dict})

print(tabulate(df.head(), headers='keys'))