import dash
from dash import dash_table, html, dcc, Output, Input, State
import json
import dash_bootstrap_components as dbc
import pandas as pd 
import subprocess
import sys
import plotly.express as px
from datetime import datetime
from geopy.geocoders import Nominatim

# класс создает интерфейс страницы
class DashboardBuilder:
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
        self.geolocator = Nominatim(user_agent="geoapiExercises")
        self.cache = dict()        

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
    
    def build_callbacks(self):
        @self.app.callback(
            Output('info_output', 'children'),
            [Input('button', 'n_clicks'),
            Input('info_dropdown', 'value')],
            [State('input_link', 'value')]
        )

        def process_url(n_clicks, selected_info, url):
            if n_clicks > 0 and url:
                subprocess.run([sys.executable, 'scraper.py', url], check=True, stdout=subprocess.PIPE)
                
                if selected_info == 'Data user':
                    json = self.load_data('user_data.json')
                    data = self.getUserInfo(json)
                    return self.build_user_info(data)
                
                elif selected_info == 'Ages of friends':
                    json = self.load_data('friends_data.json')
                    data = self.getAgesFriends(json)
                    return self.build_ages_friends(data)

            return html.Div()

    def getUserInfo(self, data):
        data_general = pd.Series(data, index=["id", "domain", "first_name", "last_name", "sex", "bdate"])
        data_country = pd.Series(data["country"]["title"], index=["country"])
        data_city = pd.Series(data["city"]["title"], index=["city"])
        data_univer = pd.Series()
        data_schools = pd.Series()

        for i in data["universities"]:
            tmp = pd.Series(i, index=["name", "faculty_name", "chair_name", "graduation"])
            tmp["faculty_name"] = tmp["faculty_name"].rstrip()
            tmp.rename(index={"name": "university"}, inplace=True)
            data_univer = pd.concat([data_univer, tmp])
        

        for i in data["schools"]:
            tmp = pd.Series(i, index=["name", "class", "speciality", "year_from", "year_to"])
            
            if "колледж" in i["name"].lower():
                tmp.rename(index={"name": "kollage"}, inplace=True)
            else:
                tmp.rename(index={"name": "school"}, inplace=True)

            data_schools= pd.concat([data_schools, tmp])

        data_schools = data_schools[data_schools.notna()]
        seria = pd.concat([data_general, data_country, data_city, data_schools, data_univer])

        return seria.to_frame(name='values').T
    
    def getAgesFriends(self, friends):
        ages = dict()

        for i in friends:
            if "bdate" in i.keys():
                year = i["bdate"].split('.')
                if len(year) == 3:
                    age = datetime.now().year - int(year[2]) 
                    if age not in ages:
                        ages[age] = 1
                    else: 
                        ages[age] += 1
                else:
                    continue
            else:
                continue
       
        ages = pd.DataFrame(ages.items(),columns=['Age', 'Count'])
        
        return ages[(ages['Age'] > 5) & (ages['Age'] < 90)]
 
    def getGendersFriends(self, friends):
        genders = dict()

        for i in friends:
            sex = i["sex"]
            if sex:
                if sex not in genders:
                    genders[sex] = 1
                else:
                    genders[sex] += 1
            else:
                continue

        return genders 
    
    def getCitiesFriends(self, friends):    
        cities = dict()

        for i in friends:
            if "city" in i.keys():
                city = i["city"]["title"]
                
                if city not in cities:
                    cities[city] = 1
                else:
                    cities[city] += 1
            else:
                continue
        
        cities = pd.DataFrame(cities.items(), columns=['City', 'Count'])
        return cities

    def getToxic(self, wall):
        toxic = dict()

        for i in wall:
            date = i["date"][:7]
            if date not in toxic:
                toxic[date] = 1
            else: 
                toxic[date] += 1

        return pd.DataFrame(toxic.items(), columns=['Mounth', 'Count posts'])

    def getCoordinates(self, city):
        if city in self.cache:
            return self.cache[city]
            
        else:
            location = self.geolocator.geocode(city)
            if location:
                self.cache[city] = (location.latitude, location.longitude)
                return self.cache[city]
            else:
                return None, None
    
    def getMarks(self, wall):
        likes = 0
        comments = 0
        views = 0
        reposts = 0

        for i in wall:
            likes += i["likes"]["count"]
            comments += i["comments"]["count"]
            views += i["views"]["count"]
            reposts += i["reposts"]["count"]

        return pd.DataFrame({'stats': ['likes', 'comments', 'views', 'reposts'], 'values':[likes, comments, views, reposts]})
    
    def getInterests(self, groups):
        interests = dict()

        for i in groups:
            act = i["activity"]
            if act not in interests:
                interests[act] = 1
            else:
                interests[act] += 1

        interests = pd.DataFrame(interests.items(), columns=["Activities", "States"])

        return interests
    
    def run(self):
        self.build_layout()
        self.build_callbacks()
        self.build_first_color_picker()
        self.app.run_server(debug=True)             

if __name__ == "__main__":
    Page_instance = DashboardBuilder()
    Page_instance.run()
