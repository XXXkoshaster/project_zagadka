import pandas as pd


def user_info(data):
    """
    Извлекает информацию о пользователе и возвращает её в виде DataFrame.

    Эта функция принимает словарь с данными о пользователе и извлекает основные поля, такие как идентификатор,
    имя, фамилия, пол, дата рождения, страна, город, университеты и школы. Возвращает DataFrame с извлеченной информацией.

    Parameters
    ----------
    data : dict
        Словарь с данными о пользователе. Может содержать ключи 'id', 'domain', 'first_name', 'last_name', 'sex', 'bdate',
        'country', 'city', 'universities' и 'schools'.

    Returns
    -------
    pd.DataFrame
        DataFrame с двумя столбцами: 'index' (название параметра) и 'values' (значение параметра).

    Examples
    --------
    >>> data = {
    ...     'id': 123,
    ...     'domain': 'example',
    ...     'first_name': 'Иван',
    ...     'last_name': 'Иванов',
    ...     'sex': 2,
    ...     'bdate': '01.01.1990',
    ...     'country': {'title': 'Россия'},
    ...     'city': {'title': 'Москва'},
    ...     'universities': [{'name': 'МГУ', 'faculty_name': 'Физфак', 'chair_name': 'Кафедра физики', 'graduation': 2012}],
    ...     'schools': [{'name': 'Школа №1', 'class': '11A', 'speciality': 'физ-мат', 'year_from': 2000, 'year_to': 2009}]
    ... }
    >>> user_info(data)
              index        values
    0             id           123
    1         domain       example
    2     first_name          Иван
    3      last_name        Иванов
    4            sex             2
    5          bdate    01.01.1990
    6        country        Россия
    7           city        Москва
    8      university           МГУ
    9   faculty_name       Физфак
    10   chair_name  Кафедра физики
    11    graduation          2012
    12         school      Школа №1
    13          class          11A
    14     speciality      физ-мат
    15      year_from          2000
    16        year_to          2009

    Notes
    -----
    Поля, которые отсутствуют в словаре данных, получают значение 'Не указано'.
    """
    records = []

    keys = ['id', 'domain', 'first_name', 'last_name', 'sex', 'bdate']
    for key in keys:
        value = data.get(key, 'Не указано')
        records.append((key, value))

    country = data.get('country', {}).get('title', 'Не указано')
    city = data.get('city', {}).get('title', 'Не указано')
    records.append(('country', country))
    records.append(('city', city))

    for uni in data.get('universities', []):
        records.append(('university', uni.get('name', 'Не указано').strip()))
        records.append(('faculty_name', uni.get('faculty_name', 'Не указано').strip()))
        records.append(('chair_name', uni.get('chair_name', 'Не указано').strip()))
        records.append(('graduation', uni.get('graduation', 'Не указано')))

    for school in data.get('schools', []):
        school_name = school.get('name', 'Не указано').strip()
        if 'колледж' in school_name.lower():
            school_name = 'college'
        records.append(('school', school_name))
        records.append(('class', school.get('class', 'Не указано')))
        records.append(('speciality', school.get('speciality', 'Не указано')))
        records.append(('year_from', school.get('year_from', 'Не указано')))
        records.append(('year_to', school.get('year_to', 'Не указано')))

    df = pd.DataFrame(records, columns=['index', 'values'])
    return df
