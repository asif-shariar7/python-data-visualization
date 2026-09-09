import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


df = pd.read_csv('smoothie_sales.csv', parse_dates = ['Date'])



app = Dash(__name__)

# No callback needed for this bar because it is static
total_sales = df.groupby("Smoothie", as_index = False)["Sales"].sum()
bar_fig = px.bar(total_sales, x = 'Smoothie', y = 'Sales', title = 'Total Sales by Smoothie')

app.layout = html.Div(
    style={
        'fontFamily': 'Arial',
        'backgroundColor': '#f4f6f8',
        'minHeight': '100vh',
        'padding': '30px'
    },
    children=[

        # Dashboard Header
        html.Div(
            style={
                'textAlign': 'center',
                'marginBottom': '30px'
            },
            children=[
                html.H1(
                    'Smoothie Sales Dashboard',
                    style={
                        'marginBottom': '8px',
                        'fontSize': '32px'
                    }
                ),

                html.P(
                    'Interactive analysis of smoothie sales over time',
                    style={
                        'fontSize': '16px',
                        'color': '#666'
                    }
                )
            ]
        ),

        # Filter Section
        html.Div(
            style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.08)'
            },
            children=[
                html.Label(
                    'Select Smoothie:',
                    style={
                        'fontWeight': 'bold',
                        'display': 'block',
                        'marginBottom': '8px'
                    }
                ),

                dcc.Dropdown(
                    id='csv-smoothie-filter',
                    options=[
                        {'label': smoothie, 'value': smoothie}
                        for smoothie in df['Smoothie'].unique()
                    ],
                    value=df['Smoothie'].unique()[0],
                    clearable=False
                )
            ]
        ),

        # Line Chart Card
        html.Div(
            style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.08)'
            },
            children=[
                dcc.Graph(
                    id='csv-sales-over-time'
                )
            ]
        ),

        # Bar Chart Card
        html.Div(
            style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.08)'
            },
            children=[
                dcc.Graph(
                    figure=bar_fig
                )
            ]
        )
    ]
)

@app.callback(
    Output('csv-sales-over-time', 'figure'),
    Input('csv-smoothie-filter', 'value')
)

def update_charts(selected_smoothie):
    filter_df = df[df['Smoothie'] == selected_smoothie]
    line_fig = px.line(filter_df, x = 'Date', y = 'Sales', title = f"{selected_smoothie} over time")

    return line_fig


if __name__ == "__main__":
    app.run(debug = True)