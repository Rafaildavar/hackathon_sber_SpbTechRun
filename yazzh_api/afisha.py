# Раздел Афиша из "https://yazzh.gate.petersburg.ru"
from typing import Optional, List, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class AfishaError(Exception):
    pass


"""
Получение объекта раздела Афиша (событие) по place_id(id события).
входные параметры: place_id обязательный параметр!
"""
def get_afisha_by_id(
    place_id: int,
    region_id: Optional[str] = None,
    service: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if place_id is None:
        raise AfishaError(
            "Параметр 'place_id' обязателен для запроса /afisha/by_id/"
        )

    params: Dict[str, Any] = {
        "place_id": place_id,
    }

    if region_id is not None:
        params["region_id"] = region_id
    if service is not None:
        params["service"] = service

    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/afisha/by_id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Afisha API error (afisha/by_id)")
        raise AfishaError(
            "Ошибка при запросе к Afisha API (afisha/by_id)"
        ) from e


"""
Получение списка всех мероприятий Афиши в соответствии с выбранными фильтрами.
входные параметры: start_date и end_date обязательные параметры!
"""
def get_afisha_all(
    start_date: str,
    end_date: str,
    separation: Optional[bool] = None,
    categoria: Optional[str] = None, #Категории мероприятий, множественный выбор. Допускается ввод через запятую без пробела
    kids: Optional[bool] = None,
    free: Optional[bool] = None,
    age: Optional[str] = None, # Возраст /0,6,12,16,18. Допускается ввод через запятую без пробела.
    location_place: Optional[str] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    format: Optional[str] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    service: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if start_date is None:
        raise AfishaError(
            "Параметр 'start_date' обязателен для запроса /afisha/all/"
        )
    if end_date is None:
        raise AfishaError(
            "Параметр 'end_date' обязателен для запроса /afisha/all/"
        )

    params: Dict[str, Any] = {
        "start_date": start_date,
        "end_date": end_date,
    }

    if separation is not None:
        params["separation"] = separation
    if categoria is not None:
        params["categoria"] = categoria
    if kids is not None:
        params["kids"] = kids
    if free is not None:
        params["free"] = free
    if age is not None:
        params["age"] = age
    if location_place is not None:
        params["location_place"] = location_place
    if location_latitude is not None:
        params["location_latitude"] = location_latitude
    if location_longitude is not None:
        params["location_longitude"] = location_longitude
    if location_radius is not None:
        params["location_radius"] = location_radius
    if format is not None:
        params["format"] = format
    if page is not None:
        params["page"] = page
    if count is not None:
        params["count"] = count
    if service is not None:
        params["service"] = service

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/afisha/all/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Afisha API error (afisha/all)")
        raise AfishaError(
            "Ошибка при запросе к Afisha API (afisha/all)"
        ) from e


"""
Получение списка всех категорий всех событий Афиши.
"""
def get_afisha_category_all(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    service: Optional[str] = None,
    user_id: Optional[str] = None,
    app_version: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date
    if service is not None:
        params["service"] = service

    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if app_version is not None:
        headers["app-version"] = app_version
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/afisha/category/all/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Afisha API error (afisha/category/all)")
        raise AfishaError(
            "Ошибка при запросе к Afisha API (afisha/category/all)"
        ) from e


"""
Получение списка категорий локаций и всех событий для карты Афиши.
"""
def get_afisha_map_all(
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    region_id: Optional[str] = None,
    user_id: Optional[str] = None,
    app_version: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if category is not None:
        params["category"] = category
    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date
    if region_id is not None:
        params["region_id"] = region_id

    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if app_version is not None:
        headers["app-version"] = app_version
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/afisha/map/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Afisha API error (afisha/map)")
        raise AfishaError(
            "Ошибка при запросе к Afisha API (afisha/map)"
        ) from e


"""
Получение карточки места проведения мероприятий Афиши по id места проведения мероприятия.
входные параметры: id обязательный параметр!
"""
def get_afisha_map_by_id(
    id: int,
    user_id: Optional[str] = None,
    app_version: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise AfishaError(
            "Параметр 'id' обязателен для запроса /afisha/map/{id}"
        )

    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if app_version is not None:
        headers["app-version"] = app_version
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/afisha/map/{id}",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Afisha API error (afisha/map/{id})")
        raise AfishaError(
            "Ошибка при запросе к Afisha API (afisha/map/{id})"
        ) from e


"""
Получение списка категорий всех локаций всех событий Афиши.
"""
def get_afisha_location_categories(
    app_version: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/afisha/location/category/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Afisha API error (afisha/location/category)")
        raise AfishaError(
            "Ошибка при запросе к Afisha API (afisha/location/category)"
        ) from e


if __name__ == "__main__":
    #print(get_afisha_by_id(place_id=70451))

    """print(
        get_afisha_all(
            start_date="2025-11-21T00:00:00",
            end_date="2025-12-22T00:00:00",
        )
    )"""

    #print(get_afisha_category_all())
    #print(get_afisha_map_all())
    #print(get_afisha_map_by_id(id=25))
    print(get_afisha_location_categories())
