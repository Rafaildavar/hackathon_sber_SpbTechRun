import requests
from typing import List, Dict, Any, Optional
from utils.logger import get_logger

log = get_logger("RetrievalAgentTools")

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"

def get_building_id_by_address(user_address: str):
    try:
        address_search = requests.get(
            f"{geo_api}/geo/buildings/search/",
            params={
                "query": user_address,
                "count": 5,
                "region_of_search": "78"
            },
            headers={"region": "78"},
            timeout=10
        )
        result = address_search.json()
        data = result.get("data", [])

        if not data:
            return None
        return data[0]["id"]
    except Exception as e:
        log.error(f"Ошибка получения building_id: {str(e)}")
        return None

def find_nearest_mfc(user_address: str):
    building_id = get_building_id_by_address(user_address)
    if building_id is None:
        return None

    try:
        mfc_info = requests.get(
            f"{main_api}/mfc/",
            params={"id_building": building_id},
            headers={"region": "78"},
            timeout=10
        )

        if mfc_info.status_code != 200:
            log.error(f"Ошибка получения МФЦ: {mfc_info.status_code}")
            return None

        mfc = mfc_info.json()
        return {
            "name": mfc["name"],
            "address": mfc["address"],
            "metro": mfc["nearest_metro"],
            "phones": mfc["phone"],
            "hours": mfc["working_hours"],
            "coords": mfc["coordinates"],
            "link": mfc["link"],
            "chat_bot": mfc["chat_bot"]
        }
    except Exception as e:
        log.error(f"Ошибка find_nearest_mfc: {str(e)}")
        return None

def get_mfc_by_district(district: str):
    try:
        resp = requests.get(
            f"{main_api}/mfc/district/",
            params={"district": district},
            timeout=10
        )

        if resp.status_code != 200:
            log.error(f"Ошибка получения МФЦ по району: {resp.status_code}")
            return None

        json_data = resp.json()
        items = json_data.get("data", [])

        result = [json_data["count"]]
        for item in items:
            result.append({
                "name": item.get("name"),
                "address": item.get("address"),
                "hours": item.get("working_hours"),
            })
        return result
    except Exception as e:
        log.error(f"Ошибка get_mfc_by_district: {str(e)}")
        return None

def get_polyclinics_by_address(user_address: str):
    building_id = get_building_id_by_address(user_address)
    if building_id is None:
        return None

    try:
        response = requests.get(
            f"{main_api}/polyclinics/",
            params={"id": building_id},
            headers={"region": "78"},
            timeout=10
        )

        if response.status_code != 200:
            log.error(f"Ошибка получения поликлиник: {response.status_code}")
            return None

        polyclinics = response.json()
        result = []
        for clinic in polyclinics:
            result.append({
                "name": clinic.get("clinic_name"),
                "address": clinic.get("clinic_address"),
                "phones": clinic.get("phone", []),
                "url": clinic.get("url"),
            })
        return result
    except Exception as e:
        log.error(f"Ошибка get_polyclinics_by_address: {str(e)}")
        return None

def get_schools_by_district(district: str):
    try:
        resp = requests.get(f"{main_api}/school/map/", timeout=10)

        if resp.status_code != 200:
            log.error(f"Ошибка получения школ: {resp.status_code}")
            return None

        data = resp.json()
        schools = data["data"]

        schools_on_district = [
            s for s in schools
            if s.get("district") == district
        ]
        return schools_on_district
    except Exception as e:
        log.error(f"Ошибка get_schools_by_district: {str(e)}")
        return None

def get_linked_schools(user_address: str):
    building_id = get_building_id_by_address(user_address)
    if building_id is None:
        return None

    try:
        url = requests.get(f"{main_api}/school/linked/{building_id}", timeout=10)

        if url.status_code != 200:
            log.error(f"Ошибка получения привязанных школ: {url.status_code}")
            return None

        return url.json()
    except Exception as e:
        log.error(f"Ошибка get_linked_schools: {str(e)}")
        return None

