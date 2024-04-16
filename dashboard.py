import dash
import json
from dash import html 
import dash_bootstrap_components as dbc

class Data:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        with open(self.filepath) as f:
            return json.load(f)

class DashboardBuilder:
    def __init__(self, data):
        self.data = data

    def build_layout(self):
        return html.Div([
                html.H1(children="PROJECT ZAGADKA", style={"color": "blue", "fontSize": "40px"}),
                html.H2("VK scraper"),
                self.build_tabs()
        ], style={"fontSize": "20px"})
    
    def build_tabs(self):
        return dbc.Tabs([
            dbc.Tap(self.build_user_info(), label="Data user"),
            dbc.Tap(self.build_project_info(), label="Projecy info")
        ])
    
    def build_user_info(self):
        return html.Ul([
            html.Br(),
            html.Li(f"ID of user: {self.data['id']}"),
            html.Li(f"Birthday date of user: {self.data['bdate']}"),
            html.Li(f"City of user: {self.data['city']['title']}"),
            html.Li(f"Country of user: {self.data['country']['title']}"),
            html.Li(f"First name of user: {self.data['first_name']}"),
            html.Li(f"Last name of user: {self.data['last_name']}"),
            html.Li(f"Accaunt of user is closed: {self.data['is_closed']}"),
            html.Li(["URL of account: ", html.A(self.data["URL"], href=self.data["URL"])])
        ])
    
    def build_project_info(self):
        return html.Div([
            html.Br(),
            html.P("Web server for analising data vk users."),
            html.P(["Git hub repo: ", html.A('https://github.com/XXXkoshaster/project_zagadka', href='https://github.com/XXXkoshaster/project_zagadka')])
        ])

class App:
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        data = Data("data.json")
        dashboard_builder = DashboardBuilder(data)
        



if __name__ == "__main__":
    app.run_server(debug=True)
