import vk_api

class VkProfile:
    """
    Класс для взаимодействия с API ВКонтакте и получения информации о профиле пользователя.

    Attributes
    ----------
    session : vk_api.VkApi
        Сессия VK API, используемая для выполнения запросов.
    api : vk_api.vk_api.VkApiMethod
        Объект для выполнения методов VK API.

    Methods
    -------
    get_user_info(user_id)
        Получает информацию о пользователе.
    get_friends_info(user_id)
        Получает информацию о друзьях пользователя.
    get_groups_info(user_id)
        Получает информацию о группах пользователя.
    get_wall_info(user_id, domain)
        Получает информацию о постах на стене пользователя.
    """

    def __init__(self, token):
        """
        Инициализирует сессию VK API с использованием указанного токена.

        Parameters
        ----------
        token : str
            Токен доступа VK API.
        """
        self.session = vk_api.VkApi(token=token)
        self.api = self.session.get_api()

    def get_user_info(self, user_id):
        """
        Получает информацию о пользователе.

        Parameters
        ----------
        user_id : int or str
            Идентификатор пользователя.

        Returns
        -------
        dict or None
            Информация о пользователе, если запрос успешен, иначе None.

        Raises
        ------
        vk_api.ApiError
            Возникает при ошибке API ВКонтакте.
        Exception
            Возникает при других ошибках.
        """
        try:
            return self.api.users.get(user_ids=user_id, fields='domain,sex,bdate,city,country,site,activities,interests,schools,universities')
        except vk_api.ApiError as e:
            print(f'Ошибка API ВКонтакте при запросе информации о пользователе: {e}')
        except Exception as e:
            print(f'Произошла ошибка при запросе информации о пользователе: {e}')

    def get_friends_info(self, user_id):
        """
        Получает информацию о друзьях пользователя.

        Parameters
        ----------
        user_id : int or str
            Идентификатор пользователя.

        Returns
        -------
        dict or None
            Информация о друзьях пользователя, если запрос успешен, иначе None.

        Raises
        ------
        vk_api.ApiError
            Возникает при ошибке API ВКонтакте.
        Exception
            Возникает при других ошибках.
        """
        try:
            return self.api.friends.get(user_id=user_id, fields='sex,bdate,city,country')
        except vk_api.ApiError as e:
            print(f'Ошибка API ВКонтакте при запросе информации о друзьях пользователя: {e}')
        except Exception as e:
            print(f'Произошла ошибка при запросе информации о друзьях пользователя: {e}')

    def get_groups_info(self, user_id):
        """
        Получает информацию о группах пользователя.

        Parameters
        ----------
        user_id : int or str
            Идентификатор пользователя.

        Returns
        -------
        dict or None
            Информация о группах пользователя, если запрос успешен, иначе None.

        Raises
        ------
        vk_api.ApiError
            Возникает при ошибке API ВКонтакте.
        Exception
            Возникает при других ошибках.
        """
        try:
            return self.api.groups.get(user_id=user_id, extended=1, fields='activity,city,country,site')
        except vk_api.ApiError as e:
            print(f'Ошибка API ВКонтакте при запросе информации о сообществах пользователя: {e}')
        except Exception as e:
            print(f'Произошла ошибка при запросе информации о сообществах пользователя: {e}')

    def get_wall_info(self, user_id, domain):
        """
        Получает информацию о постах на стене пользователя.

        Parameters
        ----------
        user_id : int or str
            Идентификатор пользователя.
        domain : str
            Доменное имя пользователя.

        Returns
        -------
        dict or None
            Информация о постах на стене пользователя, если запрос успешен, иначе None.

        Raises
        ------
        vk_api.ApiError
            Возникает при ошибке API ВКонтакте.
        Exception
            Возникает при других ошибках.
        """
        try:
            return self.api.wall.get(user_id=user_id, domain=domain, count=100, filter='all')
        except vk_api.ApiError as e:
            print(f'Ошибка API ВКонтакте при запросе информации о стене пользователя: {e}')
        except Exception as e:
            print(f'Произошла ошибка при запросе информации о стене пользователя: {e}')