def get_dou(district: str, age_year: int = 0, age_month: int = 0):
    try:
        params = {
            "district": district,
            "legal_form": "Государственная",
            "age_year": age_year,
            "age_month": age_month,
            "doo_status": "Функционирует",
        }

        resp = requests.get(f"{main_api}/dou/", params=params, timeout=10)

        if resp.status_code != 200:
            log.error(f"Ошибка получения детских садов: {resp.status_code}")
            return None

        return resp.json()
    except Exception as e:
        log.error(f"Ошибка get_dou: {str(e)}")
        return None

def pensioner_service_category():
    try:
        resp = requests.get(f"{main_api}/pensioner/services/category/", timeout=10)

        if resp.status_code != 200:
            log.error(f"Ошибка получения категорий услуг: {resp.status_code}")
            return None

        return resp.json()
    except Exception as e:
        log.error(f"Ошибка pensioner_service_category: {str(e)}")
        return None

def pensioner_service(district: str, category: str = ""):
    try:
        if isinstance(category, (list, tuple, set)):
            category_str = ",".join(str(c).strip() for c in category)
        else:
            category_str = str(category).strip()

        params = {
            "district": district,
            "category": category_str,
            "count": 21,
            "page": 1,
        }

        resp = requests.get(f"{main_api}/pensioner/services/", params=params, timeout=10)

        if resp.status_code != 200:
            log.error(f"Ошибка получения услуг для пенсионеров: {resp.status_code}")
            return None

        return resp.json()
    except Exception as e:
        log.error(f"Ошибка pensioner_service: {str(e)}")
        return None

def afisha_all_category(start_date: str, end_date: str):
    try:
        params = {
            "start_date": start_date,
            "end_date": end_date,
        }

        resp = requests.get(f"{main_api}/afisha/category/all/", params=params, timeout=10)

        if resp.status_code != 200:
            log.error(f"Ошибка получения категорий афиши: {resp.status_code}")
            return None

        return resp.json()
    except Exception as e:
        log.error(f"Ошибка afisha_all_category: {str(e)}")
        return None

def afisha_all(start_date: str, end_date: str, categoria: str = "", kids: bool = None, free: bool = None):
    try:
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "categoria": categoria,
            "kids": kids,
            "free": free,
        }

        resp = requests.get(f"{main_api}/afisha/all/", params=params, timeout=10)

        if resp.status_code != 200:
            log.error(f"Ошибка получения афиши: {resp.status_code}")
            return None

        return resp.json()
    except Exception as e:
        log.error(f"Ошибка afisha_all: {str(e)}")
        return None

def get_beautiful_places_area():
    try:
        resp = requests.get(f"{main_api}/beautiful_places/area/", timeout=10)

        if resp.status_code != 200:
            log.error(f"Ошибка получения областей красивых мест: {resp.status_code}")
            return None

        return resp.json()
    except Exception as e:
        log.error(f"Ошибка get_beautiful_places_area: {str(e)}")
        return None

def get_beautiful_categoria():
    try:
        resp = requests.get(f"{main_api}/beautiful_places/categoria/", timeout=10)

        if resp.status_code != 200:
            log.error(f"Ошибка получения категорий красивых мест: {resp.status_code}")
            return None

        return resp.json()
    except Exception as e:
        log.error(f"Ошибка get_beautiful_categoria: {str(e)}")
        return None

def get_beautiful_places(area: str = None, categoria: str = None, district: str = None):
    try:
        params = {
            "area": area,
            "district": district,
            "categoria": categoria,
        }

        resp = requests.get(f"{main_api}/beautiful_places/", params=params, timeout=10)

        if resp.status_code != 200:
            log.error(f"Ошибка получения красивых мест: {resp.status_code}")
            return None

        return resp.json()
    except Exception as e:
        log.error(f"Ошибка get_beautiful_places: {str(e)}")
        return None