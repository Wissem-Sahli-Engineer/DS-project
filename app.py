import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Load data
df = pd.read_csv("gaming_laptops2_cleaned.csv")

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Gaming Laptops Dashboard", style={"textAlign": "center"}),

    dcc.Graph(
        figure=px.histogram(
            df,
            x="Price",
            nbins=20,
            title="Price Distribution"
        )
    )
])

if __name__ == "__main__":
    app.run(debug=True)
