import pandas as pd

def user_info(data):
    try:
        data_general = pd.Series(data, index=["id", "domain", "first_name", "last_name", "sex", "bdate"])
    except Exception as e:
        print(f"Ошибка в обработке общей информации пользователя: {e}")
        data_general =  pd.Series()
    
    try:
        data_country = pd.Series(data["country"]["title"], index=["country"])
    except Exception as e:
        print(f"Ошибка в обработке информации о стране пользователя: {e}")
        data_country =  pd.Series()

    try:
        data_city = pd.Series(data["city"]["title"], index=["city"])
    except Exception as e:
        print(f"Ошибка в обработке информации о городе пользователя: {e}")
        data_city =  pd.Series()
    
    data_univer = pd.Series()
    data_schools = pd.Series()

    try:
        for i in data.get("universities", []):
            tmp = pd.Series(i, index=["name", "faculty_name", "chair_name", "graduation"])
            
            if "faculty_name" in i.keys():
                tmp["faculty_name"] = tmp["faculty_name"].rstrip()
            
            tmp.rename(index={"name": "university"}, inplace=True)
            data_univer = pd.concat([data_univer, tmp])
    except Exception as e:
        print(f"Ошибка в обработке информации о университете пользователя: {e}")

    try:
        for i in data.get("schools", []):
            tmp = pd.Series(i, index=["name", "class", "speciality", "year_from", "year_to"])
            
            if "колледж" in i.get("name", "").lower():
                tmp.rename(index={"name": "kollage"}, inplace=True)
            else:
                tmp.rename(index={"name": "school"}, inplace=True)

            data_schools = pd.concat([data_schools, tmp])
    except Exception as e:
        print(f"Ошибка в обработке информации о школе пользователя {e}")

    try:
        data_schools = data_schools[data_schools.notna()]
        seria = pd.concat([data_general, data_country, data_city, data_schools, data_univer])
        return seria.to_frame(name='values').reset_index()
    except Exception as e:
        print(f"Ошибка в обработке финальной даты: {e}")
        return pd.DataFrame(columns=['index', 'values'])