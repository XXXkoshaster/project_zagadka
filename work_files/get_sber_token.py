import dotenv
import requests
import uuid
import os

class GigaChatToken:
    """
    Класс для получения токена доступа к GigaChat API.

    Attributes
    ----------
    api_key : str
        API ключ для доступа к GigaChat API.
    """

    def __init__(self):
        """
        Инициализация класса GigaChatToken.
        Загружает переменные окружения и устанавливает API ключ.
        """
        dotenv.load_dotenv()
        self.api_key = os.getenv('API_KEY_GIGA_CHAT')

    def get_token(self, auth_token, scope='GIGACHAT_API_PERS'):
        """
        Выполняет POST-запрос к эндпоинту для получения токена.

        Parameters
        ----------
        auth_token : str
            Токен авторизации, необходимый для запроса.
        scope : str, optional
            Область действия запроса API. По умолчанию — «GIGACHAT_API_PERS».

        Returns
        -------
        dict or None
            Ответ API в формате словаря, содержащий токен и срок его действия, или None в случае ошибки.
        """
        rq_uid = str(uuid.uuid4())

        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': rq_uid,
            'Authorization': f'Basic {auth_token}'
        }

        payload = {
            'scope': scope
        }

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка: {str(e)}")
            return None

    def return_token(self):
        """
        Возвращает токен доступа, используя API ключ из переменных окружения.

        Returns
        -------
        str or None
            Токен доступа или None в случае ошибки.
        """
        if not self.api_key:
            print("API_KEY_GIGA_CHAT не найден в переменных окружения.")
            return None
        else:
            token_response = self.get_token(self.api_key)
            if token_response:
                giga_token = token_response.get('access_token')
                if giga_token:
                    return giga_token
                else:
                    print("Не удалось получить access_token из ответа API.")
                    return None
            else:
                print("Не удалось получить ответ от API.")
                return None
