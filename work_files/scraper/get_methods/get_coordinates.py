def coord_info(city, geolocator, cache):
    """
    Получает координаты (широту и долготу) для указанного города.

    Эта функция использует геолокатор для получения координат указанного города. Если координаты города уже
    присутствуют в кэше, они возвращаются из кэша, иначе координаты запрашиваются у геолокатора и сохраняются в кэш.

    Parameters
    ----------
    city : str
        Название города, для которого необходимо получить координаты.
    geolocator : object
        Объект геолокатора, используемый для получения координат. Например, экземпляр `geopy.geocoders`.
    cache : dict
        Словарь кэша для хранения координат городов. Ключом является название города, значением — кортеж (широта, долгота).

    Returns
    -------
    tuple of (float, float) or (None, None)
        Возвращает кортеж из широты и долготы города. Если город не найден, возвращает (None, None).

    Raises
    ------
    Exception
        Возникает при возникновении ошибки в процессе получения координат города. В случае ошибки функция возвращает (None, None).

    Examples
    --------
    >>> from geopy.geocoders import Nominatim
    >>> geolocator = Nominatim(user_agent="geoapiExercises")
    >>> cache = {}
    >>> coord_info("Москва", geolocator, cache)
    (55.755826, 37.6173)
    >>> coord_info("Москва", geolocator, cache)  # Возвращается из кэша
    (55.755826, 37.6173)

    Notes
    -----
    Функция использует кэш для уменьшения количества запросов к геолокатору и повышения производительности.
    """
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
