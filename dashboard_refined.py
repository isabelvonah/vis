import pandas as pd
import plotly.express as px

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash (__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv(r'cup_continent.csv')

all = df.continent.unique()

options=[{'label':x , 'value':x} for x in all]
options.append({'label': 'Select All', 'value': "all"})

app.layout = html.Div([

    html.Div([
        html.H1("Weltmeisterschaften im Damenfussball", style = {'text-align': 'left', 'font-weight': 'bold', 'color': 'white', 'display': 'inline-block '}),
        html.Img(src=r"assets/Logo.png", style={"right": "2vw", "position": "absolute",})
    ], style={"padding": "1vw", "margin": "1vw", "background-color": "orange","height": "10vh"}),

    html.Div([

        html.Div([
            html.H5("Wähle Kontinente aus, die du vergleichen möchtest", style = {'text-align': 'left'}),

            dcc.Checklist(id='conti',
                options=[{'label':x , 'value':x} for x in all],
                value=all,
                labelStyle={'display': 'block'},
                style={"padding-left":"15%", "padding-top":"10%", "padding-bottom": "10%"}
                ),

            html.H5("Möchtest du sogar einzelne Länder untersuchen? Dann wähle diese aus", style = {'text-align': 'left'}),
            
            
        ], style={"width": "15vw", "height": "78vh", "padding": "1vw", "background-color": "lightgrey"} ),

        html.Div([
            dcc.Graph(id='goals', figure={}, style={'display': 'inline-block', 'width': '37vw', 'height': '40vh'}),

            dcc.Graph(id='ages', figure={}, style={'display': 'inline-block', 'width': '37vw', 'height': '40vh'}),

            dcc.Graph(id='penalty', figure={}, style={'display': 'inline-block', 'width': '37vw', 'height': '40vh'}),

            dcc.Graph(id='match', figure={}, style={'display': 'inline-block', 'width': '37vw', 'height': '40vh'})

        ], style={"margin-left": "18vw", "transform": "translateY(-78vh)"}),
        
    ],
    style={"margin-left": "1vw", "margin-top": "1vh", "margin-right": "5vw"}),

])

@app.callback(
      [Output(component_id='goals', component_property='figure'),
      Output(component_id='ages', component_property='figure'),
      Output(component_id='penalty', component_property='figure'),
      Output(component_id='match', component_property='figure')
      ],
      [Input(component_id='conti', component_property='value')]
)

def update_graph(option_slctd):
    dff = df.copy()
    if option_slctd == ['all']:
        dff = df
    else:
        dff = df[df.continent.isin(option_slctd)]

# Plotly express
    fig_g = px.scatter(dff, x="min_playing_time", y="goals", 
                    size="age", 
                    color="continent", 
                    hover_data=['squad'], 
                    trendline="ols",
                    trendline_scope="overall",
                    labels={
                        "min_playing_time": "time played",
                        "goals": "goals",},
                    title="Tore pro Spielzeit",
                    template="simple_white"
                    )
    
    fig_a = px.histogram(dff, x="age", title="Alter der Mannschaften", template="simple_white")

    fig_c = px.bar(dff, x='squad', y='penalty_kicks_attempted',
                    labels={
                        "squad": "team",
                        "penalty_kicks_attempted": "penaltys",},
                    title="Elfmeterschüsse",
                    color="continent",
                    template="simple_white"
                    )
    
    fig_m = px.line(dff, x="year", y="min_playing_time", color='squad',
                    labels={"squad": "team",
                        "matches_played": "Anzahl Spiele"},
                    title="Spiele pro Team",
                    template="simple_white")

    return fig_g, fig_a, fig_c, fig_m

if __name__ == '__main__':
               app.run_server(debug=True)
