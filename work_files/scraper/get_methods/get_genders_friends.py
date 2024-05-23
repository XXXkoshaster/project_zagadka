import pandas as pd


def geenders_info(friends):
    """
    Вычисляет распределение полов среди друзей.

    Эта функция принимает список друзей с информацией о поле и возвращает DataFrame с распределением полов.

    Parameters
    ----------
    friends : list of dict
        Список словарей, где каждый словарь представляет собой профиль друга.
        Каждый профиль может содержать ключ 'sex' с числовым значением, представляющим пол (1 - женский, 2 - мужской).

    Returns
    -------
    pd.DataFrame
        DataFrame с двумя столбцами: 'Sex' (пол) и 'Count' (количество друзей данного пола).

    Raises
    ------
    Exception
        Возникает при возникновении ошибки в обработке информации о поле пользователя.
        В случае ошибки функция возвращает пустой DataFrame с колонками ['Sex', 'Count'].

    Examples
    --------
    >>> friends = [
    ...     {'sex': 1},
    ...     {'sex': 2},
    ...     {'sex': 2},
    ...     {'sex': 1},
    ...     {'sex': 1}
    ... ]
    >>> geenders_info(friends)
       Sex  Count
    0    1      3
    1    2      2

    Notes
    -----
    Друзья без указанной информации о поле не учитываются в расчетах.
    """
    try:
        genders = dict()

        for i in friends:
            if 'sex' in i.keys():
                sex = i['sex']
                if sex:
                    if sex not in genders:
                        genders[sex] = 1
                    else:
                        genders[sex] += 1
                else:
                    continue

        genders = pd.DataFrame(genders.items(), columns=['Sex', 'Count'])

        return genders
    except Exception as e:
        print(f'Ошибка в обработке пола пользователя: {e}')
        return dict()
