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
        html.Img(src=r"assets/Logo.png", style = {"height": "16vh", 'margin-left': '4vw', 'margin-top': '-0.5vw', 'display': 'inline-block', 'margin-right': '10vw'}), # >---- Position Headline geändert und Größe Logo
        html.H1("Weltmeisterschaften im Damenfussball", style = {'text-align': 'left', 'margin-left': '-1.5vw', 'font-weight': 'bold', 'font-size': '45pt', 'color': 'white', 'display': 'inline-block '}), #---> Schriftgröße Headline geändert
        
    ], style={"padding": "1vw", "margin": "1vw", "background-color": "orange","height": "10vh"}), #das ist der orangene Balken

     html.Div([
        html.H1("von 1991 bis 2019", style = {'text-align': 'left', 'margin-top': '-1vw', 'margin-left': '21vw', 'font-weight': 'bold', 'font-size': '30pt', 'color': 'orange'}),
    ],), #----> neues Div für Subheadline eingefügt

    html.Div([

        html.Div([
            html.H5("Wähle Kontinente aus, die Du vergleichen möchtest", style = {'text-align': 'left', 'color': 'white'}), # ---> Rechtschreibung korrigiert und Fond Farbe an Header angepasst.

            dcc.Checklist(id='conti',
                options=[{'label':x , 'value':x} for x in all],
                value=all,
                labelStyle={'display': 'block'},
                style={"padding-left":"15%", "padding-top":"10%", "padding-bottom": "10%"}
                ),

            html.H5("Gespielte Matches pro Turnier", style = {'text-align': 'left', 'color': 'white'}), #---> Rechtschreibung korrigiert und Fond Farbe an Header angepasst.
            
            dcc.RangeSlider(id='matches_played', min=3, max=8, value=[3,8], step=1,)
            
        ], style={"width": "16vw", "height": "78vh", 'margin-top': '2vw', "padding": "1vw", "background-color": "orange"} ), # ---> grauer Balken geändert in orange und Breite um 1 vergrößert, damit Logo drüber genau in der Mitte ist. Abstand zum oberen Balken vergrößert.

        html.Div([
            dcc.Graph(id='goals', figure={}, style={'display': 'inline-block', 'width': '37vw', 'height': '40vh'}),

            dcc.Graph(id='ages', figure={}, style={'display': 'inline-block', 'width': '37vw', 'height': '40vh'}),

            dcc.Graph(id='penalty', figure={}, style={'display': 'inline-block', 'width': '37vw', 'height': '40vh'}),

            dcc.Graph(id='match', figure={}, style={'display': 'inline-block', 'width': '37vw', 'height': '40vh'})

        ], style={"margin-left": "18vw", 'margin-top': '-1vw', "transform": "translateY(-78vh)"}), #----> Höhe der Graphen an die Schrifthöhe im linken Balken angepasst.
        
    ],
    style={"margin-left": "1vw", "margin-top": "1vh", "margin-right": "5vw"}),

])

@app.callback(
      [Output(component_id='goals', component_property='figure'),
      Output(component_id='ages', component_property='figure'),
      Output(component_id='penalty', component_property='figure'),
      Output(component_id='match', component_property='figure')
      ],
      [Input(component_id='conti', component_property='value'),
      Input(component_id='matches_played', component_property='value')]
)

def update_graph(option_slctd, option_slctd2):
    dff = df.copy()
    if option_slctd == ['all']:
        dff = dff
    else:
        dff = dff[dff.continent.isin(option_slctd)]
    dff = dff[(dff["matches_played"] <= option_slctd2[1]) & (dff["matches_played"] >= option_slctd2[0])]

# Plotly express
    fig_g = px.scatter(dff, x="min_playing_time", y="goals", color="continent",
                    labels={
                     "min_playing_time": "Gesamtspielzeit im Turnier in Minuten",
                     "goals": "Anzahl Tore",
                     "continent": "Kontinente"
                    },
                    size="age",
                    hover_data=['squad'], 
                    trendline="ols",
                    trendline_scope="overall",
                    title="Tore pro Spielzeit",
                    template="simple_white"
                    )
    
    fig_a = px.histogram(dff, x="age",
                    labels={
                        "age": "Durchschnittsalter"
                    },
                    title="Durchschnittsalter der ausgewählten Mannschaften", template="simple_white"
                    ).update_layout(yaxis_title="Anzahl Mannschaften")

    fig_c = px.bar(dff, x='squad', y='penalty_kicks_attempted',
                    labels={
                        "squad": "Mannschaft",
                        "penalty_kicks_attempted": "Elfmeterschüsse",
                        "continent": "Kontinente"
                    },
                    title="Elfmeterschüsse",
                    color="continent",
                    template="simple_white"
                    )
    
    fig_m = px.line(dff, x="year", y="min_playing_time", color='squad',
                    labels={"squad": "Mannschaft",
                        "min_playing_time": "Gesamtspielzeit im Turnier in Minuten",
                        "year": "Jahre"
                    },
                    title="Spiele pro Team",
                    template="simple_white"
                    )

    return fig_g, fig_a, fig_c, fig_m

if __name__ == '__main__':
               app.run_server(debug=True)
