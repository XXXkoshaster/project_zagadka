import pandas as pd


def stat_info(wall):
    """
    Вычисляет количество постов на стене пользователя по месяцам.

    Эта функция принимает список постов на стене пользователя и возвращает DataFrame с количеством постов,
    сгруппированных по месяцам.

    Parameters
    ----------
    wall : list of dict
        Список словарей, где каждый словарь представляет собой пост на стене пользователя.
        Каждый пост должен содержать ключ 'date' с датой в формате 'YYYY-MM-DD'.

    Returns
    -------
    pd.DataFrame
        DataFrame с двумя столбцами: 'Month' (месяц) и 'Count posts' (количество постов за этот месяц).

    Raises
    ------
    Exception
        Возникает при возникновении ошибки в обработке статистики пользователя.
        В случае ошибки функция возвращает пустой DataFrame с колонками ['Month', 'Count posts'].

    Examples
    --------
    >>> wall = [
    ...     {'date': '2021-05-01'},
    ...     {'date': '2021-05-15'},
    ...     {'date': '2021-06-01'},
    ...     {'date': '2021-06-20'},
    ...     {'date': '2021-07-05'}
    ... ]
    >>> stat_info(wall)
         Month  Count posts
    0  2021-05            2
    1  2021-06            2
    2  2021-07            1

    Notes
    -----
    Посты без указанного ключа 'date' не учитываются в расчетах.
    """
    try:
        posts = dict()

        for i in wall:
            if "date" in i.keys():
                date = i["date"][:7]
                if date not in posts:
                    posts[date] = 1
                else:
                    posts[date] += 1

        return pd.DataFrame(posts.items(), columns=["Mounth", "Count posts"])
    except Exception as e:
        print(f"Ошибка в обработке cтатистики пользователя: {e}")
        return pd.DataFrame(lumns=["Mounth", "Count posts"])
