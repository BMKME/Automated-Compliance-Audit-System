# dash_app.py

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Create a simple DataFrame
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Grapes"],
    "Amount": [4, 1, 2, 5]
})

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=px.bar(df, x="Fruit", y="Amount", title="Fruit Amounts")
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
