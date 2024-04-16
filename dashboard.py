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
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

        
    def load_data(self):
        with open(self.filepath) as f:
            return json.load(f)
    
    def build_layout(self):
        self.app.layout = html.Div([
                html.H1(children="PROJECT ZAGADKA", style={"color": "blue", "fontSize": "40px"}),
                
                html.H2("VK scraper"),
                
                html.Div([
                    dcc.Input(
                        id='input_link',
                        type='text',
                        placeholder='Put your URL'
                    ), 
                    html.Button(
                        'Submit',
                        id='button',
                        n_clicks=0,
                    )
                ]),  

                dcc.Dropdown(
                    id='info_dropdown', 
                    options=[
                        {'label': user, 'value': user} for user in ['Data user', 'Project info']
                    ],
                ),  
               
                html.Div(id='info_output'),

                html.Br(),

                dbc.Tabs([dbc.Tab(self.build_project_info(), label="Project info")])
        
        ], style={"fontSize": "20px"})
    
    def build_user_info(self, data):
        return html.Div([html.Br(),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in data.columns],
                data=data.to_dict('records'),
            )
        ])
    
    def build_project_info(self):
        return html.Div([
            html.Br(),
            html.P("Web server for analysing data vk users."),
            html.P(["GitHub repo: ", html.A('https://github.com/XXXkoshaster/project_zagadka', href='https://github.com/XXXkoshaster/project_zagadka')])
        ])

    def build_callbacks(self):
        @self.app.callback(
            Output('info_output', 'children'),
            [Input('button', 'n_clicks'),
            Input('info_dropdown', 'value')],
            [State('input_link', 'value')]
        )
        def process_url(n_clicks, selected_info, url):
            if n_clicks > 0 and url:
                subprocess.run([sys.executable, 'test.py', url], check=True, stdout=subprocess.PIPE)
                json = self.load_data()
                data = pd.DataFrame(json)
                
                if selected_info == 'Data user':
                    return self.build_user_info(data)
                elif selected_info == 'Project info':
                    return self.build_project_info()

            return html.Div()

    def run(self):
        self.build_layout() 
        self.build_callbacks()
        self.app.run_server(debug=True)             

if __name__ == "__main__":
    Page_instance = DashboardBuilder('user_data.json')
    Page_instance.run()

