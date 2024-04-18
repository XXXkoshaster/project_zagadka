import pandas as pd

def toxic_info(wall):
        try:
            toxic = dict()

            for i in wall:
                if "date" in i.keys():
                    date = i["date"][:7]
                    if date not in toxic:
                        toxic[date] = 1
                    else: 
                        toxic[date] += 1

            return pd.DataFrame(toxic.items(), columns=['Mounth', 'Count posts'])
        except Exception as e:
            print(f"Ошибка в обработке токсичности пользователя: {e}")
            return pd.DataFrame(lumns=['Mounth', 'Count posts'])