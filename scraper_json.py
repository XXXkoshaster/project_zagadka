import pandas as pd
from datetime import datetime
from geopy.geocoders import Nominatim

class UserProfileParser:
    def __init__(self):
        self.cache = {}  
        self.geolocator = Nominatim(user_agent="your_app_name")  

    def get_user_info(self, data):
        try:
            data_general = pd.Series(data, index=["id", "domain", "first_name", "last_name", "sex", "bdate"])
        except Exception as e:
            print(f"Ошибка в обработке общей информации пользователя: {e}")
            data_general =  pd.Series()
        
        try:
            data_country = pd.Series(data["country"]["title"], index=["country"])
        except Exception as e:
            print(f"Ошибка в обработке информации о стране пользователя: {e}")
            data_country =  pd.Series()

        try:
            data_city = pd.Series(data["city"]["title"], index=["city"])
        except Exception as e:
            print(f"Ошибка в обработке информации о городе пользователя: {e}")
            data_city =  pd.Series()
        
        data_univer = pd.Series()
        data_schools = pd.Series()

        try:
            for i in data.get("universities", []):
                tmp = pd.Series(i, index=["name", "faculty_name", "chair_name", "graduation"])
                tmp["faculty_name"] = tmp["faculty_name"].rstrip()
                tmp.rename(index={"name": "university"}, inplace=True)
                data_univer = pd.concat([data_univer, tmp])
        except Exception as e:
            print(f"Ошибка в обработке информации о университете пользователя: {e}")

        try:
            for i in data.get("schools", []):
                tmp = pd.Series(i, index=["name", "class", "speciality", "year_from", "year_to"])
                
                if "колледж" in i.get("name", "").lower():
                    tmp.rename(index={"name": "kollage"}, inplace=True)
                else:
                    tmp.rename(index={"name": "school"}, inplace=True)

                data_schools = pd.concat([data_schools, tmp])
        except Exception as e:
            print(f"Ошибка в обработке информации о школе пользователя {e}")

        try:
            data_schools = data_schools[data_schools.notna()]
            seria = pd.concat([data_general, data_country, data_city, data_schools, data_univer])
        except Exception as e:
            print(f"Ошибка в обработке финальной даты: {e}")
            seria = pd.Series()

        return seria.to_frame(name='values').T

    def get_ages_friends(self, friends):
        try:
            ages = dict()

            for i in friends:
                if "bdate" in i.keys():
                    year = i["bdate"].split('.')
                    if len(year) == 3:
                        age = datetime.now().year - int(year[2]) 
                        if age not in ages:
                            ages[age] = 1
                        else: 
                            ages[age] += 1
                    else:
                        continue
                else:
                    continue
        
            ages = pd.DataFrame(ages.items(),columns=['Age', 'Count'])
            
            return ages[(ages['Age'] > 5) & (ages['Age'] < 90)]
        except Exception as e:
            print(f"Ошибка в обработке возраста пользователя: {e}")
            return pd.DataFrame(columns=['Age', 'Count'])
        
    def get_genders_friends(self, friends):
        try:
            genders = dict()

            for i in friends:
                sex = i["sex"]
                if sex:
                    if sex not in genders:
                        genders[sex] = 1
                    else:
                        genders[sex] += 1
                else:
                    continue

            return genders 
        except Exception as e:
            print(f"Ошибка в обработке пола пользователя: {e}")
            return dict()

    def get_cities_friends(self, friends):    
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

    def get_toxic(self, wall):
        try:
            toxic = dict()

            for i in wall:
                date = i["date"][:7]
                if date not in toxic:
                    toxic[date] = 1
                else: 
                    toxic[date] += 1

            return pd.DataFrame(toxic.items(), columns=['Mounth', 'Count posts'])
        except Exception as e:
            print(f"Ошибка в обработке токсичности пользователя: {e}")
            return pd.DataFrame(lumns=['Mounth', 'Count posts'])

    def get_coordinates(self, city):
        if city in self.cache:
            return self.cache[city]
            
        else:
            location = self.geolocator.geocode(city)
            if location:
                self.cache[city] = (location.latitude, location.longitude)
                return self.cache[city]
            else:
                return None, None

    def get_marks(self, wall):
        try:
            likes = 0
            comments = 0
            views = 0
            reposts = 0

            for i in wall:
                likes += i["likes"]["count"]
                comments += i["comments"]["count"]
                views += i["views"]["count"]
                reposts += i["reposts"]["count"]

            return pd.DataFrame({'stats': ['likes', 'comments', 'views', 'reposts'], 'values':[likes, comments, views, reposts]})
        except Exception as e:
            print(f"Ошибка в обработке статистики пользователя: {e}")
            return pd.DataFrame(columns=['stats', 'values'])
        
    def get_interests(self, groups):
        try:    
            interests = dict()

            for i in groups:
                act = i["activity"]
                if act not in interests:
                    interests[act] = 1
                else:
                    interests[act] += 1

            interests = pd.DataFrame(interests.items(), columns=["Activities", "States"])
            return interests
        except Exception as e:
            print(f"Ошибка в обработке интересов пользователя: {e}")
            return pd.DataFrame(columns=["Activities", "States"])