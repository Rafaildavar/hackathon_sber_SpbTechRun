#Раздел мой питомец (ЭГС) из "https://yazzh.gate.petersburg.ru"
from typing import Optional, List, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"

class MyPetsEGSAPIError(Exception):
    pass

"""
Поиск клиник в заданном радиусе от координат и по перечню услуг.
:srevices: Услуги: Прием и осмотр животных, Акушерство и гинекология, Анестезия, 
           Вакцинация (госуслуга), Вакцинация (платная), Выдача ВСД на животных, 
           Вызов врача на дом, Дерматология, КТ, Кардиология, Клинико-диагностическая лаборатория, 
           Косметические операции, Круглосуточный стационар, Онкология, Ортопедия, 
           Офтальмология, Прием и осмотр животных, Рентген, Стерилизация / кастрация, 
           Стоматология, Терапия, УЗИ, Физиотерапия, Функциональная диагностика, Хирургия, 
           Чипирование, ЭКГ, ЭХО-КГ, Эвтаназия, Эндоскопия, Энцефалография
входные параметры: можно оставить без фильтров
"""

def get_mypets_clinics(
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    services: Optional[List[str]] = None ) -> Dict[str, Any]:

    params: Dict[str, Any] = {
        "location_latitude": location_latitude,
        "location_longitude": location_longitude,
        "location_radius": location_radius,
        "services": services
    }

    params = {k: v for k, v in params.items() if v is not None}

    try:
        resp = requests.get(
            f"{main_api}/mypets/clinics/",
            params=params,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MyPets EGS API error (clinics)")
        raise MyPetsEGSAPIError(
            "Ошибка при запросе к MyPets EGS API (clinics)"
        ) from e

"""
    Получение информации о вет.клинике по id.
    # входные параметры: id клиники обязательный параметр!
"""
def get_mypets_clinics_id(
    id: Optional[int] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = "78") -> Dict[str, Any]:

    if id is None:
        raise MyPetsEGSAPIError(
            "Параметр 'id' обязателен для запроса /mypets/clinics/id/"
        )

    params: Dict[str, Any] = {"id": id}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/mypets/clinics/id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MyPets EGS API error (clinics/id)")
        raise MyPetsEGSAPIError(
            "Ошибка при запросе к MyPets EGS API (clinics/id)"
        ) from e

"""
    Поиск парков и площадок в заданном радиусе от координат.
входные параметры: можно оставить без фильтров
"""
def get_mypets_parks_playground(
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    place_type: Optional[str] = None,  # Парк, Площадка
) -> Dict[str, Any]:

    params: Dict[str, Any] = {
        "location_latitude": location_latitude,
        "location_longitude": location_longitude,
        "location_radius": location_radius,
        "type": place_type,
    }
    params = {k: v for k, v in params.items() if v is not None}

    try:
        resp = requests.get(
            f"{main_api}/mypets/parks-playground/",
            params=params,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MyPets EGS API error (parks-playground)")
        raise MyPetsEGSAPIError(
            "Ошибка при запросе к MyPets EGS API (parks-playground)"
        ) from e

"""
    Получение информации о парке/площадке по id.
    входные параметры: id парка/площадки обязательный параметр!
"""
def get_mypets_parks_playground_id(
    id: Optional[int] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = "78") -> Dict[str, Any]:

    if id is None:
        raise MyPetsEGSAPIError(
            "Параметр 'id' обязателен для запроса /mypets/parks-playground/id/"
        )

    params: Dict[str, Any] = {"id": id}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/mypets/parks-playground/id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MyPets EGS API error (parks-playground/id)")
        raise MyPetsEGSAPIError(
            "Ошибка при запросе к MyPets EGS API (parks-playground/id)"
        ) from e

"""
    Поиск приютов в заданном радиусе от координат и по специализации.
входные параметры: можно оставить без фильтров
"""
def get_mypets_shelters(
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    specialization: Optional[List[str]] = None,  # Кошки, Собаки, Дикие животные
) -> Dict[str, Any]:

    params: Dict[str, Any] = {
        "location_latitude": location_latitude,
        "location_longitude": location_longitude,
        "location_radius": location_radius,
        "specialization": specialization
    }

    params = {k: v for k, v in params.items() if v is not None}

    try:
        resp = requests.get(
            f"{main_api}/mypets/shelters/",
            params=params,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MyPets EGS API error (shelters)")
        raise MyPetsEGSAPIError(
            "Ошибка при запросе к MyPets EGS API (shelters)"
        ) from e

"""
  Получение информации о приюте по id.
  входные параметры: id приюта обязательный параметр!
"""
def get_mypets_shelters_id(
    id: Optional[int] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = "78",
) -> Dict[str, Any]:

    if id is None:
        raise MyPetsEGSAPIError(
            "Параметр 'id' обязателен для запроса /mypets/shelters/id/"
        )

    params: Dict[str, Any] = {"id": id}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/mypets/shelters/id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MyPets EGS API error (shelters/id)")
        raise MyPetsEGSAPIError(
            "Ошибка при запросе к MyPets EGS API (shelters/id)"
        ) from e

if __name__ == "__main__":
    #print(get_mypets_clinics())
    #print(get_mypets_clinics(services=["Рентген", "Офтальмология"]))
    #print(get_mypets_clinics_id(id=30))

    #print(get_mypets_parks_playground())
    #print(get_mypets_parks_playground(place_type="Парк"))

    #print(get_mypets_parks_playground_id(id=77))

    #print(get_mypets_shelters())
    #print(get_mypets_shelters(specialization=["Кошки"]))

    print(get_mypets_shelters_id(id=14))


