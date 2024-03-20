import vk_api
import json
import os
from dotenv import load_dotenv
import re 

#
load_dotenv()

TOKEN = os.getenv('API_KEY')
#

#
URL = input("Введите URL профиль Вконтакте: ")

match = re.search(r'vk.com/(\w+)', URL)
if not match:
    print("Некорректный URL.")
    exit()
    
ID = match.group(1)
#

def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    
    try:
        response = vk.users.get(user_ids=ID, fields='bdate, city, country')
    except vk_api.ApiError as e:
        print(f"Ошибка API вконтакте: {e}")
        return
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return
    
    if response:
        with open('data.json', 'w') as data:
            json.dump(response, data)

if __name__ == '__main__':
    main()