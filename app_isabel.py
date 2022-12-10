import pandas as pd
import plotly.express as px

from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# External Stylsheet: siehe Foliensatz 7 --> S. 37

app = Dash(__name__)

df = pd.read_csv(r'womens-world-cup.csv')

app.layout = html.Div([
    html.H1("Frauen-Fussball-WMs der Jahre ...."),

    dcc.Graph(id="???"),
    dcc.Graph(id="????")
])

if __name__ == '__main__':
    app.run_server(debug=True)