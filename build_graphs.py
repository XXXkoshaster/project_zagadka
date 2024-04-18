import dash
from dash import dash_table, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd 
import plotly.express as px
from scraper_json import UserProfileParser

class BuildGraphs():  
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
        self.parser = UserProfileParser()

    def build_user_info(self, data):
        return html.Div([
            html.Br(),
            dash_table.DataTable(
                id='table',
                data=data.to_dict('records'),
                columns=[{"name": i, "id": i} for i in data.columns]
            )
        ])

    def build_genders_friends(self, data):
        return html.Div([
            dcc.Graph(
                figure=px.pie(names=data.keys(), values=data.values())
            )
        ])
    
    def build_project_info(self):
        return html.Div([
            html.Br(),
            html.P("Web server for analysing data vk users."),
            html.P(["GitHub repo: ", html.A('https://github.com/XXXkoshaster/project_zagadka', href='https://github.com/XXXkoshaster/project_zagadka')])
        ])
    
    def build_map_friends(self, data):
        data['Latitude'], data['Longitude'] = zip(*data['City'].apply(self.parser.get_coordinates))
        
        fig = px.scatter_geo(data,
                    lat="Latitude",
                    lon="Longitude",
                    size="Count",
                    projection="natural earth",
                    hover_name="City")
    
        return html.Div([
            dcc.Graph(figure=fig)
        ])
    
    def build_ages_friends(self, data):
        data_json = data.to_json(date_format='iso', orient='split', default_handler=str)    
        return  html.Div([
            dcc.Dropdown(
                id='first_color_picker',
                options=[{'label': color, 'value': color} for color in ['blue', 'red', 'yellow', 'green']],
                value='blue',
                clearable=False
            ),
            dcc.Graph(
                id = 'histogram'
            ),
            dcc.Store(
                id='first_store',
                data=data_json
            )
        ])
    
    def build_first_color_picker(self):
        @self.app.callback(
            Output('histogram', 'figure'),
            [Input('first_color_picker', 'value'),
            State('first_store', 'data')]
        )

        def update_histogram(selected_color, stored_data_json):
            stored_data_df = pd.read_json(stored_data_json, orient='split')
            fig = px.histogram(stored_data_df, x='Age', y='Count', color_discrete_sequence=[selected_color], nbins=14)

            return fig
    
    def build_stats(self, data, table):
        data_json = data.to_json(date_format='iso', orient='split', default_handler=str)    
        return  html.Div([
            dcc.Dropdown(
                id='second_color_picker',
                options=[{'label': color, 'value': color} for color in ['blue', 'red', 'yellow', 'green']],
                value='blue',
                clearable=False
            ),
            html.Br(),
            html.P(
                'Статистика акнивности пользователя по месяцам за последнии 100 публикаций'
            ),
            dcc.Graph(
                id = 'graph'
            ),
            dcc.Store(
                id='second_store',
                data=data_json
            ),
            html.Br(),
            
            dash_table.DataTable(
                id='table',
                data=table.to_dict('records'),
                columns=[{"name": i, "id": i} for i in table.columns]
            )
        ])
    
    def build_second_color_picker(self):
        @self.app.callback(
            Output('graph', 'figure'),
            [Input('second_color_picker', 'value'),
            State('second_store', 'data')]
        )

        def update_graph(selected_color, stored_data_json):
            stored_data_df = pd.read_json(stored_data_json, orient='split')
            fig = px.scatter(stored_data_df, x='Mounth', y='Count posts', color_discrete_sequence=[selected_color])

            return fig
   
    def build_interests(self, data):
        data_json = data.to_json(date_format='iso', orient='split', default_handler=str)    
        return  html.Div([
            dcc.Dropdown(
                id='third_color_picker',
                options=[{'label': color, 'value': color} for color in ['blue', 'red', 'yellow', 'green']],
                value='blue',
                clearable=False
            ),
            dcc.Graph(
                id = 'bar'
            ),
            dcc.Store(
                id='third_store',
                data=data_json
            )
        ])
    
    def build_third_color_picker(self):
        @self.app.callback(
            Output('bar', 'figure'),
            [Input('third_color_picker', 'value'),
            State('third_store', 'data')]
        )

        def update_bar(selected_color, stored_data_json):
            stored_data_df = pd.read_json(stored_data_json, orient='split')
            fig = px.bar(stored_data_df, x='Activities', y='States', color_discrete_sequence=[selected_color])

            return fig