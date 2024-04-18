import pandas as pd

def cities_info(friends):
    try:
        cities = dict()

        for i in friends:
            if "city" in i.keys():
                city = i["city"]["title"]
                
                if city not in cities:
                    cities[city] = 1
                else:
                    cities[city] += 1
            else:
                continue
        
        cities = pd.DataFrame(cities.items(), columns=['City', 'Count'])
        return cities
    except Exception as e:
        print(f"Ошибка в обработке города пользователя: {e}")
        return pd.DataFrame(columns=['City', 'Count'])
