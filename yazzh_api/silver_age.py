# Раздел "Серебряный возраст" из "https://yazzh.gate.petersburg.ru"
from typing import Optional, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class PensionerError(Exception):
    pass


"""
Информация по Горячим номерам (по районам).
"""
def get_pensioner_hotlines(
    district: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if district is not None:
        params["district"] = district

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/pensioner/hotlines/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/hotlines/)")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/hotlines/)"
        ) from e


"""
Справочник районов для горячих номеров.
"""
def get_pensioner_hotlines_districts(
    region: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/pensioner/hotlines/district/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/hotlines/district/)")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/hotlines/district/)"
        ) from e


"""
Получения списка всех категорий кружков досуга для пенсионеров.
"""
def get_pensioner_services_categories(
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
            f"{main_api}/pensioner/services/category/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/services/category/)")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/services/category/)"
        ) from e


"""
Кружки досуга для пенсионеров по выбранным типам в заданном радиусе.
"""
def get_pensioner_services(
    location_title: Optional[str] = None,
    category: Optional[str] = None,
    district: Optional[str] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    egs: Optional[bool] = None,
    app_version: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if location_title is not None:
        params["location_title"] = location_title
    if category is not None:
        params["category"] = category
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
    if egs is not None:
        params["egs"] = egs

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/pensioner/services/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/services/)")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/services/)"
        ) from e


"""
Объект кружка досуга для пенсионеров по id.
Параметр id обязателен.
"""
def get_pensioner_service_by_id(
    id: str,
    egs: Optional[bool] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise PensionerError(
            "Параметр 'id' обязателен для запроса /pensioner/services/{id}"
        )

    params: Dict[str, Any] = {}
    if egs is not None:
        params["egs"] = egs

    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/pensioner/services/{id}",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/services/{id})")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/services/{id})"
        ) from e


"""
Справочник районов для кружков досуга.
"""
def get_pensioner_services_districts(
    region: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/pensioner/services/district/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/services/district/)")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/services/district/)"
        ) from e


"""
Места для пенсионеров по выбранным типам (общий досуг).
"""
def get_pensioner_locations(
    category: Optional[str] = None,
    district: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if category is not None:
        params["category"] = category
    if district is not None:
        params["district"] = district

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/pensioner/services/location/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/services/location/)")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/services/location/)"
        ) from e


"""
Места для пенсионеров по выбранным типам (спортивный досуг).
"""
def get_pensioner_sports_locations(
    category: Optional[str] = None,
    district: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if category is not None:
        params["category"] = category
    if district is not None:
        params["district"] = district

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/pensioner/sports/location/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/sports/location/)")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/sports/location/)"
        ) from e


"""
Справочник категорий карты (серебряный возраст).
"""
def get_pensioner_map_categories(
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/pensioner/map/category/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/map/category/)")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/map/category/)"
        ) from e


"""
Объекты карты для пенсионеров.
"""
def get_pensioner_map_objects(
    category: Optional[str] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if category is not None:
        params["category"] = category
    if location_latitude is not None:
        params["location_latitude"] = location_latitude
    if location_longitude is not None:
        params["location_longitude"] = location_longitude
    if location_radius is not None:
        params["location_radius"] = location_radius

    try:
        resp = requests.get(
            f"{main_api}/pensioner/map/",
            params=params,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/map/)")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/map/)"
        ) from e


"""
Объект карты по id.
Параметр id обязателен.
"""
def get_pensioner_map_object_by_id(
    id: str,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise PensionerError(
            "Параметр 'id' обязателен для запроса /pensioner/map/{id}"
        )

    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/pensioner/map/{id}",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/map/{id})")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/map/{id})"
        ) from e


"""
Получения списка всех категорий статей (серебряный возраст).
"""
def get_pensioner_posts_categories() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/pensioner/posts/category/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/posts/category/)")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/posts/category/)"
        ) from e


"""
Статьи по выбранным категориям.
"""
def get_pensioner_posts(
    category: Optional[str] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if category is not None:
        params["category"] = category
    if page is not None:
        params["page"] = page
    if count is not None:
        params["count"] = count

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id

    try:
        resp = requests.get(
            f"{main_api}/pensioner/posts/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/posts/)")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/posts/)"
        ) from e


"""
Вывод статьи по id.
Параметр id обязателен.
"""
def get_pensioner_post_by_id(
    id: int,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise PensionerError(
            "Параметр 'id' обязателен для запроса /pensioner/posts/{id}"
        )

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/pensioner/posts/{id}",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/posts/{id})")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/posts/{id})"
        ) from e


"""
Справочник категорий 'Помощь и благотворительность'.
"""
def get_pensioner_charity_categories() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/pensioner/charity/category/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/charity/category/)")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/charity/category/)"
        ) from e


"""
Помощь и благотворительность для пенсионеров по выбранным типам в заданном радиусе.
"""
def get_pensioner_charity(
    category: Optional[str] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if category is not None:
        params["category"] = category
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

    try:
        resp = requests.get(
            f"{main_api}/pensioner/charity/",
            params=params,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/charity/)")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/charity/)"
        ) from e


"""
Объект 'Помощь и благотворительность' по id.
Параметр id обязателен.
"""
def get_pensioner_charity_by_id(
    id: int,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise PensionerError(
            "Параметр 'id' обязателен для запроса /pensioner/charity/{id}"
        )

    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/pensioner/charity/{id}",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Pensioner API error (pensioner/charity/{id})")
        raise PensionerError(
            "Ошибка при запросе к Pensioner API (pensioner/charity/{id})"
        ) from e


if __name__ == "__main__":
    #print(get_pensioner_hotlines())
    #print(get_pensioner_hotlines_districts())
    #print(get_pensioner_services_categories())

    #print(get_pensioner_services())
    #print(get_pensioner_services(district="Адмиралтейский"))

    #print(get_pensioner_service_by_id("475"))
    #print(get_pensioner_services_districts())

    #print(get_pensioner_locations())
    #print(get_pensioner_sports_locations())

    #print(get_pensioner_map_categories())
    #print(get_pensioner_map_objects())

    #print(get_pensioner_map_object_by_id("14,Социально-досуговые центры"))

    print(get_pensioner_posts_categories())
    print(get_pensioner_posts())
    #print(get_pensioner_post_by_id(id=1))

    #print(get_pensioner_charity_categories())
    #print(get_pensioner_charity())
    #print(get_pensioner_charity_by_id(1))
    ...
