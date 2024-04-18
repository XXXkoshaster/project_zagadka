import vk_api

#класс для поучения информации о профиле пользователя с использованием VK API
class VkProfile:
    def __init__(self, token):
        self.session = vk_api.VkApi(token=token)
        self.api = self.session.get_api()

#метод для получения информации о самом пользователе
    def get_user_info(self, user_id):
        try:
            return self.api.users.get(user_ids=user_id, fields="domain, sex, bdate, city, country, site, activities, interests, schools, universities")
        except vk_api.ApiError as e:
            print(f"Ошибка API вконтакте при запросе информации о пользователе: {e}")
        except Exception as e:
            print(f"Произошла ошибка при запросе информации о пользователе: {e}")
            
#метод для получения информации о друзьях пользователя:
    def get_friends_info(self, user_id):
        try:
            return self.api.friends.get(user_id=user_id, fields="sex, bdate, city, country, site, activities, interests, schools, universities")
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
