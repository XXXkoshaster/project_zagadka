import vk_api
import json
import os
from dotenv import load_dotenv
import re
from datetime import datetime
import sys

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

#метод для получения информации о самом пользователе
    def get_user_info(self, user_id):
        try:
            return self.api.users.get(user_ids=user_id, fields="domain, sex, bdate, city, country, site, contacts, activities, interests, career, schools, universities, occupation, movies, music, books, tv, relatives")
        except vk_api.ApiError as e:
            print(f"Ошибка API вконтакте при запросе информации о пользователе: {e}")
        except Exception as e:
            print(f"Произошла ошибка при запросе информации о пользователе: {e}")

#метод для получения информации о друзьях пользователя:
    def get_friends_info(self, user_id):
        try:
            return self.api.friends.get(user_id=user_id, fields="sex, bdate, city, country, site, contacts, activities, interests, career, schools, universities, occupation, movies, music, books, tv, relatives")
        except vk_api.ApiError as e:
            print(f"Ошибка API вконтакте при запросе информации о друзьх пользователя: {e}")
        except Exception as e:
            print(f"Произошла ошибка при запросе информации о друзьх пользователя: {e}")

#метод для получения информации о друзьях пользователя
    def get_groups_info(self, user_id):
        try:
            return self.api.groups.get(user_id=user_id, extended=1, fields="activity, city, country, site")
        except vk_api.ApiError as e:
            print(f"Ошибка API вконтакте при запросе информации о сообщестах пользователя: {e}")
        except Exception as e:
            print(f"Произошла ошибка при запросе информации о сообществах пользователя: {e}")

#метод для получения информации о друзьях пользователя
    def get_wall_info(self, user_id, domain):
        try:
            return self.api.wall.get(user_id=user_id, domain=domain, count=100, filter=all)
        except vk_api.ApiError as e:
            print(f"Ошибка API вконтакте при запросе информации о стене пользователя: {e}")
        except Exception as e:
            print(f"Произошла ошибка при запросе информации о стене пользователя: {e}")

#класс для сохранения инфромации о пользователе в файл json
class File:
    @staticmethod
    def save_data(file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


#класс создания приложения
class VkApp:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("API_KEY")
        self.profile = VkProfile(self.token)

    def time_convertor(self, object):
        date_time = datetime.utcfromtimestamp(object["date"])
        formatted_date = date_time.strftime('%Y-%m-%d %H:%M:%S')
        object["date"] = formatted_date

    def sex_convertor(self, object):
        if object["sex"] == 2:
            object["sex"] = "male"
        elif object["sex"] == 1:
            object["sex"] = "female"
        else:
            object["sex"] = None

    def run(self):
        url = sys.argv[1]
        user_name = ID.get_user_id(url)
        user_id = self.profile.get_user_info(user_name)[0]["id"]
        user_domain = self.profile.get_user_info(user_name)[0]["domain"]
        
        if user_id:
            user_data = self.profile.get_user_info(user_id)
            friends_data = self.profile.get_friends_info(user_id)
            groups_data = self.profile.get_groups_info(user_id)
            wall_data = self.profile.get_wall_info(user_id, user_domain)
            
            user_data[0]["URL"] = url
            
            #
            self.sex_convertor(user_data[0])
            for i in friends_data["items"]:
                self.sex_convertor(i)
            #
    
            for i in wall_data["items"]:
                self.time_convertor(i)

            File.save_data("user_data.json", user_data[0])
            File.save_data("friends_data.json", friends_data["items"])
            File.save_data("groups_data.json", groups_data["items"])
            File.save_data("wall_data.json", wall_data["items"])

#объединение в общий скрипт
if __name__ == "__main__":
    app = VkApp()
    app.run()