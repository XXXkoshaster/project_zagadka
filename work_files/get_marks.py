import pandas as pd

def marks_info(wall):
    try:
        likes = 0
        comments = 0
        views = 0
        reposts = 0

        for i in wall:
            if "likes" in i.keys(): 
                likes += i["likes"]["count"]

            if "comments" in i.keys():   
                comments += i["comments"]["count"]
            
            if "views" in i.keys():
                views += i["views"]["count"]

            if "reposts" in i.keys():
                reposts += i["reposts"]["count"]

        return pd.DataFrame({'stats': ['likes', 'comments', 'views', 'reposts'], 'values':[likes, comments, views, reposts]})
    except Exception as e:
        print(f"Ошибка в обработке статистики пользователя: {e}")
        return pd.DataFrame(columns=['stats', 'values'])