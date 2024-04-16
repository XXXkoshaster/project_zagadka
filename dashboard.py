import dash
import json
from dash import html 

with open("data.jason") as f:
    data = json.load(f)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("PROJECT ZAGADKA",
        style={"color": "blue",
               "fontSize": "40px"}),
    html.H2("VK scraper"),
    html.P("Data user:"),
    html.Ul([
        html.Li(f"ID of user: {data['id']}"),
        html.Li(f"Birthday date of user: {data['date']}"),
        html.Li(f"City of user: {data['city']}"),
        html.Li(f"Country of user: {data['country']}"),
        html.Li(f"First name of user: {data['first_name']}"),
        html.Li(f"Last name of user: {data['last_name']}"),
        html.Li(f"Is accaunt of user closed: {data['is_closed']}"),
        html.Li([
            "User account ",
            html.A(data["URL"])
        ])
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
