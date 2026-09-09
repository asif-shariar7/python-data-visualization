import pandas as pd
import plotly.express as px    
from dash import Dash, dcc, html, Input, Output


df = pd.read_csv("smoothie_sales.csv", parse_dates = ["Date"])

app = Dash(__name__)  

app.layout = html.Div([

    # Dashboard title
    html.H1(
        "Smoothie Sales Dashboard",
        style={
            "textAlign": "center",
            "marginBottom": "30px"
        }
    ),

    # Filter section
    html.Div([
        
        html.Label(
            "Select Smoothie:",
            style={
                "fontWeight": "bold",
                "fontSize": "16px"
            }
        ),

        dcc.Dropdown(
            id="csv-smoothie-filter",
            options=[
                {
                    "label": smoothie,
                    "value": smoothie
                }
                for smoothie in df["Smoothie"].unique()
            ],
            value=df["Smoothie"].unique()[0],
            clearable=False,
            style={
                "marginTop": "8px"
            }
        )

    ], style={
        "width": "80%",
        "margin": "auto",
        "marginBottom": "30px"
    }),

    # Main chart
    html.Div([
        
        dcc.Graph(
            id="csv-sales-over-time"
        )

    ], style={
        "width": "90%",
        "margin": "auto"
    })

])


@app.callback(
    Output('csv-sales-over-time', 'figure'),
    Input('csv-smoothie-filter', 'value')
)

def update_csv_time_series(selected_smoothie):
    filter_df = df[df["Smoothie"] == selected_smoothie]
    fig = px.line(filter_df, x = 'Date', y = 'Sales', title = f"{selected_smoothie} Sales Over Time") 

    return fig



if __name__ == '__main__':
    app.run(debug=True)