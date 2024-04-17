import re
from datetime import datetime
import json

class DataProcessor:
    @staticmethod
    def get_user_id(url):
        try:
            match = re.search(r"vk.com/(\w+)", url)
            return match.group(1)
        except Exception as e:
            print(f"Некорректный URL или отсутствует идентификатор пользователя: {e}")

    @staticmethod
    def save_data(file_path, data):
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

    @staticmethod
    def time_convertor(data_wall):
        try:
            date_time = datetime.utcfromtimestamp(data_wall["date"])
            formatted_date = date_time.strftime("%Y-%m-%d %H:%M:%S")
            data_wall["date"] = formatted_date
        except Exception:
            print(f"Отсутствует ключ 'date' в объекте данных")
    
    @staticmethod
    def gender_convertor(data_friends):
        try:
            if data_friends["sex"] == 2:
                data_friends["sex"] = "male"
            elif data_friends["sex"] == 1:
                data_friends["sex"] = "female"
            else:
                data_friends["sex"] = None
        except Exception:
            print(f"Отсутствует ключ 'sex' в объекте данных")
    
    @staticmethod
    def convert_user_data(user_data):
            DataProcessor.gender_convertor(user_data)
    
    @staticmethod
    def convert_friends_data(friends_data):
        for friend in friends_data["items"]:
            DataProcessor.gender_convertor(friend)
    
    @staticmethod
    def convert_wall_data(wall_data):
        for post in wall_data["items"]:
            DataProcessor.time_convertor(post)
