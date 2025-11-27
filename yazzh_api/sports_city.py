#Раздел спортивный город (Спортивные события) из "https://yazzh.gate.petersburg.ru"
from typing import Optional, List, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"

class SportCityError(Exception):
    pass

"""
Получение спортивных мероприятий (районных) в соответствии с выбранными фильтрами.
входные параметры: можно оставить без фильтров
"""
def get_sport_events(
    categoria: Optional[str] = None,
    type_municipality: Optional[str] = None,
    start_date: Optional[str] = None,   # формат yyyy-mm-dd
    end_date: Optional[str] = None,     # формат yyyy-mm-dd
    district: Optional[str] = None,
    ovz: Optional[str] = None,          # "true"/"false" — доступность для инвалидов
    family_hour: Optional[str] = None,  # "true"/"false" — программа "Семейный час"
    page: Optional[int] = 1,
    count: Optional[int] = 10,
    service: Optional[str] = None,   # например, "silverAge"
    region: Optional[str] = "78") -> Dict[str, Any]:

    params: Dict[str, Any] = {
        "categoria": categoria,
        "type_municipality": type_municipality,
        "start_date": start_date,
        "end_date": end_date,
        "district": district,
        "ovz": ovz,
        "family_hour": family_hour,
        "page": page,
        "count": count,
        "service": service,
    }
    params = {k: v for k, v in params.items() if v is not None}

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/sport-events/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("SportCity API error (sport-events)")
        raise SportCityError(
            "Ошибка при запросе к SportCity API (sport-events)"
        ) from e

"""
Спортивные мероприятия (районные) по id.
входные параметры: id обязательный параметр!
"""
def get_sport_event_by_id(
    id: Optional[int] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = "78") -> Dict[str, Any]:

    if id is None:
        raise SportCityError(
            "Параметр 'id' обязателен для запроса /sport-events/id/"
        )

    params: Dict[str, Any] = {"id": id}

    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/sport-events/id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("SportCity API error (sport-events/id)")
        raise SportCityError(
            "Ошибка при запросе к SportCity API (sport-events/id)"
        ) from e

"""
Получение списка всех категорий спортивных событий для выбранного района.
входные параметры: район обязательный параметр!, 
"""
def get_sport_events_categoria(
    district: Optional[str] = None,
    service: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = "78",) -> Dict[str, Any]:

    if district is None:
        raise SportCityError(
            "Параметр 'district' обязателен для запроса /sport-events/categoria/"
        )

    params: Dict[str, Any] = {
        "district": district,
        "service": service,  # например, silverAge
    }
    params = {k: v for k, v in params.items() if v is not None}

    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/sport-events/categoria/",
            params=params,
            headers=headers,
            timeout=20,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("SportCity API error (sport-events/categoria)")
        raise SportCityError(
            "Ошибка при запросе к SportCity API (sport-events/categoria)"
        ) from e

"""
Получение спортивных мероприятий (районных) для карты в соответствии с выбранными фильтрами.
входные параметры: хотя бы один фильтр указать надо, без него не работает
"""
def get_sport_events_map(
    categoria: Optional[str] = None,
    type_municipality: Optional[str] = None,
    start_date: Optional[str] = None,   # формат yyyy-mm-dd
    end_date: Optional[str] = None,     # формат yyyy-mm-dd
    district: Optional[str] = None,
    ovz: Optional[str] = None,          # "true"/"false" — доступность для инвалидов
    family_hour: Optional[str] = None,  # "true"/"false" — программа "Семейный час"
    service: Optional[str] = None,      # например, "silverAge"
    region: Optional[str] = "78") -> Dict[str, Any]:

    params: Dict[str, Any] = {
        "categoria": categoria,
        "type_municipality": type_municipality,
        "start_date": start_date,
        "end_date": end_date,
        "district": district,
        "ovz": ovz,
        "family_hour": family_hour,
        "service": service,
    }
    params = {k: v for k, v in params.items() if v is not None}

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/sport-events/map",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("SportCity API error (sport-events/map)")
        raise SportCityError(
            "Ошибка при запросе к SportCity API (sport-events/map)"
        ) from e

if __name__ == "__main__":
    #print(get_sport_events())
    #print(get_sport_event_by_id(id=9243))

    #print(get_sport_events_categoria(district="приморский"))

    #print(get_sport_events_map(categoria="Волейбол"))
    print(get_sport_events_map(district="приморский"))
    ...