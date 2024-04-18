import pandas as pd
from geopy.geocoders import Nominatim
from get_user_info import user_info
from get_ages_friends import ages_info
from get_genders_friends import geenders_info
from get_cities_friends import cities_info
from get_toxic import toxic_info
from get_coordinates import coord_info
from get_marks import marks_info
from get_interests import interests_info

class UserProfileParser:
    def __init__(self):
        self.cache = {}  
        self.geolocator = Nominatim(user_agent="geoapiExercises")  

    def get_user_info(self, data):
        return user_info(data)

    def get_ages_friends(self, friends):
        return ages_info(friends)
        
    def get_genders_friends(self, friends):
        return geenders_info(friends)

    def get_cities_friends(self, friends):    
        return cities_info(friends)

    def get_toxic(self, wall):
        return toxic_info(wall)
    
    def get_coordinates(self, city):
        return coord_info(city, self.geolocator, self.cache)

    def get_marks(self, wall):
        return marks_info(wall)
    
    def get_interests(self, groups):
        return interests_info(groups)