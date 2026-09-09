# Note : Here No user input controlling the output so no callback needed.

import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

df = pd.read_csv("titanic.csv")

app = Dash(__name__)


# survival rate by class
survival_rate = df.groupby('Pclass')['Survived'].mean().reset_index()
survival_rate['Survived'] = survival_rate['Survived']*100
fig1 = px.bar(survival_rate, x = 'Pclass', y = 'Survived', title = "Survival Rate by Class")

#Survived by sex
counts = df.groupby('Sex')['Survived'].sum().reset_index()
fig2 = px.bar(counts, x = "Sex", y = "Survived", title = "Survived Passengers by Sex")

# Survival rate by class and sex
survival_class_sex = df.groupby(['Pclass', 'Sex'])['Survived'].mean().reset_index()
survival_class_sex['Survived'] *= 100
fig3 = px.bar(survival_class_sex, x = 'Pclass', y = 'Survived', color = 'Sex', barmode = 'group', title = "Survival Rate by Class and Sex")

app.layout = html.Div([
    
    html.H1(
        "Titanic Survival Analysis Dashboard",
        style={
            "textAlign": "center",
            "marginBottom": "30px"
        }
    ),

    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3)
])


if __name__ == "__main__":
    app.run(debug = True)
