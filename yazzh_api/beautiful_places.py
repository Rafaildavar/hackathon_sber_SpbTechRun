# Раздел Красивые места из "https://yazzh.gate.petersburg.ru"
from typing import Optional, List, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class BeautifulPlacesError(Exception):
    pass


"""
Получение списка красивых мест в соответствии с выбранными фильтрами.
"""
def get_beautiful_places(
    area: Optional[str] = None,
    categoria: Optional[str] = None,
    keywords: Optional[str] = None,
    district: Optional[str] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    app_version: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if area is not None:
        params["area"] = area
    if categoria is not None:
        params["categoria"] = categoria
    if keywords is not None:
        params["keywords"] = keywords
    if district is not None:
        params["district"] = district
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
            f"{main_api}/beautiful_places/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("BeautifulPlaces API error (beautiful_places)")
        raise BeautifulPlacesError(
            "Ошибка при запросе к BeautifulPlaces API (beautiful_places)"
        ) from e


"""
Получение списка мест по списку id.
входные параметры: ids обязательный параметр!
"""
def get_beautiful_places_by_ids(
    ids: str, #Список идентификаторов мест через запятую. Для получения Мест из ЛК, к id необходимо добавить '-M'
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    region_id: Optional[str] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if ids is None:
        raise BeautifulPlacesError(
            "Параметр 'ids' обязателен для запроса /beautiful_places/id/"
        )

    params: Dict[str, Any] = {
        "ids": ids,
    }

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
            f"{main_api}/beautiful_places/id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("BeautifulPlaces API error (beautiful_places/id)")
        raise BeautifulPlacesError(
            "Ошибка при запросе к BeautifulPlaces API (beautiful_places/id)"
        ) from e


"""
Получение списка областей и их районов для красивых мест.
"""
def get_beautiful_places_areas(
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
            f"{main_api}/beautiful_places/area/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("BeautifulPlaces API error (beautiful_places/area)")
        raise BeautifulPlacesError(
            "Ошибка при запросе к BeautifulPlaces API (beautiful_places/area)"
        ) from e


"""
Получение списка районов в соответствии с областью.
Эндпоинт помечен как deprecated в OpenAPI.
"""
def get_beautiful_places_area_districts(
    area: Optional[str] = None,
    app_version: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if area is not None:
        params["area"] = area

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/beautiful_places/area/district/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "BeautifulPlaces API error (beautiful_places/area/district)"
        )
        raise BeautifulPlacesError(
            "Ошибка при запросе к BeautifulPlaces API (beautiful_places/area/district)"
        ) from e


"""
Получение списка всех категорий красивых мест.
"""
def get_beautiful_places_categories(
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
            f"{main_api}/beautiful_places/categoria/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "BeautifulPlaces API error (beautiful_places/categoria)"
        )
        raise BeautifulPlacesError(
            "Ошибка при запросе к BeautifulPlaces API (beautiful_places/categoria)"
        ) from e


"""
Получение списка всех ключевых слов для красивых мест.
"""
def get_beautiful_places_keywords(
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
            f"{main_api}/beautiful_places/keywords/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "BeautifulPlaces API error (beautiful_places/keywords)"
        )
        raise BeautifulPlacesError(
            "Ошибка при запросе к BeautifulPlaces API (beautiful_places/keywords)"
        ) from e


"""
Получение списка маршрутов в соответствии с выбранными фильтрами.
"""
def get_beautiful_routes_all(
    access_for_disabled: Optional[bool] = None,
    length_km_from: Optional[int] = None,
    length_km_to: Optional[int] = None,
    time_min_from: Optional[int] = None,
    time_min_to: Optional[int] = None,
    theme: Optional[str] = None,
    type: Optional[str] = None,
    audio: Optional[bool] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    expanded: Optional[bool] = None,
    app_version: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if access_for_disabled is not None:
        params["access_for_disabled"] = access_for_disabled
    if length_km_from is not None:
        params["length_km_from"] = length_km_from
    if length_km_to is not None:
        params["length_km_to"] = length_km_to
    if time_min_from is not None:
        params["time_min_from"] = time_min_from
    if time_min_to is not None:
        params["time_min_to"] = time_min_to
    if theme is not None:
        params["theme"] = theme
    if type is not None:
        params["type"] = type
    if audio is not None:
        params["audio"] = audio
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
    if expanded is not None:
        params["expanded"] = expanded

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/beautiful_places/routes/all/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "BeautifulPlaces API error (beautiful_places/routes/all)"
        )
        raise BeautifulPlacesError(
            "Ошибка при запросе к BeautifulPlaces API (beautiful_places/routes/all)"
        ) from e


"""
Получение объекта маршрутов по списку id.
входные параметры: ids обязательный параметр!
"""
def get_beautiful_routes_by_ids(
    ids: str,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    region_id: Optional[str] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if ids is None:
        raise BeautifulPlacesError(
            "Параметр 'ids' обязателен для запроса /beautiful_places/routes/id/"
        )

    params: Dict[str, Any] = {
        "ids": ids,
    }

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
            f"{main_api}/beautiful_places/routes/id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "BeautifulPlaces API error (beautiful_places/routes/id)"
        )
        raise BeautifulPlacesError(
            "Ошибка при запросе к BeautifulPlaces API (beautiful_places/routes/id)"
        ) from e


"""
Получение списка тем маршрутов (theme) для красивых мест.
"""
def get_beautiful_routes_themes(
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
            f"{main_api}/beautiful_places/routes/theme/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "BeautifulPlaces API error (beautiful_places/routes/theme)"
        )
        raise BeautifulPlacesError(
            "Ошибка при запросе к BeautifulPlaces API (beautiful_places/routes/theme)"
        ) from e


"""
Получение списка типов маршрутов (type) для красивых мест.
"""
def get_beautiful_routes_types(
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
            f"{main_api}/beautiful_places/routes/type/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "BeautifulPlaces API error (beautiful_places/routes/type)"
        )
        raise BeautifulPlacesError(
            "Ошибка при запросе к BeautifulPlaces API (beautiful_places/routes/type)"
        ) from e


if __name__ == "__main__":
    #print(get_beautiful_places())
    #print(get_beautiful_places_by_ids(ids="1,2,3"))
    #print(get_beautiful_places_areas())
    #print(get_beautiful_places_categories())
    #print(get_beautiful_places_keywords())
    #print(get_beautiful_routes_all())
    #print(get_beautiful_routes_by_ids(ids="1,2"))
    print(get_beautiful_routes_themes())
    print(get_beautiful_routes_types())
    ...
