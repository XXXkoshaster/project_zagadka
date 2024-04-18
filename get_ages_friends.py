import pandas as pd
from datetime import datetime

def ages_info(friends):    
    try:
        ages = dict()

        for i in friends:
            if "bdate" in i.keys():
                year = i["bdate"].split('.')
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
    
        ages = pd.DataFrame(ages.items(),columns=['Age', 'Count'])
        
        return ages[(ages['Age'] > 5) & (ages['Age'] < 90)]
    except Exception as e:
        print(f"Ошибка в обработке возраста пользователя: {e}")
        return pd.DataFrame(columns=['Age', 'Count'])   