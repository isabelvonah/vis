import pandas as pd
import plotly.express as px

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash (__name__)

df = pd.read_csv(r'womens-world-cup.csv')

app.layout = html.Div([

    html.H1("Womens world cup", style = {'text-align': 'center'}),
    html.H4("Numbers and facts womens world cup", style = {'text-align': 'left'}),

    dcc.Dropdown(id='squad',
                    options = [
                        {"label": "Argentinia", "value": 'Argentinia'},
                        {"label": "Germany", "value": 'Germany'},
                        {"label": "France", "value": 'France'},
                        {"label": "Austria", "value": 'Austria'},
                        {"label": "Slovenia", "value": 'Slovenia'},
                        {"label": "Netherlands", "value": 'Netherlands'},
                        {"label": "Nigeria", "value": 'Nigeria'},
                        {"label": "Switzerland", "value": 'Switzerland'}],
                    multi = False,
                    value='Germany',
                    style = {"width": "40%"}),

    dcc.Graph(id='ageplot', figure = {}),

    html.Br(),

    dcc.Graph(id='playplot', figure = {})
])

@app.callback(
      [Output(component_id='ageplot', component_property='figure'),
       Output(component_id='playplot', component_property='figure')],
      [Input(component_id='squad', component_property='value')]
)

def update_graph(option_slctd):
    dff = df.copy()
    dff = dff[dff["squad"] == option_slctd]

# Plotly express
    fig = px.line(dff, x='year', y='age')
    fig2 = px.scatter(dff, x="year", y="goals", 
                                    size="matches_played", color="non_penalty_goals", 
                                    hover_data=['squad'], trendline="ols")


    return fig, fig2

if __name__ == '__main__':
               app.run_server(debug=True)
