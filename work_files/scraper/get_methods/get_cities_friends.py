import pandas as pd


def cities_info(friends):
    """
    Вычисляет распределение городов, в которых живут друзья.

    Эта функция принимает список друзей с информацией о городах и возвращает DataFrame с распределением городов,
    где живут друзья.

    Parameters
    ----------
    friends : list of dict
        Список словарей, где каждый словарь представляет собой профиль друга.
        Каждый профиль может содержать ключ 'city' с вложенным словарем, содержащим ключ 'title' (название города).

    Returns
    -------
    pd.DataFrame
        DataFrame с двумя столбцами: 'City' (город) и 'Count' (количество друзей в этом городе).

    Raises
    ------
    Exception
        Возникает при возникновении ошибки в обработке информации о городах пользователя.
        В случае ошибки функция возвращает пустой DataFrame с колонками ['City', 'Count'].

    Examples
    --------
    >>> friends = [
    ...     {'city': {'title': 'Москва'}},
    ...     {'city': {'title': 'Санкт-Петербург'}},
    ...     {'city': {'title': 'Москва'}},
    ...     {'city': {'title': 'Новосибирск'}}
    ... ]
    >>> cities_info(friends)
                City  Count
    0         Москва      2
    1  Санкт-Петербург    1
    2    Новосибирск      1

    Notes
    -----
    Друзья без указанной информации о городе не учитываются в расчетах.
    """
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

        cities = pd.DataFrame(cities.items(), columns=["City", "Count"])
        return cities
    except Exception as e:
        print(f"Ошибка в обработке города пользователя: {e}")
        return pd.DataFrame(columns=["City", "Count"])
