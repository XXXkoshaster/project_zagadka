import dash
from dash import dash_table, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from scraper.scraper_json import UserProfileParser
from io import StringIO

class BuildGraphs:
    """
    Класс для построения графиков и отображения данных пользователей ВКонтакте с использованием Dash и Plotly.

    Attributes
    ----------
    app : dash.Dash
        Экземпляр Dash приложения.
    parser : UserProfileParser
        Экземпляр парсера профилей пользователей.

    Methods
    -------
    build_user_info(data)
        Создает компонент для отображения информации о пользователе.
    build_genders_friends(data)
        Создает компонент для отображения распределения полов среди друзей.
    build_map_friends(data)
        Создает компонент для отображения географического распределения друзей.
    build_ages_friends(data)
        Создает компонент для отображения распределения возрастов друзей.
    build_ages_color_picker()
        Колбэк для обновления гистограммы распределения возрастов.
    build_stats(data, table)
        Создает компонент для отображения статистики активности пользователя.
    build_stats_color_picker()
        Колбэк для обновления графика статистики активности.
    build_interests(data)
        Создает компонент для отображения распределения интересов.
    build_interests_color_picker()
        Колбэк для обновления гистограммы распределения интересов.
    build_toxicity(data)
        Создает компонент для отображения токсичности постов.
    build_toxicity_color_picker()
        Колбэк для обновления гистограммы токсичности постов.
    build_project_info()
        Создает компонент для отображения информации о проекте.
    build_gigachat_response()
        Создает компонент для отображения краткой информации о пользователе с помощью gigachat.
    """

    def __init__(self):
        """
        Инициализирует экземпляр BuildGraphs с приложением Dash и парсером профилей пользователей.
        """
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
        self.parser = UserProfileParser()

    def build_user_info(self, data):
        """
        Создает компонент для отображения информации о пользователе.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame с информацией о пользователе.

        Returns
        -------
        html.Div
            Компонент для отображения информации о пользователе.
        """
        return html.Div([
            html.Br(),
            dash_table.DataTable(
                id='table',
                data=data.to_dict('records'),
                columns=[{"name": i, "id": i} for i in data.columns]
            )
        ])

    def build_genders_friends(self, data):
        """
        Создает компонент для отображения распределения полов среди друзей.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame с распределением полов среди друзей.

        Returns
        -------
        html.Div
            Компонент для отображения распределения полов среди друзей.
        """
        return html.Div([
            dcc.Graph(
                figure=px.pie(names=data["Sex"], values=data["Count"])  
            )
        ])

    def build_map_friends(self, data):
        """
        Создает компонент для отображения географического распределения друзей.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame с информацией о городах друзей.

        Returns
        -------
        html.Div
            Компонент для отображения географического распределения друзей.
        """
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
        """
        Создает компонент для отображения распределения возрастов друзей.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame с распределением возрастов друзей.

        Returns
        -------
        html.Div
            Компонент для отображения распределения возрастов друзей.
        """
        data_json = data.to_json(date_format='iso', orient='split', default_handler=str)
        return html.Div([
            dcc.Dropdown(
                id='ages_color_picker',
                options=[{'label': color, 'value': color} for color in ['blue', 'red', 'yellow', 'green']],
                value='blue',
                clearable=False
            ),
            dcc.Graph(
                id='histogram'
            ),
            dcc.Store(
                id='ages_store',
                data=data_json
            )
        ])

    def build_ages_color_picker(self):
        """
        Колбэк для обновления гистограммы распределения возрастов.

        Returns
        -------
        None
        """
        @self.app.callback(
            Output('histogram', 'figure'),
            [Input('ages_color_picker', 'value'),
             State('ages_store', 'data')]
        )
        def update_histogram(selected_color, stored_data_json):
            stored_data_df = pd.read_json(StringIO(stored_data_json), orient='split')
            fig = px.histogram(stored_data_df, x='Age', y='Count', color_discrete_sequence=[selected_color], nbins=14)
            return fig

    def build_stats(self, data, table):
        """
        Создает компонент для отображения статистики активности пользователя.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame с данными о статистике активности пользователя.
        table : pd.DataFrame
            DataFrame с дополнительной информацией о статистике активности пользователя.

        Returns
        -------
        html.Div
            Компонент для отображения статистики активности пользователя.
        """
        data_json = data.to_json(date_format='iso', orient='split', default_handler=str)
        return html.Div([
            dcc.Dropdown(
                id='stats_color_picker',
                options=[{'label': color, 'value': color} for color in ['blue', 'red', 'yellow', 'green']],
                value='blue',
                clearable=False
            ),
            html.Br(),
            html.P(
                'Статистика активности пользователя по месяцам за последние 100 публикаций'
            ),
            dcc.Graph(
                id='graph'
            ),
            dcc.Store(
                id='stats_store',
                data=data_json
            ),
            html.Br(),
            dash_table.DataTable(
                id='table',
                data=table.to_dict('records'),
                columns=[{"name": i, "id": i} for i in table.columns]
            )
        ])

    def build_stats_color_picker(self):
        """
        Колбэк для обновления графика статистики активности.

        Returns
        -------
        None
        """
        @self.app.callback(
            Output('graph', 'figure'),
            [Input('stats_color_picker', 'value'),
             State('stats_store', 'data')]
        )
        def update_graph(selected_color, stored_data_json):
            stored_data_df = pd.read_json(StringIO(stored_data_json), orient='split')
            fig = px.scatter(stored_data_df, x='Mounth', y='Count posts', color_discrete_sequence=[selected_color])
            return fig

    def build_interests(self, data):
        """
        Создает компонент для отображения распределения интересов.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame с распределением интересов.

        Returns
        -------
        html.Div
            Компонент для отображения распределения интересов.
        """
        data_json = data.to_json(date_format='iso', orient='split', default_handler=str)
        return html.Div([
            dcc.Dropdown(
                id='interests_color_picker',
                options=[{'label': color, 'value': color} for color in ['blue', 'red', 'yellow', 'green']],
                value='blue',
                clearable=False
            ),
            dcc.Graph(
                id='interests_bar'
            ),
            dcc.Store(
                id='interests_store',
                data=data_json
            )
        ])

    def build_interests_color_picker(self):
        """
        Колбэк для обновления гистограммы распределения интересов.

        Returns
        -------
        None
        """
        @self.app.callback(
            Output('interests_bar', 'figure'),
            [Input('interests_color_picker', 'value'),
             State('interests_store', 'data')]
        )
        def update_interests_bar(selected_color, stored_data_json):
            stored_data_df = pd.read_json(StringIO(stored_data_json), orient='split')
            fig = px.bar(stored_data_df, x='Activities', y='States', color_discrete_sequence=[selected_color])
            return fig

    def build_toxicity(self, data):
        """
        Создает компонент для отображения токсичности постов.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame с данными о токсичности постов.

        Returns
        -------
        html.Div
            Компонент для отображения токсичности постов.
        """
        data_json = data.to_json(date_format='iso', orient='split', default_handler=str)
        return html.Div([
            dcc.Dropdown(
                id='toxicity_color_picker',
                options=[{'label': color, 'value': color} for color in ['blue', 'red', 'yellow', 'green']],
                value='blue',
                clearable=False,
            ),
            dcc.Graph(
                id='toxicity_bar'
            ),
            dcc.Store(
                id='toxicity_store',
                data=data_json
            )
        ])

    def build_toxicity_color_picker(self):
        """
        Колбэк для обновления гистограммы токсичности постов.

        Returns
        -------
        None
        """
        @self.app.callback(
            Output('toxicity_bar', 'figure'),
            [Input('toxicity_color_picker', 'value'),
             State('toxicity_store', 'data')]
        )
        def update_toxicity_bar(selected_color, stored_data_json):
            stored_data_df = pd.read_json(StringIO(stored_data_json), orient='split')
            fig = px.bar(stored_data_df, x=['Non-toxic', 'Insult', 'Obscenity', 'Threat', 'Dangerous'], y='Probability', color_discrete_sequence=[selected_color])
            return fig

    def build_project_info(self):
        """
        Создает компонент для отображения информации о проекте.

        Returns
        -------
        html.Div
            Компонент для отображения информации о проекте.
        """
        return html.Div([
            html.Br(),
            html.P('Web server for analysing data vk users.'),
            html.P(['GitHub repo: ', html.A('https://github.com/XXXkoshaster/project_zagadka', href='https://github.com/XXXkoshaster/project_zagadka')])
        ])

    def build_gigachat_response(self, text):
        """
        Создает компонент для отображения краткой информации о пользователе с помощью gigachat.

        Parameters
        ----------
        text : str
            Текст ответа от GigaChat.

        Returns
        -------
        html.Div
            Компонент для отображения информации о пользователе.
        """
        answer = [html.P(line) for line in text]

        return html.Div([
            html.Br(),
            html.H4('Краткая информация о пользователи от GigaChat'),
            *answer
        ])