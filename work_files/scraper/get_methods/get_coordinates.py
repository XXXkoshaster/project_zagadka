def coord_info(city, geolocator, cache):
    try:
        if city in cache:
            return cache[city]
        else:
            location = geolocator.geocode(city)
            if location:
                cache[city] = (location.latitude, location.longitude)
                return cache[city]
            else:
                return None, None
    except Exception as e:
        print(f"Ошибка при получении координат города {city}: {e}")
        return None, None