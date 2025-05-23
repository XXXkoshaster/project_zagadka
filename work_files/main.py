import json

import dash_bootstrap_components as dbc
from build_graphs import BuildGraphs
from create_data_base import VkApp
from dash import Input, Output, State, dcc, html
from gigachat import GigaChat


class DashboardBuilder(BuildGraphs):
    """
    Класс для создания и запуска веб-дэшборда с использованием Dash и Plotly.

    Methods
    -------
    load_data(filepath)
        Загружает данные из указанного файла.
    build_layout()
        Создает макет веб-дэшборда.
    build_callbacks()
        Создает колбэки для обработки взаимодействий с веб-дэшбордом.
    run()
        Запускает веб-дэшборд.
    """

    def __init__(self):
        """
        Инициализирует экземпляр DashboardBuilder.
        """
        super().__init__()

    def load_data(self, filepath):
        """
        Загружает данные из указанного файла.

        Parameters
        ----------
        filepath : str
            Путь к файлу с данными.

        Returns
        -------
        dict
            Содержимое файла в виде словаря.
        """
        with open(filepath) as f:
            return json.load(f)

    def build_layout(self):
        """
        Создает макет веб-дэшборда.

        Returns
        -------
        None
        """
        self.app.layout = html.Div(
            [
                html.H1(
                    children="PROJECT ZAGADKA",
                    style={"color": "blue", "fontSize": "40px"},
                ),
                html.H2("VK scraper"),
                html.Div(
                    [
                        dcc.Input(
                            id="input_link", type="text", placeholder="Put your URL"
                        ),
                        html.Button(
                            "Submit",
                            id="button",
                            n_clicks=0,
                        ),
                    ]
                ),
                dcc.Dropdown(
                    id="info_dropdown",
                    options=[
                        {"label": user, "value": user}
                        for user in [
                            "Data user",
                            "Ages of friends",
                            "Gender of friends",
                            "Cites of friends",
                            "Stats",
                            "Interests",
                            "Toxicity",
                            "GigaChat",
                        ]
                    ],
                ),
                dcc.Loading(
                    id="loading-info-output",
                    children=[html.Div(id="info_output")],
                    type="default",
                ),
                html.Br(),
                dbc.Tabs([dbc.Tab(self.build_project_info(), label="Project info")]),
            ],
            style={"fontSize": "20px"},
        )

    def build_callbacks(self):
        """
        Создает колбэки для обработки взаимодействий с веб-дэшбордом.

        Returns
        -------
        None
        """

        @self.app.callback(
            Output("info_output", "children"),
            [Input("button", "n_clicks"), Input("info_dropdown", "value")],
            [State("input_link", "value")],
        )
        def process_url(n_clicks, selected_info, url):
            if n_clicks > 0 and url:
                try:
                    VkApp(url)
                except Exception as e:
                    print(f"Ошибка при получении данных: {e}")

                if selected_info == "Data user":
                    json = self.load_data(
                        "/home/xxxkoshaster/Documents/Zagadka/work_files/data_base/user_data.json"
                    )
                    data = self.parser.get_user_info(json)
                    return self.build_user_info(data)

                elif selected_info == "Ages of friends":
                    json = self.load_data(
                        "/home/xxxkoshaster/Documents/Zagadka/work_files/data_base/friends_data.json"
                    )
                    data = self.parser.get_ages_friends(json)
                    return self.build_ages_friends(data)

                elif selected_info == "Gender of friends":
                    json = self.load_data(
                        "/home/xxxkoshaster/Documents/Zagadka/work_files/data_base/friends_data.json"
                    )
                    data = self.parser.get_genders_friends(json)
                    return self.build_genders_friends(data)

                elif selected_info == "Cites of friends":
                    json = self.load_data(
                        "/home/xxxkoshaster/Documents/Zagadka/work_files/data_base/friends_data.json"
                    )
                    data = self.parser.get_cities_friends(json)
                    return self.build_map_friends(data)

                elif selected_info == "Stats":
                    json = self.load_data(
                        "/home/xxxkoshaster/Documents/Zagadka/work_files/data_base/wall_data.json"
                    )
                    data = self.parser.get_stat(json)
                    table = self.parser.get_marks(json)
                    return self.build_stats(data, table)

                elif selected_info == "Interests":
                    json = self.load_data(
                        "/home/xxxkoshaster/Documents/Zagadka/work_files/data_base/groups_data.json"
                    )
                    data = self.parser.get_interests(json)
                    return self.build_interests(data)

                elif selected_info == "Toxicity":
                    json = self.load_data(
                        "/home/xxxkoshaster/Documents/Zagadka/work_files/data_base/wall_data.json"
                    )
                    data = self.parser.get_toxic(json)
                    return self.build_toxicity(data)

                elif selected_info == "GigaChat":
                    chat = GigaChat()
                    chat.create_request()
                    json = self.load_data(
                        "/home/xxxkoshaster/Documents/Zagadka/work_files/data_base/gigachat_response.json"
                    )
                    data = self.parser.get_gigachat_answer(json)
                    return self.build_gigachat_response(data)

            return html.Div()

    def run(self):
        """
        Запускает веб-дэшборд.

        Returns
        -------
        None
        """
        self.build_layout()
        self.build_callbacks()
        self.build_ages_color_picker()
        self.build_stats_color_picker()
        self.build_interests_color_picker()
        self.build_toxicity_color_picker()
        self.app.run_server(debug=True)


if __name__ == "__main__":
    Page_instance = DashboardBuilder()
    Page_instance.run()
