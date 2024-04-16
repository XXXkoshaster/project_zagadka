import dash
from dash import dash_table, html, dcc, Output, Input, State
import json
import dash_bootstrap_components as dbc
import pandas as pd 
import subprocess
import sys


# класс создает интерфейс страницы
class DashboardBuilder:
    def __init__(self, filepath):
        self.filepath = filepath
        self.json = self.load_data()
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.data = pd.DataFrame(self.json)
        
    def load_data(self):
        with open(self.filepath) as f:
            return json.load(f)
    
    def build_layout(self):
        self.app.layout = html.Div([
                html.H1(children="PROJECT ZAGADKA", style={"color": "blue", "fontSize": "40px"}),
                
                html.H2("VK scraper"),
                
                html.Div([
                    dcc.Input(
                        type='text',
                        placeholder='Put your URL'
                    ), 
                    html.Button(
                        'Submit'
                    )
                ]),  

                dcc.Dropdown(
                    options=[
                        {'label': user, 'value': user} for user in ['Data user', 'Project info']
                    ],
                ),  
               
                html.Div(id='info_output'),

                html.Br(),

                dbc.Tabs([dbc.Tab(self.build_project_info(), label="Project info")])
        
        ], style={"fontSize": "20px"})
    
    def build_user_info(self):
        return html.Div([html.Br(),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in self.data.columns],
                data=self.data.to_dict('records'),
            )
        ])
    
    def build_project_info(self):
        return html.Div([
            html.Br(),
            html.P("Web server for analysing data vk users."),
            html.P(["GitHub repo: ", html.A('https://github.com/XXXkoshaster/project_zagadka', href='https://github.com/XXXkoshaster/project_zagadka')])
        ])

    def run(self):
        self.build_layout() 
        self.build_callbacks()
        self.app.run_server(debug=True)


if __name__ == "__main__":
    Page_instance = DashboardBuilder('user_data.json')
    Page_instance.run()
