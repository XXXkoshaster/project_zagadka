import pandas as pd


def interests_info(groups):
    """
    Вычисляет распределение интересов среди групп.

    Эта функция принимает список групп с информацией об их активности и возвращает DataFrame с распределением активностей.

    Parameters
    ----------
    groups : list of dict
        Список словарей, где каждый словарь представляет собой информацию о группе.
        Каждый словарь может содержать ключ 'activity', представляющий тип активности группы.

    Returns
    -------
    pd.DataFrame
        DataFrame с двумя столбцами: 'Activities' (тип активности) и 'States' (количество групп с таким типом активности).

    Raises
    ------
    Exception
        Возникает при возникновении ошибки в обработке информации об интересах пользователя.
        В случае ошибки функция возвращает пустой DataFrame с колонками ['Activities', 'States'].

    Examples
    --------
    >>> groups = [
    ...     {'activity': 'Музыка'},
    ...     {'activity': 'Спорт'},
    ...     {'activity': 'Музыка'},
    ...     {'activity': 'Танцы'},
    ...     {'activity': 'Спорт'}
    ... ]
    >>> interests_info(groups)
      Activities  States
    0      Музыка       2
    1       Спорт       2
    2       Танцы       1

    Notes
    -----
    Группы без указанной информации об активности не учитываются в расчетах.
    """
    try:
        interests = dict()

        for i in groups:
            if 'activity' in i.keys():
                act = i['activity']
                if act not in interests:
                    interests[act] = 1
                else:
                    interests[act] += 1

        interests = pd.DataFrame(interests.items(), columns=['Activities', 'States'])
        return interests
    except Exception as e:
        print(f'Ошибка в обработке интересов пользователя: {e}')
        return pd.DataFrame(columns=['Activities', 'States'])