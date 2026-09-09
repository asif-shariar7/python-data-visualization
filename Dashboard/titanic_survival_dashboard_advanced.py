import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

df = pd.read_csv("titanic.csv")

app = Dash(__name__)


# survival rate by class
survival_rate = df.groupby('Pclass')['Survived'].mean().reset_index()
survival_rate['Survived'] = survival_rate['Survived']*100
fig1 = px.bar(survival_rate, x = 'Pclass', y = 'Survived', title = "Survival Rate by Class", labels = {'Survived': 'Survival Rate (%)', 'Pclass': 'Passenger Class'})

#Survived by sex
counts = df.groupby('Sex')['Survived'].sum().reset_index()
fig2 = px.bar(counts, x = "Sex", y = "Survived", title = "Number of Survived Passengers by Sex")

# Survival rate by class and sex
survival_class_sex = df.groupby(['Pclass', 'Sex'])['Survived'].mean().reset_index()
survival_class_sex['Survived'] *= 100
fig3 = px.bar(survival_class_sex, x = 'Pclass', y = 'Survived', color = 'Sex', barmode = 'group', title = "Survival Rate by Class and Sex", labels = {'Pclass': 'Passenger Class', 'Survived': 'Survival Rate (%)'})


# for survival pie
df['Outcome'] = df['Survived'].map({0: 'Did Not Survive', 1: 'Survived'})

app.layout = html.Div(
    style={
        'fontFamily': 'Arial',
        'backgroundColor': '#f5f6fa',
        'minHeight': '100vh',
        'padding': '30px'
    },
    children=[

        # Header
        html.Div(
            style={
                'textAlign': 'center',
                'marginBottom': '30px'
            },
            children=[
                html.H1(
                    'Titanic Survival Dashboard',
                    style={'marginBottom': '5px'}
                ),
                html.P(
                    'Analysis of passenger survival patterns',
                    style={'color': '#666'}
                )
            ]
        ),

        # Static Graphs
        html.Div(
            style={
                'display': 'grid',
                'gridTemplateColumns': '1fr 1fr',
                'gap': '20px'
            },
            children=[

                html.Div(
                    style={
                        'backgroundColor': 'white',
                        'padding': '10px',
                        'borderRadius': '10px'
                    },
                    children=[
                        dcc.Graph(figure=fig1)
                    ]
                ),

                html.Div(
                    style={
                        'backgroundColor': 'white',
                        'padding': '10px',
                        'borderRadius': '10px'
                    },
                    children=[
                        dcc.Graph(figure=fig2)
                    ]
                ),

                html.Div(
                    style={
                        'backgroundColor': 'white',
                        'padding': '10px',
                        'borderRadius': '10px',
                        'gridColumn': '1 / -1'
                    },
                    children=[
                        dcc.Graph(figure=fig3)
                    ]
                )
            ]
        ),

        # Dynamic Graph Section
        html.Div(
            style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'marginTop': '20px'
            },
            children=[

                html.H3('Explore Survival Outcome by Class'),

                dcc.Dropdown(
                    id='class-dropdown',
                    options=[
                        {'label': 'Class 1', 'value': 1},
                        {'label': 'Class 2', 'value': 2},
                        {'label': 'Class 3', 'value': 3}
                    ],
                    placeholder='Select Passenger Class',
                    clearable=True
                ),

                dcc.Graph(id='survival-pie')
            ]
        )
    ]
)

@app.callback(
    Output('survival-pie', 'figure'),
    Input('class-dropdown', 'value')
)
def update_pie(selected_class):
    if selected_class is None:
        return px.pie(title = "Select a class to see survival outcome")
    filtered = df[df['Pclass'] == selected_class]
    return px.pie(filtered, names = 'Outcome', title = f"Survival Outcome - Class {selected_class}")


if __name__ == "__main__":
    app.run(debug = True)
