import pandas as pd 

def interests_info(groups):
    try:    
        interests = dict()

        for i in groups:
            if "activity" in i.keys():
                act = i["activity"]
                if act not in interests:
                    interests[act] = 1
                else:
                    interests[act] += 1

        interests = pd.DataFrame(interests.items(), columns=["Activities", "States"])
        return interests
    except Exception as e:
        print(f"Ошибка в обработке интересов пользователя: {e}")
        return pd.DataFrame(columns=["Activities", "States"])