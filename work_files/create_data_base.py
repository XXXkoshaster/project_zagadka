import os
import dotenv
import sys
from scraper.data_processor import DataProcessor
from scraper.take_profile_info import VkProfile

class VkApp:
    """
    Класс для получения и обработки данных профиля пользователя ВКонтакте.

    Attributes
    ----------
    token : str
        Токен доступа VK API.
    profile : VkProfile
        Экземпляр класса VkProfile для взаимодействия с VK API.
    user_name : str
        Имя пользователя, извлеченное из URL.
    user_id : int
        Идентификатор пользователя.
    user_domain : str
        Доменное имя пользователя.

    Methods
    -------
    run()
        Получает и обрабатывает данные профиля пользователя.
    """

    def __init__(self, url):
        """
        Инициализирует VkApp с указанным URL профиля пользователя ВКонтакте.

        Parameters
        ----------
        url : str
            URL профиля пользователя ВКонтакте.
        """
        dotenv.load_dotenv()
        self.token = os.getenv('API_KEY')
        self.profile = VkProfile(self.token)

        self.user_name = DataProcessor.get_user_id(url)
        self.user_id = self.profile.get_user_info(self.user_name)[0]['id']
        self.user_domain = self.profile.get_user_info(self.user_name)[0]['domain']

        self.run()

    def run(self):
        """
        Получает и обрабатывает данные профиля пользователя.

        Получает данные профиля, друзей, групп и стены пользователя. Затем обрабатывает эти данные
        и сохраняет их в файлы JSON.
        """
        if self.user_id:
            user_data = self.profile.get_user_info(self.user_id)
            friends_data = self.profile.get_friends_info(self.user_id)
            groups_data = self.profile.get_groups_info(self.user_id)
            wall_data = self.profile.get_wall_info(self.user_id, self.user_domain)

            DataProcessor.convert_user_data(user_data[0])
            DataProcessor.convert_friends_data(friends_data)
            DataProcessor.convert_wall_data(wall_data)

            DataProcessor.save_data('/home/xxxkoshaster/Documents/Zagadka/work_files/data_base/user_data.json', user_data[0])
            DataProcessor.save_data('/home/xxxkoshaster/Documents/Zagadka/work_files/data_base/friends_data.json', friends_data['items'])
            DataProcessor.save_data('/home/xxxkoshaster/Documents/Zagadka/work_files/data_base/groups_data.json', groups_data['items'])
            DataProcessor.save_data('/home/xxxkoshaster/Documents/Zagadka/work_files/data_base/wall_data.json', wall_data['items'])

# объединение в общий скрипт
if __name__ == '__main__':
    app = VkApp(sys.argv[1])
