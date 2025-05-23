from geopy.geocoders import Nominatim
from scraper.get_methods.get_ages_friends import ages_info
from scraper.get_methods.get_cities_friends import cities_info
from scraper.get_methods.get_coordinates import coord_info
from scraper.get_methods.get_genders_friends import geenders_info
from scraper.get_methods.get_gigachat_answer import get_gigachat_answer
from scraper.get_methods.get_interests import interests_info
from scraper.get_methods.get_marks import marks_info
from scraper.get_methods.get_stat import stat_info
from scraper.get_methods.get_toxic import Toxic
from scraper.get_methods.get_user_info import user_info


class UserProfileParser:
    """
    Класс для парсинга и анализа профилей пользователей ВКонтакте.

    Attributes
    ----------
    cache : dict
        Кэш для хранения координат городов.
    geolocator : geopy.geocoders.Nominatim
        Геолокатор для получения координат городов.

    Methods
    -------
    get_user_info(data)
        Извлекает информацию о пользователе.
    get_ages_friends(friends)
        Вычисляет распределение возрастов друзей.
    get_genders_friends(friends)
        Вычисляет распределение полов среди друзей.
    get_cities_friends(friends)
        Вычисляет распределение городов, в которых живут друзья.
    get_stat(wall)
        Вычисляет количество постов на стене пользователя по месяцам.
    get_coordinates(city)
        Получает координаты (широту и долготу) для указанного города.
    get_marks(wall)
        Вычисляет суммарное количество лайков, комментариев, просмотров и репостов на стене пользователя.
    get_interests(groups)
        Вычисляет распределение интересов среди групп.
    get_toxic(wall)
        Возвращает среднюю вероятность различных типов токсичности для списка постов.
    """

    def __init__(self):
        """
        Инициализирует кэш и геолокатор.
        """
        self.cache = {}
        self.geolocator = Nominatim(user_agent="geoapiExercises")

    def get_user_info(self, data):
        """
        Извлекает информацию о пользователе.

        Parameters
        ----------
        data : dict
            Словарь с данными о пользователе.

        Returns
        -------
        pd.DataFrame
            DataFrame с извлеченной информацией о пользователе.
        """
        return user_info(data)

    def get_ages_friends(self, friends):
        """
        Вычисляет распределение возрастов друзей.

        Parameters
        ----------
        friends : list of dict
            Список словарей, где каждый словарь представляет собой профиль друга.

        Returns
        -------
        pd.DataFrame
            DataFrame с распределением возрастов друзей.
        """
        return ages_info(friends)

    def get_genders_friends(self, friends):
        """
        Вычисляет распределение полов среди друзей.

        Parameters
        ----------
        friends : list of dict
            Список словарей, где каждый словарь представляет собой профиль друга.

        Returns
        -------
        pd.DataFrame
            DataFrame с распределением полов среди друзей.
        """
        return geenders_info(friends)

    def get_cities_friends(self, friends):
        """
        Вычисляет распределение городов, в которых живут друзья.

        Parameters
        ----------
        friends : list of dict
            Список словарей, где каждый словарь представляет собой профиль друга.

        Returns
        -------
        pd.DataFrame
            DataFrame с распределением городов друзей.
        """
        return cities_info(friends)

    def get_stat(self, wall):
        """
        Вычисляет количество постов на стене пользователя по месяцам.

        Parameters
        ----------
        wall : list of dict
            Список словарей, где каждый словарь представляет собой пост на стене пользователя.

        Returns
        -------
        pd.DataFrame
            DataFrame с количеством постов по месяцам.
        """
        return stat_info(wall)

    def get_coordinates(self, city):
        """
        Получает координаты (широту и долготу) для указанного города.

        Parameters
        ----------
        city : str
            Название города.

        Returns
        -------
        tuple of (float, float) or (None, None)
            Кортеж с координатами (широта, долгота) или (None, None), если город не найден.
        """
        return coord_info(city, self.geolocator, self.cache)

    def get_marks(self, wall):
        """
        Вычисляет суммарное количество лайков, комментариев, просмотров и репостов на стене пользователя.

        Parameters
        ----------
        wall : list of dict
            Список словарей, где каждый словарь представляет собой пост на стене пользователя.

        Returns
        -------
        pd.DataFrame
            DataFrame с суммарной статистикой по лайкам, комментариям, просмотрам и репостам.
        """
        return marks_info(wall)

    def get_interests(self, groups):
        """
        Вычисляет распределение интересов среди групп.

        Parameters
        ----------
        groups : list of dict
            Список словарей, где каждый словарь представляет собой информацию о группе.

        Returns
        -------
        pd.DataFrame
            DataFrame с распределением интересов среди групп.
        """
        return interests_info(groups)

    def get_toxic(self, wall):
        """
        Возвращает среднюю вероятность различных типов токсичности для списка постов.

        Parameters
        ----------
        wall : list of dict
            Список словарей, где каждый словарь представляет собой пост на стене пользователя.

        Returns
        -------
        pd.DataFrame
            DataFrame с вероятностями различных типов токсичности.
        """
        toxic = Toxic()
        return toxic.toxicity_info(wall)

    def get_gigachat_answer(self, answer):
        """
        Возвращает ответ от GigaChat API.

        Parameters
        ----------
        answer : dict
            Ответ от GigaChat API в формате словаря.

        Returns
        -------
        list of str
            Список строк, содержащих текстовое содержание из ответа GigaChat.
        """
        return get_gigachat_answer(answer)
