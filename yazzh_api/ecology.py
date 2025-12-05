# Раздел Экология из "https://yazzh.gate.petersburg.ru"
from typing import Optional, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class EcologyError(Exception):
    pass


"""
Возвращает данные по ближайшим мусоросборкам (предыдущая версия).
Для сортировки по расстоянию рекомендуется передавать latitude и longitude.
"""
def get_nearest_recycling(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    count: Optional[int] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if latitude is not None:
        params["latitude"] = latitude
    if longitude is not None:
        params["longitude"] = longitude
    if count is not None:
        params["count"] = count

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/api/v2/external/recycling/nearest",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Ecology API error (api/v2/external/recycling/nearest)")
        raise EcologyError(
            "Ошибка при запросе к Ecology API (api/v2/external/recycling/nearest)"
        ) from e


"""
[Карта] Возвращает все пункты сбора по фильтрам.
Выборка по категориям через запятую без пробелов.
"""
def get_recycling_map(
    category: Optional[str] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    app_version: Optional[str] = None,
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

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/api/v2/recycling/map/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Ecology API error (api/v2/recycling/map/)")
        raise EcologyError(
            "Ошибка при запросе к Ecology API (api/v2/recycling/map/)"
        ) from e


"""
[Карта] Возвращает по id все данные о пункте.
Параметр id обязателен.
"""
def get_recycling_map_item_by_id(
    id: int,
    user_id: Optional[str] = None,
    app_version: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise EcologyError(
            "Параметр 'id' обязателен для запроса /api/v2/recycling/map/{id}"
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
            f"{main_api}/api/v2/recycling/map/{id}",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Ecology API error (api/v2/recycling/map/{id})")
        raise EcologyError(
            "Ошибка при запросе к Ecology API (api/v2/recycling/map/{id})"
        ) from e


"""
[Карта] Возвращает категории и идентификаторы пунктов приёма.
"""
def get_recycling_categories(
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/api/v2/recycling/map/category/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Ecology API error (api/v2/recycling/map/category/)")
        raise EcologyError(
            "Ошибка при запросе к Ecology API (api/v2/recycling/map/category/)"
        ) from e


"""
[Карта] Возвращает количество пунктов по категориям.
"""
def get_recycling_counts_by_category(
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/api/v2/recycling/map/counts/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Ecology API error (api/v2/recycling/map/counts/)")
        raise EcologyError(
            "Ошибка при запросе к Ecology API (api/v2/recycling/map/counts/)"
        ) from e


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        nearest = get_nearest_recycling(latitude=60.0, longitude=30.3, count=3)
        logger.info("Ближайшие мусоросборки (пример): %s", str(nearest)[:300])

        recycling_map = get_recycling_map(
            category="Бумага,Пластик",
            location_latitude=60.0,
            location_longitude=30.3,
            location_radius=5,
        )
        logger.info("Пункты сбора по карте (пример): %s", str(recycling_map)[:300])

        item = get_recycling_map_item_by_id(id=7333)
        logger.info("Пункт приёма по id (пример): %s", str(item)[:300])

        categories = get_recycling_categories()
        logger.info("Категории пунктов сбора (пример): %s", str(categories)[:300])

        counts = get_recycling_counts_by_category()
        logger.info("Количество пунктов по категориям (пример): %s", str(counts))

    except EcologyError as e:
        logger.error("Ecology API test failed: %s", e)
