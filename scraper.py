import vk_api
import json
import os
from dotenv import load_dotenv
import re

#класс для получения ID пользователя. Класс обрабатывает введенный URL и извлекает из него ID при помощи регулярных выражений 
class ID:
    @staticmethod
    def extract_user_id(url):
        match = re.search(r"vk.com/(\w+)", url)
        if not match:
            print("Некорректный URL.")
            return None
        return match.group(1)

#класс для поучения информации о профиле пользователя с использованием VK API
class VkProfile:
    def __init__(self, token):
        self.session = vk_api.VkApi(token=token)
        self.api = self.session.get_api()

    def get_usser_info(self, user_id):
        try:
            return self.api.users.get(user_ids=user_id, fields="bdate, city, country")
        except vk_api.ApiError as e:
            print(f"Ошибка API вконтакте: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

#класс для сохранения инфромации о пользователе в файл json
class File:
    @staticmethod
    def save_data(file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file)


#класс создания приложения
class VkApp:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("API_KEY")
        self.vk = VkProfile(self.token)

    def run(self):
        url = input("Введите URL профиль Вконтакте: ")
        user_id = ID.extract_user_id(url)

        if user_id:
            response = self.vk.get_usser_info(user_id)
            if response:
                response[0]["URL"] = url
                File.save_data("data.json", response[0])


#объединение в общий скрипт
if __name__ == "__main__":
    app = VkApp()
    app.run()