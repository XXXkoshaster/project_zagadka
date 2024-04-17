import os
import dotenv 
import sys
from data_processor import DataProcessor
from vk_profile import VkProfile

#класс создания приложения
class VkApp:
    def __init__(self, url):
        dotenv.load_dotenv()
        self.token = os.getenv("API_KEY")
        self.profile = VkProfile(self.token)
        
        self.user_name = DataProcessor.get_user_id(url)
        self.user_id = self.profile.get_user_info(self.user_name)[0]["id"]
        self.user_domain = self.profile.get_user_info(self.user_name)[0]["domain"]
        
        self.run()

    def run(self): 
        if self.user_id:
            user_data = self.profile.get_user_info(self.user_id)
            friends_data = self.profile.get_friends_info(self.user_id)
            groups_data = self.profile.get_groups_info(self.user_id)
            wall_data = self.profile.get_wall_info(self.user_id, self.user_domain)
            
            DataProcessor.convert_user_data(user_data[0])
            DataProcessor.convert_friends_data(friends_data)    
            DataProcessor.convert_wall_data(wall_data)

            DataProcessor.save_data("user_data.json", user_data[0])
            DataProcessor.save_data("friends_data.json", friends_data["items"])
            DataProcessor.save_data("groups_data.json", groups_data["items"])
            DataProcessor.save_data("wall_data.json", wall_data["items"])

#объединение в общий скрипт
if __name__ == "__main__":
    app = VkApp(sys.argv)
