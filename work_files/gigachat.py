import requests
import json
import urllib3
from get_sber_token import GigaChatToken
from scraper.scraper_json import UserProfileParser
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GigaChat:
    """
    Класс для взаимодействия с GigaChat API.

    Attributes
    ----------
    api_url : str
        URL для отправки запросов к GigaChat API.
    token : str
        Токен аутентификации для доступа к GigaChat API.
    parser : UserProfileParser
        Объект для парсинга данных пользователя.
    """

    def __init__(self):
        """
        Инициализация класса GigaChat.
        """
        self.api_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        self.token = GigaChatToken().return_token()
        self.parser = UserProfileParser()

    def load_data(self, filepath):
        """
        Загружает данные из указанного файла JSON.

        Parameters
        ----------
        filepath : str
            Путь к файлу JSON.

        Returns
        -------
        dict or None
            Загруженные данные в виде словаря или None, если произошла ошибка.
        """
        try:
            with open(filepath) as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка при загрузке данных из файла {filepath}: {str(e)}")
            return None

    def get_data(self):
        """
        Загружает и обрабатывает данные пользователя из файлов.

        Returns
        -------
        tuple of DataFrame or None
            Кортеж, содержащий обработанные данные в виде DataFrame, или None, если произошла ошибка.
        """
        base_path = '/home/xxxkoshaster/Documents/Zagadka/work_files/data_base'
        df_friends = self.load_data(os.path.join(base_path, 'friends_data.json'))
        df_user = self.load_data(os.path.join(base_path, 'user_data.json'))
        df_groups = self.load_data(os.path.join(base_path, 'groups_data.json'))
        df_wall = self.load_data(os.path.join(base_path, 'wall_data.json'))

        if df_friends is None or df_user is None or df_groups is None or df_wall is None:
            print("Ошибка при загрузке данных.")
            return None, None, None, None, None, None, None, None

        try:
            age_friends = self.parser.get_ages_friends(df_friends)
            general_user_info = self.parser.get_user_info(df_user)
            genders_friends = self.parser.get_genders_friends(df_friends)
            cities_friends = self.parser.get_cities_friends(df_friends)
            stats = self.parser.get_stat(df_wall)
            marks = self.parser.get_marks(df_wall)
            interests = self.parser.get_interests(df_groups)
            toxicity = self.parser.get_toxic(df_wall)
        except AttributeError as e:
            print(f"Ошибка в обработке данных: {str(e)}")
            return None, None, None, None, None, None, None, None

        return age_friends, general_user_info, genders_friends, cities_friends, stats, marks, interests, toxicity

    def prepare_payload(self, user_message):
        """
        Формирует тело запроса для GigaChat API.

        Parameters
        ----------
        user_message : str
            Сообщение пользователя для отправки в GigaChat.

        Returns
        -------
        str
            Тело запроса в формате JSON.
        """
        return json.dumps({
            'model': 'GigaChat',
            'messages': [
                {
                    'role': 'user',
                    'content': user_message
                }
            ],
            'temperature': 1,
            'top_p': 0.1,
            'n': 1,
            'stream': False,
            'max_tokens': 512,
            'repetition_penalty': 1,
            'update_interval': 0
        })

    def send_request(self, user_message):
        """
        Отправляет запрос к GigaChat API и возвращает ответ.

        Parameters
        ----------
        user_message : str
            Сообщение пользователя для отправки в GigaChat.

        Returns
        -------
        dict or None
            Ответ от GigaChat API в виде словаря или None, если произошла ошибка.
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        payload = self.prepare_payload(user_message)

        try:
            response = requests.post(self.api_url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при выполнении запроса: {str(e)}")
            return None

    def create_request(self):
        """
        Загружает данные, отправляет их к GigaChat API частями и сохраняет ответы в файл.
        """
        if not self.token:
            print("Не удалось получить токен.")
            return

        age_friends, general_user_info, genders_friends, cities_friends, stats, marks, interests, toxicity = self.get_data()

        if age_friends is None:
            print("Ошибка при обработке данных.")
            return

        age_friends_json = age_friends.to_json(orient='records', force_ascii=False)
        general_user_info_json = general_user_info.to_json(orient='records', force_ascii=False)
        genders_friends_json = genders_friends.to_json(orient='records', force_ascii=False)
        cities_friends_json_1 = cities_friends.head(len(cities_friends)//3).to_json(orient='records', force_ascii=False)
        cities_friends_json_2 = cities_friends.tail(len(cities_friends)//3).to_json(orient='records', force_ascii=False)
        stats_json = stats.to_json(orient='records', force_ascii=False)
        marks_json = marks.to_json(orient='records', force_ascii=False)
        interests_json = interests.to_json(orient='records', force_ascii=False)
        toxicity_json = toxicity.to_json(orient='records', force_ascii=False)

        responses = {}

        responses['general_user_info'] = self.send_request(f"Сделай краткую выжимку о пользователе ВК по переданным данным, которые содержат информацию об общей информации пользователя:\n{general_user_info_json}")
        responses['age_friends'] = self.send_request(f"Статистика распределения друзей пользователя по возрасту. Не составляй таблицу:\n{age_friends_json}")
        responses['genders_friends'] = self.send_request(f"Статистика распределения друзей пользователя по полу:\n{genders_friends_json}")
        responses['cities_friends_1'] = self.send_request(f"Статистика распределения друзей пользователя по городам. Составь список с этой информацией, не составляя таблицу:\n{cities_friends_json_1}")
        responses['cities_friends_2'] = self.send_request(f"Статистика распределения друзей пользователя по городам. Составь список с этой информацией, не составляя таблицу:\n{cities_friends_json_2}")
        responses['stats'] = self.send_request(f"Активность пользователя:\n{stats_json}")
        responses['marks'] = self.send_request(f"Статистика со стены:\n{marks_json}")
        responses['interests'] = self.send_request(f"Интересы пользователя:\n{interests_json}")
        responses['toxicity'] = self.send_request(f"Оценка токсичности пользователя по переданным данным, которые содержат вероятности нетоксичности, грубость, непристойности, агрессивности, опасности пользователя. Если нет значений, то написать, что нет сведений о токсичности:\n{toxicity_json}")

        with open('/home/xxxkoshaster/Documents/Zagadka/work_files/data_base/gigachat_response.json', 'w', encoding='utf-8') as f:
            json.dump(responses, f, ensure_ascii=False, indent=2)
