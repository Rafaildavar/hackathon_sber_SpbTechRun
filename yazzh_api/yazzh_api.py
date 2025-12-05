import requests
from typing import List, Dict, Any

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"

# Определение id здания по адресу (вспомогательная ф)
def get_building_id_by_address(user_address: str):
    address_search = requests.get(
        f"{geo_api}/geo/buildings/search/",
        params={
            "query": user_address,
            "count": 5,
            "region_of_search": "78"
        },
        headers={"region": "78"}
    )

    result = address_search.json()
    data = result.get("data", [])

    if not data:
        return None
    else:
        first_building = data[0]
        building_id = first_building["id"]
        return building_id


# Нахождение МФЦ по адресу пользователя
# входной параметр, например "Невский проспект 1"
def find_nearest_mfc(user_address: str):
    # 1. Найти building_id по адресу
    building_id = get_building_id_by_address(user_address)
    if building_id is None:
        return None

    # 2. Найти МФЦ рядом с домом
    mfc_info = requests.get(
        f"{main_api}/mfc/",
        params={"id_building": building_id},
        headers={"region": "78"}
    )

    if mfc_info.status_code != 200:
        print(f"код ошибки {mfc_info.status_code}")
        return

    mfc = mfc_info.json()
    # ВЫОВОДИМАЯ ИНФОРМАЦИЯ:
    return {
        "name": mfc["name"],
        "address": mfc["address"],
        "metro": mfc["nearest_metro"],
        "phones": mfc["phone"],
        "hours": mfc["working_hours"],
        "coords": mfc["coordinates"],
        "link": mfc["link"],
        "chat_bot": mfc["chat_bot"]}


# Ищет поликлиники по адресу пользователя.
# входной параметр, например "Комендантский проспект 61"
def get_polyclinics_by_address(user_address: str):
    # 1. получаем building_id
    building_id = get_building_id_by_address(user_address)
    if building_id is None:
        return None

    response = requests.get(
        f"{main_api}/polyclinics/",
        params={"id": building_id},
        headers={"region": "78"},
    )

    # Случай, когда по адресу нет поликлиник: 204 No Content
    if response.status_code != 200:
        print(f"код ошибки {response.status_code}")
        return

    polyclinics = response.json()

    # ВЫОВОДИМАЯ ИНФОРМАЦИЯ:
    result = []
    for clinic in polyclinics:
        result.append({
            "name": clinic.get("clinic_name"),
            "address": clinic.get("clinic_address"),
            "phones": clinic.get("phone", []),
            "url": clinic.get("url"),
        })
    return result

# Ищет ближайшую школу по адресу
# входной параметр, например "Комендантский проспект 61"
def get_linked_schools(user_address: str):
    # 1. получаем building_id
    building_id = get_building_id_by_address(user_address)
    if building_id is None:
        return None

    url = requests.get(f"{main_api}/school/linked/{building_id}")

    if url.status_code != 200:
        print(f"код ошибки {url.status_code}")
        return

    data = url.json()
    # ВЫОВОДИМАЯ ИНФОРМАЦИЯ: полная инфа в json
    return data

""" 
в kindergarten.py
# Получить детские сады по фильтрам (район, возраст ребенка в годах, возраст ребенка в месяцах)
# входные параметры, например: district="Приморский", age_year=3
def get_dou(district, age_year: int = 0, age_month: int = 0):
    params = {
        "district": district,
        "legal_form": "Государственная",
        "age_year": age_year,
        "age_month": age_month,
        "doo_status": "Функционирует",
    }

    resp = requests.get(f"{main_api}/dou/", params=params)
    resp.raise_for_status()
    if resp.status_code != 200:
        print(f"код ошибки {resp.status_code}")
        return
    data = resp.json()
    # ВЫОВОДИМАЯ ИНФОРМАЦИЯ: полная инфа в json
    return data
"""
if __name__ == "__main__":
    #Выводит id здания по адресу
    print(get_building_id_by_address("Комендантский проспект 61"))

    mfc_data = find_nearest_mfc("Комендантский проспект 61")
    print(mfc_data)

    result = get_polyclinics_by_address("Комендантский проспект 61")
    #print(result)

    data = get_linked_schools("Комендантский проспект 61")
    #print(data)





