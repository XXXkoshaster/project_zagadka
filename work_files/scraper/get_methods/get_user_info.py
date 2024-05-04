import pandas as pd


def user_info(data):
    records = []

    keys = ["id", "domain", "first_name", "last_name", "sex", "bdate"]
    for key in keys:
        value = data.get(key, "Не указано")
        records.append((key, value))

    country = data.get("country", {}).get("title", "Не указано")
    city = data.get("city", {}).get("title", "Не указано")
    records.append(("country", country))
    records.append(("city", city))

    for uni in data.get("universities", []):
        records.append(("university", uni.get("name", "Не указано").strip()))
        records.append(("faculty_name", uni.get("faculty_name", "Не указано").strip()))
        records.append(("chair_name", uni.get("chair_name", "Не указано").strip()))
        records.append(("graduation", uni.get("graduation", "Не указано")))

    for school in data.get("schools", []):
        school_name = school.get("name", "Не указано").strip()
        if "колледж" in school_name.lower():
            school_name = "college"
        records.append(("school", school_name))
        records.append(("class", school.get("class", "Не указано")))
        records.append(("speciality", school.get("speciality", "Не указано")))
        records.append(("year_from", school.get("year_from", "Не указано")))
        records.append(("year_to", school.get("year_to", "Не указано")))

    df = pd.DataFrame(records, columns=["index", "values"])
    return df
