def geenders_info(friends): 
    try:
        genders = dict()

        for i in friends:
            if "sex" in i.keys():    
                sex = i["sex"]
                if sex:
                    if sex not in genders:
                        genders[sex] = 1
                    else:
                        genders[sex] += 1
                else:
                    continue

        return genders 
    except Exception as e:
        print(f"Ошибка в обработке пола пользователя: {e}")
        return dict()
