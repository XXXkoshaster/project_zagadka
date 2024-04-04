import vk_api
import json
import os
from dotenv import load_dotenv
import re

#класс для получения ID пользователя. Класс обрабатывает введенный URL и извлекает из него ID при помощи регулярных выражений 
class ID:
    @staticmethod
    def get_user_id(url):
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

#подкласс VkProfile для получения информации о самом пользователе
class VkUser(VkProfile):
    def get_user_info(self, user_id):
        try:
            return self.api.users.get(user_ids=user_id, fields="sex, bdate, city, country")
        except vk_api.ApiError as e:
            print(f"Ошибка API вконтакте при запросе информации о пользователе: {e}")
        except Exception as e:
            print(f"Произошла ошибка при запросе информации о пользователе: {e}")

#подкласс VkProfile для получения информации о друзьях пользователя
class VkFriends(VkProfile):
    def get_friends_info(self, user_id):
        try:
            return self.api.friends.get(user_id=user_id, fields="sex, bdate, city, country")
        except vk_api.ApiError as e:
            print(f"Ошибка API вконтакте при запросе информации о друзьх пользователя: {e}")
        except Exception as e:
            print(f"Произошла ошибка при запросе информации о друзьх пользователя: {e}")

#подкласс VkProfile для получения информации о друзьях пользователя
class VkGroups(VkProfile):
    def get_groups_info(self, user_id):
        try:
            return self.api.groups.get(user_id=user_id, extended=1, fields="activity, city, country")
        except vk_api.ApiError as e:
            print(f"Ошибка API вконтакте при запросе информации о сообщестах пользователя: {e}")
        except Exception as e:
            print(f"Произошла ошибка при запросе информации о сообществах пользователя: {e}")

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
        self.user = VkUser(self.token)
        self.friends = VkFriends(self.token)
        self.groups = VkGroups(self.token)

    def run(self):
        url = input("Введите URL профиль Вконтакте: ")
        user_name = ID.get_user_id(url)
        user_id = self.user.get_user_info(user_name)[0]["id"]

        if user_id:
            user_data = self.user.get_user_info(user_id)
            friends_data = self.friends.get_friends_info(user_id)
            groups_data = self.groups.get_groups_info(user_id)
            user_data[0]["URL"] = url
            File.save_data("user_data.json", user_data[0])
            File.save_data("friends_data.json", friends_data["items"])
            File.save_data("groups_data.json", groups_data)

#объединение в общий скрипт
if __name__ == "__main__":
    app = VkApp()
    app.run()