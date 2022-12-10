import pandas as pd
import plotly.express as px

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash (__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv(r'womens-world-cup.csv')


app.layout = html.Div([

    html.Div([
        html.H1("Frauen-Fussball-WMs der Jahre 1991 bis 2019", style = {'text-align': 'left'}),
    ], style={"padding": "1vw", "background-color": "green",}),

    html.Div([

        html.H4("Wählen Sie ein Jahr aus", style = {'text-align': 'left'}),

        dcc.Dropdown(id='year',
                        options = [
                            {"label": "1991", "value": 1991},
                            {"label": "1995", "value": 1995},
                            {"label": "1999", "value": 1999},
                            {"label": "2003", "value": 2003},
                            {"label": "2007", "value": 2007},
                            {"label": "2011", "value": 2011},
                            {"label": "2015", "value": 2015},
                            {"label": "2019", "value": 2019}],
                        multi = False,
                        value=1991,
                        style = {"width": "40%"}),

        dcc.Graph(id='goals', figure={}, style={'display': 'inline-block', 'width': '40vw'}),

        dcc.Graph(id='ages', figure={}, style={'display': 'inline-block', 'width': '40vw'}),

        dcc.Graph(id='penalty', figure={}, style={"width": "80vw"})
    ],
    style={"margin-left": "10vw", "margin-top": "5vh", "margin-right": "5vw", "margin-bottom": "5vh"})
])

@app.callback(
      [Output(component_id='goals', component_property='figure'),
      Output(component_id='ages', component_property='figure'),
      Output(component_id='penalty', component_property='figure')],
      [Input(component_id='year', component_property='value'),]
)

def update_graph(option_slctd):
    dff = df.copy()
    dff = dff[dff["year"] == option_slctd]

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


    return fig_g, fig_a, fig_c

if __name__ == '__main__':
               app.run_server(debug=True)
