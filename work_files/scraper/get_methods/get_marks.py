import pandas as pd


def marks_info(wall):
    """
    Вычисляет суммарное количество лайков, комментариев, просмотров и репостов на стене пользователя.

    Эта функция принимает список постов на стене пользователя и возвращает DataFrame с суммарной статистикой
    по лайкам, комментариям, просмотрам и репостам.

    Parameters
    ----------
    wall : list of dict
        Список словарей, где каждый словарь представляет собой пост на стене пользователя.
        Каждый пост может содержать ключи 'likes', 'comments', 'views' и 'reposts' с информацией о количестве.

    Returns
    -------
    pd.DataFrame
        DataFrame с двумя столбцами: 'stats' (тип метрики) и 'values' (значение метрики).

    Raises
    ------
    Exception
        Возникает при возникновении ошибки в обработке статистики пользователя.
        В случае ошибки функция возвращает пустой DataFrame с колонками ['stats', 'values'].

    Examples
    --------
    >>> wall = [
    ...     {'likes': {'count': 10}, 'comments': {'count': 2}, 'views': {'count': 100}, 'reposts': {'count': 1}},
    ...     {'likes': {'count': 5}, 'comments': {'count': 3}, 'views': {'count': 50}, 'reposts': {'count': 0}},
    ...     {'likes': {'count': 7}, 'comments': {'count': 1}, 'views': {'count': 70}, 'reposts': {'count': 2}}
    ... ]
    >>> marks_info(wall)
         stats  values
    0    likes      22
    1  comments       6
    2     views     220
    3   reposts       3

    Notes
    -----
    Посты без указанных ключей ('likes', 'comments', 'views', 'reposts') не учитываются в расчетах.
    """
    try:
        likes = 0
        comments = 0
        views = 0
        reposts = 0

        for i in wall:
            if 'likes' in i.keys():
                likes += i['likes']['count']

            if 'comments' in i.keys():
                comments += i['comments']['count']

            if 'views' in i.keys():
                views += i['views']['count']

            if 'reposts' in i.keys():
                reposts += i['reposts']['count']

        return pd.DataFrame({'stats': ['likes', 'comments', 'views', 'reposts'], 'values':[likes, comments, views, reposts]})
    except Exception as e:
        print(f'Ошибка в обработке статистики пользователя: {e}')
        return pd.DataFrame(columns=['stats', 'values'])