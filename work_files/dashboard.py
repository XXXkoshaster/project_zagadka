import dash
from dash import html, dcc, Output, Input, State
import json
import dash_bootstrap_components as dbc
from scraper import VkApp
from build_graphs import BuildGraphs

# класс создает интерфейс страницы
class DashboardBuilder(BuildGraphs):
    def __init__(self):
        super().__init__()

    def load_data(self, filepath):
        with open(filepath) as f:
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
                        {'label': user, 'value': user} for user in ['Data user', 'Ages of friends', 'Gender of friends', 'Cites of friends', 'Static', 'Interests']
                    ],
                ),  
               
                dcc.Loading(
                    id="loading-info-output",
                    children=[html.Div(id="info_output")],
                    type="default",
                ),

                html.Br(),

                dbc.Tabs([dbc.Tab(self.build_project_info(), label="Project info")])
        
        ], style={"fontSize": "20px"})

    
    def build_callbacks(self):
        @self.app.callback(
            Output('info_output', 'children'),
            [Input('button', 'n_clicks'),
            Input('info_dropdown', 'value')],
            [State('input_link', 'value')]
        )

        def process_url(n_clicks, selected_info, url):
            if n_clicks > 0 and url:
                try:
                    VkApp(url)
                except Exception as e:
                    print(f"Ошибка при получении данных: {e}")
                    
                if selected_info == 'Data user':
                    json = self.load_data('user_data.json')
                    data = self.parser.get_user_info(json)
                    return self.build_user_info(data)
                
                elif selected_info == 'Ages of friends':
                    json = self.load_data('friends_data.json')
                    data = self.parser.get_ages_friends(json)
                    return self.build_ages_friends(data)

                elif selected_info == 'Gender of friends':
                    json = self.load_data('friends_data.json')
                    data = self.parser.get_genders_friends(json)
                    return self.build_genders_friends(data)
                
                elif selected_info == 'Cites of friends':
                    json = self.load_data('friends_data.json')
                    data = self.parser.get_cities_friends(json)
                    return self.build_map_friends(data)
                
                elif selected_info == 'Static':
                    json = self.load_data('wall_data.json')
                    data = self.parser.get_toxic(json)
                    table = self.parser.get_marks(json)
                    return self.build_stats(data, table)
                
                elif selected_info == 'Interests':
                    json = self.load_data('groups_data.json')
                    data = self.parser.get_interests(json)
                    return self.build_interests(data)
                
            return html.Div()
        
    def run(self):
        self.build_layout()
        self.build_callbacks()
        self.build_first_color_picker()
        self.build_second_color_picker()
        self.build_third_color_picker()
        self.app.run_server(debug=True)             

if __name__ == "__main__":
    Page_instance = DashboardBuilder()
    Page_instance.run()

    