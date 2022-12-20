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

all_y = df.year.unique()

options_y=[{'label':x , 'value':x} for x in all_y]
options_y.append({'label': 'Select All', 'value': "all_y"})

app.layout = html.Div([

    html.Div([
        html.H1("Weltmeisterschaften im Damenfussball", style = {'text-align': 'left', 'font-weight': 'bold', 'color': 'white', 'display': 'inline-block '}),
        html.Img(src=r"assets/Logo.png", style={"right": "2vw", "position": "absolute",})
    ], style={"padding": "1vw", "margin": "1vw", "background-color": "orange","height": "10vh"}),

    html.Div([

        html.Div([
            html.H4("Wählen Sie ein Jahr aus", style = {'text-align': 'left'}),

            dcc.Dropdown(id='conti', 
                            options=[{'label':x , 'value':x} for x in all] + [{'label':'Select All' , 'value':'all'}] , 
                            value= 'Select All', 
                            multi=True, 
                            style = {"width": "100%"}),
            
            dcc.Dropdown(id='year', 
                            options=[{'label':x , 'value':x} for x in all_y] + [{'label':'Select All' , 'value':'all_y'}] , 
                            value= 'Select All', 
                            multi=True, 
                            style = {"width": "100%"}),
            
            
        ], style={"width": "15vw"}),

    html.Div([
        dcc.Graph(id='goals', figure={}, style={'display': 'inline-block', 'width': '37vw', 'height': '40vh'}),

        dcc.Graph(id='ages', figure={}, style={'display': 'inline-block', 'width': '37vw', 'height': '40vh'}),

        dcc.Graph(id='match', figure={}, style={'display': 'inline-block', 'width': '37vw', 'height': '40vh'}),

        dcc.Graph(id='penalty', figure={}, style={'display': 'inline-block', 'width': '37vw', 'height': '40vh'})

    ], style={"margin-left": "18vw", "transform": "translateY(-100px)"}),
        
    ],
    style={"margin-left": "1vw", "margin-top": "5vh", "margin-right": "5vw"}),

])

@app.callback(
      [Output(component_id='goals', component_property='figure'),
      Output(component_id='ages', component_property='figure'),
      Output(component_id='match', component_property='figure'),
      Output(component_id='penalty', component_property='figure')],
      [Input(component_id='year', component_property='value'),
      Input(component_id='conti', component_property='value')]
)

def update_graph(option_slctd, option_slctd2):
    dff = df.copy()
    #dff = dff[dff["year"] == option_slctd]
    if option_slctd2 == ['all']:
        dff = df
    else:
        dff = df[df.continent.isin(option_slctd2)]
    if option_slctd == ['all_y']:
        dff = df
    else:
        dff = df[df.year.isin(option_slctd)]

# Plotly express
    fig_g = px.scatter(dff, x="min_playing_time", y="goals", 
                    size="age", 
                    color="squad", 
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
                    template="simple_white"
                    )
    
    fig_m = px.line(dff, x="year", y="matches_played", color='squad',
                    labels={"squad": "team",
                        "matches_played": "Anzahl Spiele"},
                    title="Spiele pro Team")

    return fig_g, fig_a, fig_c, fig_m

if __name__ == '__main__':
               app.run_server(debug=True)
