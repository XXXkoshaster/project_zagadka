from datetime import datetime

import pandas as pd


def ages_info(friends):
    """
    Вычисляет распределение возрастов друзей.

    Эта функция принимает список друзей с их днями рождения и возвращает DataFrame с распределением возрастов,
    исключая нереалистичные данные (возраст менее 5 и более 90 лет).

    Parameters
    ----------
    friends : list of dict
        Список словарей, где каждый словарь представляет собой профиль друга.
        Каждый профиль может содержать ключ 'bdate' с датой рождения в формате 'дд.мм.гггг'.

    Returns
    -------
    pd.DataFrame
        DataFrame с двумя столбцами: 'Age' (возраст) и 'Count' (количество друзей данного возраста).

    Raises
    ------
    Exception
        Возникает при возникновении ошибки в обработке возраста пользователя.
        В случае ошибки функция возвращает пустой DataFrame с колонками ['Age', 'Count'].

    Examples
    --------
    >>> friends = [
    ...     {'bdate': '12.04.1990'},
    ...     {'bdate': '05.06.1985'},
    ...     {'bdate': '01.01.1970'},
    ...     {'bdate': '13.12.2005'}
    ... ]
    >>> ages_info(friends)
       Age  Count
    0   31      1
    1   36      1
    2   51      1
    3   16      1

    Notes
    -----
    Друзья без указанной даты рождения или с неполной датой (без года) не учитываются в расчетах.
    """
    try:
        ages = dict()

        for i in friends:
            if "bdate" in i.keys():
                year = i["bdate"].split(".")
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

        ages = pd.DataFrame(ages.items(), columns=["Age", "Count"])

        return ages[(ages["Age"] > 5) & (ages["Age"] < 90)]
    except Exception as e:
        print(f"Ошибка в обработке возраста пользователя: {e}")
        return pd.DataFrame(columns=["Age", "Count"])
