import json
import re
from datetime import datetime


class DataProcessor:
    """
    Класс для обработки данных пользователей ВКонтакте.

    Methods
    -------
    get_user_id(url)
        Извлекает идентификатор пользователя из URL.
    save_data(file_path, data)
        Сохраняет данные в файл JSON.
    time_convertor(data_wall)
        Конвертирует временную метку в читаемый формат даты и времени.
    gender_convertor(data_friends)
        Конвертирует числовое значение пола в строковое представление.
    convert_user_data(user_data)
        Конвертирует данные пользователя.
    convert_friends_data(friends_data)
        Конвертирует данные друзей.
    convert_wall_data(wall_data)
        Конвертирует данные стены (постов).
    """

    @staticmethod
    def get_user_id(url):
        """
        Извлекает идентификатор пользователя из URL.

        Parameters
        ----------
        url : str
            URL страницы пользователя ВКонтакте.

        Returns
        -------
        str or None
            Идентификатор пользователя, если он найден, иначе None.

        Raises
        ------
        Exception
            Возникает, если URL некорректен или отсутствует идентификатор пользователя.

        Examples
        --------
        >>> DataProcessor.get_user_id('https://vk.com/username')
        'username'
        """
        try:
            match = re.search(r"vk.com/(\w+)", url)
            return match.group(1)
        except Exception as e:
            print(f"Некорректный URL или отсутствует идентификатор пользователя: {e}")

    @staticmethod
    def save_data(file_path, data):
        """
        Сохраняет данные в файл JSON.

        Parameters
        ----------
        file_path : str
            Путь к файлу для сохранения данных.
        data : dict
            Данные для сохранения.

        Raises
        ------
        Exception
            Возникает, если происходит ошибка при сохранении файла.

        Examples
        --------
        >>> data = {'key': 'value'}
        >>> DataProcessor.save_data('data.json', data)
        """
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

    @staticmethod
    def time_convertor(data_wall):
        """
        Конвертирует временную метку в читаемый формат даты и времени.

        Parameters
        ----------
        data_wall : dict
            Словарь с данными о посте, содержащий ключ 'date'.

        Raises
        ------
        Exception
            Возникает, если отсутствует ключ 'date' в объекте данных.

        Examples
        --------
        >>> post = {'date': 1617184800}
        >>> DataProcessor.time_convertor(post)
        >>> post['date']
        '2021-03-31 12:00:00'
        """
        try:
            date_time = datetime.utcfromtimestamp(data_wall["date"])
            formatted_date = date_time.strftime("%Y-%m-%d %H:%M:%S")
            data_wall["date"] = formatted_date
        except Exception:
            print('Отсутствует ключ "date" в объекте данных')

    @staticmethod
    def gender_convertor(data_friends):
        """
        Конвертирует числовое значение пола в строковое представление.

        Parameters
        ----------
        data_friends : dict
            Словарь с данными о друге, содержащий ключ 'sex'.

        Raises
        ------
        Exception
            Возникает, если отсутствует ключ 'sex' в объекте данных.

        Examples
        --------
        >>> friend = {'sex': 2}
        >>> DataProcessor.gender_convertor(friend)
        >>> friend['sex']
        'Мужской'
        """
        try:
            if data_friends["sex"] == 2:
                data_friends["sex"] = "Мужской"
            elif data_friends["sex"] == 1:
                data_friends["sex"] = "Женский"
            else:
                data_friends["sex"] = None
        except Exception:
            print('Отсутствует ключ "sex" в объекте данных')

    @staticmethod
    def convert_user_data(user_data):
        """
        Конвертирует данные пользователя.

        Parameters
        ----------
        user_data : dict
            Словарь с данными о пользователе.

        Examples
        --------
        >>> user = {'sex': 2}
        >>> DataProcessor.convert_user_data(user)
        >>> user['sex']
        'Мужской'
        """
        DataProcessor.gender_convertor(user_data)

    @staticmethod
    def convert_friends_data(friends_data):
        """
        Конвертирует данные друзей.

        Parameters
        ----------
        friends_data : dict
            Словарь с данными о друзьях, содержащий ключ 'items', который является списком данных о каждом друге.

        Examples
        --------
        >>> friends = {'items': [{'sex': 2}, {'sex': 1}]}
        >>> DataProcessor.convert_friends_data(friends)
        >>> friends['items'][0]['sex']
        'Мужской'
        >>> friends['items'][1]['sex']
        'Женский'
        """
        for friend in friends_data["items"]:
            DataProcessor.gender_convertor(friend)

    @staticmethod
    def convert_wall_data(wall_data):
        """
        Конвертирует данные стены (постов).

        Parameters
        ----------
        wall_data : dict
            Словарь с данными о стене, содержащий ключ 'items', который является списком данных о каждом посте.

        Examples
        --------
        >>> wall = {'items': [{'date': 1617184800}]}
        >>> DataProcessor.convert_wall_data(wall)
        >>> wall['items'][0]['date']
        '2021-03-31 12:00:00'
        """
        for post in wall_data["items"]:
            DataProcessor.time_convertor(post)
