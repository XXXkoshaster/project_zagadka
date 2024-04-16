import dash
import json
from dash import html 
import dash_bootstrap_components as dbc

with open("data.json") as f:
    data = json.load(f)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
dbc.Row([
    dbc.Col('Column 1', width=2),
    dbc.Col('Column 2', width=5),
    dbc.Col('Column 3', width=4),
])
app.layout = html.Div([
    html.H1(children="PROJECT ZAGADKA",
        style={"color": "blue",
               "fontSize": "40px"}),
    html.H2("VK scraper"),
    html.P("Data user:", style={"fontSize": "24px"}),
    html.Ul([
        html.Li(f"ID of user: {data['id']}"),
        html.Li(f"Birthday date of user: {data['bdate']}"),
        html.Li(f"City of user: {data['city']['title']}"),
        html.Li(f"Country of user: {data['country']['title']}"),
        html.Li(f"First name of user: {data['first_name']}"),
        html.Li(f"Last name of user: {data['last_name']}"),
        html.Li(f"Accaunt of user is closed: {data['is_closed']}"),
        html.Li([
            "URL of account: ",
            html.A(data["URL"], href=data["URL"])
        ])
    ], style={"fontSize": "20px"})
])

if __name__ == "__main__":
    app.run_server(debug=True)
