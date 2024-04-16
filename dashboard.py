import dash
from dash import dash_table, html, dcc, Output, Input, State
import json
import dash_bootstrap_components as dbc
import pandas as pd 
import subprocess
import sys
from datetime import datetime

# класс создает интерфейс страницы
class DashboardBuilder:
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

        
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
                        {'label': user, 'value': user} for user in ['Data user', 'Project info']
                    ],
                ),  
               

                html.Br(),

                dbc.Tabs([dbc.Tab(self.build_project_info(), label="Project info")])
        
        ], style={"fontSize": "20px"})
    
    def build_user_info(self, data):
        return html.Div([html.Br(),
            dash_table.DataTable(
                id='table',
                data=data.to_dict('records'),
                columns=[{"name": i, "id": i} for i in data.columns]
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
                
                if selected_info == 'Data user':
                    json = self.load_data('user_data.json')
                    data = self.getUserInfo(json)
                    return self.build_user_info(data)
                

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
    
    def run(self):
        self.build_layout() 
        self.build_callbacks()
        self.app.run_server(debug=True)             

if __name__ == "__main__":
    Page_instance = DashboardBuilder()
    Page_instance.run()
