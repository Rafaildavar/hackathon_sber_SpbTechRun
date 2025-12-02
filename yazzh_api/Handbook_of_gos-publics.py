# Раздел Справочник по Госпабликам из "https://yazzh.gate.petersburg.ru"
from typing import Optional, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class GosPublicsError(Exception):
    pass


"""
Метод под id паблика.
Параметр id — идентификатор паблика, обязателен.
"""
def get_gos_public_by_id(
    id: int,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise GosPublicsError(
            "Параметр 'id' обязателен для запроса /gos-publics/{id}"
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
            f"{main_api}/gos-publics/{id}",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("GosPublics API error (gos-publics/{id})")
        raise GosPublicsError(
            "Ошибка при запросе к GosPublics API (gos-publics/{id})"
        ) from e


"""
Метод для карты, поиск по фильтру.
Фильтры:
- type — тип организации
- name — название организации (частичное совпадение)
- district — район города (без слова «район»)
- location_latitude / location_longitude — координаты
- location_radius — радиус поиска (км)
- page, count — пагинация.
"""
def get_gos_publics_map(
    type: Optional[str] = None,
    name: Optional[str] = None,
    district: Optional[str] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if type is not None:
        params["type"] = type
    if name is not None:
        params["name"] = name
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
    if user_id is not None:
        headers["user-id"] = user_id

    try:
        resp = requests.get(
            f"{main_api}/gos-publics/map/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("GosPublics API error (gos-publics/map/)")
        raise GosPublicsError(
            "Ошибка при запросе к GosPublics API (gos-publics/map/)"
        ) from e


"""
Справочник по типам организаций (type).
"""
def get_gos_publics_types(
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id

    try:
        resp = requests.get(
            f"{main_api}/gos-publics/type/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("GosPublics API error (gos-publics/type/)")
        raise GosPublicsError(
            "Ошибка при запросе к GosPublics API (gos-publics/type/)"
        ) from e


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        # Пример запроса по id:
        public_item = get_gos_public_by_id(id=1294)
        logger.info("Госпаблик по id (пример): %s", str(public_item)[:300])

        types_data = get_gos_publics_types()
        logger.info("Типы госпабликов (пример): %s", str(types_data)[:300])

        publics_map = get_gos_publics_map(
            page=1,
            count=5,
        )
        logger.info("Карта госпабликов (пример): %s", str(publics_map)[:300])


    except GosPublicsError as e:
        logger.error("GosPublics API test failed: %s", e)
