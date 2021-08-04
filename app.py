import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from urllib.request import urlopen
import json
import pandas as pd

#token = open("mapbox.mapbox_token").read() # you will need your own token

path = 'https://raw.githubusercontent.com/momijizen/covid19_world_vaccination/main/countries.geojson'
with urlopen(path) as response:
    geojson = json.load(response)

df_data = pd.read_csv('country_vaccinations.csv')
data_countries = df_data.sort_values('date').drop_duplicates('country',keep='last')

#df = px.data.election()
#geojson = px.data.election_geojson()
candidates = 'total_vaccinations'

app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1("COVID-19 World Vaccination Progress"),
    html.Div([
        html.Div(
            [
            html.H2('Choose options:', style={'margin-right': '2em'}),
            ]
        ),
        dcc.Dropdown(id='candidate',
                           options=[
                                     {'label': 'Total number of vaccinations', 'value': 'total_vaccinations'},
                                     {'label': 'Total number of people vaccinated', 'value': 'people_vaccinated'},
                                     {'label': 'Total number of people fully vaccinated', 'value': 'people_fully_vaccinated'}
                                    ],
                          placeholder='Select an option',
                          style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'})
    ], style={'display':'flex'}),
    dcc.Graph(id="choropleth"),
])


@app.callback(
    Output("choropleth", "figure"), 
    [Input("candidate", "value")])
def display_choropleth(candidate):
    fig = px.choropleth_mapbox(
        data_countries,
        geojson=geojson, 
        color=candidate,
        mapbox_style="carto-positron",
        color_continuous_scale="Viridis",
        locations="iso_code", featureidkey="properties.ISO_A3",
        center={"lat": 45.5517, "lon": -73.7073}, zoom=1,
        range_color=[0, data_countries[candidate].max()])
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        #mapbox_accesstoken=token
    )

    return fig


if __name__ == "__main__":
    app.run_server()
