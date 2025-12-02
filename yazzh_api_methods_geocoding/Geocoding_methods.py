# Раздел Методы геокодирования (получение информации по id здания и по адресу)
from typing import Optional, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"


class GeoError(Exception):
    pass


"""
Получить информацию о здании по его идентификатору building_id.
Параметр building_id обязателен.
Формат вывода: сокращенный (short) или расширенный (extended, по умолчанию).
"""
def get_geo_building_by_id(
    building_id: str,
    format: Optional[str] = "extended",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if building_id is None:
        raise GeoError(
            "Параметр 'building_id' обязателен для запроса /api/v2/geo/buildings/{building_id}"
        )

    params: Dict[str, Any] = {}
    if format is not None:
        params["format"] = format

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{geo_api}/geo/buildings/{building_id}",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Geo API error (geo/buildings/{building_id})")
        raise GeoError(
            "Ошибка при запросе к Geo API (geo/buildings/{building_id})"
        ) from e


"""
Поиск зданий по адресу (полнотекстовый поиск).
Параметр query (текстовый запрос) обязателен.
"""
def search_geo_buildings(
    query: str,
    count: Optional[int] = None,
    region_of_search: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if query is None:
        raise GeoError(
            "Параметр 'query' обязателен для запроса /api/v2/geo/buildings/search/"
        )

    params: Dict[str, Any] = {"query": query}
    if count is not None:
        params["count"] = count
    if region_of_search is not None:
        params["region_of_search"] = region_of_search

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{geo_api}/geo/buildings/search/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Geo API error (geo/buildings/search/)")
        raise GeoError(
            "Ошибка при запросе к Geo API (geo/buildings/search/)"
        ) from e


"""
не работает, не знаю что в id_building_fias должно быть
Получить информацию о здании по ФИАС-идентификатору.
Параметр id_building_fias обязателен.
Формат вывода: сокращенный (short) или расширенный (extended, по умолчанию).

def get_geo_building_by_fias(
    id_building_fias: str,
    format: Optional[str] = "extended",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id_building_fias is None:
        raise GeoError(
            "Параметр 'id_building_fias' обязателен для запроса /api/v2/geo/buildings/fias/{id_building_fias}"
        )

    params: Dict[str, Any] = {}
    if format is not None:
        params["format"] = format

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{geo_api}/geo/buildings/fias/{id_building_fias}",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Geo API error (geo/buildings/fias/{id_building_fias})")
        raise GeoError(
            "Ошибка при запросе к Geo API (geo/buildings/fias/{id_building_fias})"
        ) from e
"""

"""
Получить список муниципальных округов (только для СПб).
"""
def get_geo_municipalities(
    region: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{geo_api}/geo/municipality/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Geo API error (geo/municipality/)")
        raise GeoError(
            "Ошибка при запросе к Geo API (geo/municipality/)"
        ) from e


"""
Получить список районов (только для СПб).
"""
def get_geo_districts(
    region: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{geo_api}/geo/district/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Geo API error (geo/district/)")
        raise GeoError(
            "Ошибка при запросе к Geo API (geo/district/)"
        ) from e


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        # Пример поиска по адресу
        search_result = search_geo_buildings(
            query="Невский проспект 1",
            region_of_search="78",
        )
        logger.info(
            "Поиск зданий по адресу (пример): %s",
            str(search_result)[:300],
        )

        municipalities = get_geo_municipalities(region="78")
        logger.info(
            "Муниципальные округа (пример): %s",
            str(municipalities)[:300],
        )

        districts = get_geo_districts(region="78")
        logger.info(
            "Районы города (пример): %s",
            str(districts)[:300],
        )

        building = get_geo_building_by_id(building_id="210836", region="78")
        logger.info("Здание по building_id (пример): %s", str(building)[:300])

        # building_fias = get_geo_building_by_fias(id_building_fias="REAL_FIAS_ID", region="78")
        # logger.info("Здание по ФИАС (пример): %s", str(building_fias)[:300])

    except GeoError as e:
        logger.error("Geo API test failed: %s", e)
