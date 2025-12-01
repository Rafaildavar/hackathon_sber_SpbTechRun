# Раздел Я родитель из "https://yazzh.gate.petersburg.ru"
from typing import Optional, List, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class IParentError(Exception):
    pass


"""
Получения списка всех категорий мест (кэшируется).
"""
def get_iparent_places_categories(
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/iparent/places/categoria/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("IParent API error (iparent/places/categoria)")
        raise IParentError(
            "Ошибка при запросе к IParent API (iparent/places/categoria)"
        ) from e


"""
Получения списка мест с детьми в соответствии с выбранными фильтрами (кэшируется).
"""
def get_iparent_places_all(
    categoria: Optional[str] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if categoria is not None:
        params["categoria"] = categoria

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/iparent/places/all/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("IParent API error (iparent/places/all)")
        raise IParentError(
            "Ошибка при запросе к IParent API (iparent/places/all)"
        ) from e


"""
Объект раздела Места по id.
входные параметры: place_id обязательный параметр!
"""
def get_iparent_place_by_id(
    place_id: int,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if place_id is None:
        raise IParentError(
            "Параметр 'place_id' обязателен для запроса /iparent/places/by_id/"
        )

    params: Dict[str, Any] = {"place_id": place_id}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/iparent/places/by_id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("IParent API error (iparent/places/by_id)")
        raise IParentError(
            "Ошибка при запросе к IParent API (iparent/places/by_id)"
        ) from e


"""
Получения списка всех категорий событий.
"""
def get_iparent_recreations_categories(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    user_id: Optional[str] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date

    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/iparent/recreations/categoria/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("IParent API error (iparent/recreations/categoria)")
        raise IParentError(
            "Ошибка при запросе к IParent API (iparent/recreations/categoria)"
        ) from e


"""
Получения списка мероприятий для отдыха с детьми в соответствии с выбранными фильтрами.
"""
def get_iparent_recreations_all(
    categoria: Optional[str] = None,
    free: Optional[bool] = None,
    min_age: Optional[str] = None,
    max_age: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    app_version: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if categoria is not None:
        params["categoria"] = categoria
    if free is not None:
        params["free"] = free
    if min_age is not None:
        params["min_age"] = min_age
    if max_age is not None:
        params["max_age"] = max_age
    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date
    if location_latitude is not None:
        params["location_latitude"] = location_latitude
    if location_longitude is not None:
        params["location_longitude"] = location_longitude
    if location_radius is not None:
        params["location_radius"] = location_radius
    if page is not None:
        params["page"] = page
    if count is not None:
        params["count"] = count

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/iparent/recreations/all/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("IParent API error (iparent/recreations/all)")
        raise IParentError(
            "Ошибка при запросе к IParent API (iparent/recreations/all)"
        ) from e


"""
Объект раздела События по id.
входные параметры: id обязательный параметр!
"""
def get_iparent_recreation_by_id(
    id: int,
    region_id: Optional[str] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise IParentError(
            "Параметр 'id' обязателен для запроса /iparent/recreations/{id}"
        )

    params: Dict[str, Any] = {}
    if region_id is not None:
        params["region_id"] = region_id

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/iparent/recreations/{id}",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("IParent API error (iparent/recreations/{id})")
        raise IParentError(
            "Ошибка при запросе к IParent API (iparent/recreations/{id})"
        ) from e


if __name__ == "__main__":
    #print(get_iparent_places_categories())

    #print(get_iparent_places_all(categoria="Парки"))
    #print(get_iparent_places_all())

    #print(get_iparent_place_by_id(place_id=31))

    #print(get_iparent_recreations_categories())

    print(get_iparent_recreations_all(categoria="Театр", free=True))

    # print(get_iparent_recreation_by_id(id=1))
    ...
