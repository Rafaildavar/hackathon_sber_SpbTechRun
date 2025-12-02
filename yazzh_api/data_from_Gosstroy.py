# Раздел Данные из Госстрой из "https://yazzh.gate.petersburg.ru"
from typing import Optional, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class GosstroyError(Exception):
    pass


"""
Плановые работы для отображения на карте.
Можно фильтровать по виду работ, категории, статусу, отношению, 214-ФЗ, датам, району и/или радиусу от точки.
"""
def get_gosstroy_map(
    type: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    assignment: Optional[str] = None,
    supervised_law_214: Optional[bool] = None,
    date_start_planned: Optional[str] = None,
    date_start_actual: Optional[str] = None,
    date_end_planned: Optional[str] = None,
    date_end_actual: Optional[str] = None,
    district: Optional[str] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    app_version: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if type is not None:
        params["type"] = type
    if category is not None:
        params["category"] = category
    if status is not None:
        params["status"] = status
    if assignment is not None:
        params["assignment"] = assignment
    if supervised_law_214 is not None:
        params["supervised_law_214"] = supervised_law_214
    if date_start_planned is not None:
        params["date_start_planned"] = date_start_planned
    if date_start_actual is not None:
        params["date_start_actual"] = date_start_actual
    if date_end_planned is not None:
        params["date_end_planned"] = date_end_planned
    if date_end_actual is not None:
        params["date_end_actual"] = date_end_actual
    if district is not None:
        params["district"] = district
    if location_latitude is not None:
        params["location_latitude"] = location_latitude
    if location_longitude is not None:
        params["location_longitude"] = location_longitude
    if location_radius is not None:
        params["location_radius"] = location_radius

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/gosstroy/map/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Gosstroy API error (gosstroy/map/)")
        raise GosstroyError(
            "Ошибка при запросе к Gosstroy API (gosstroy/map/)"
        ) from e


"""
Плановые работы по id.
Параметр id обязателен.
"""
def get_gosstroy_by_id(
    id: int,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise GosstroyError(
            "Параметр 'id' обязателен для запроса /gosstroy/{id}"
        )

    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/gosstroy/{id}",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Gosstroy API error (gosstroy/{id})")
        raise GosstroyError(
            "Ошибка при запросе к Gosstroy API (gosstroy/{id})"
        ) from e


"""
Справочник: объекты работ (вид работ).
"""
def get_gosstroy_types() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/gosstroy/type/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Gosstroy API error (gosstroy/type/)")
        raise GosstroyError(
            "Ошибка при запросе к Gosstroy API (gosstroy/type/)"
        ) from e


"""
Справочник: категории работ.
"""
def get_gosstroy_categories() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/gosstroy/category/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Gosstroy API error (gosstroy/category/)")
        raise GosstroyError(
            "Ошибка при запросе к Gosstroy API (gosstroy/category/)"
        ) from e


"""
не работает
Справочник: статусы работ.
def get_gosstroy_statuses() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/gosstroy/status/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Gosstroy API error (gosstroy/status/)")
        raise GosstroyError(
            "Ошибка при запросе к Gosstroy API (gosstroy/status/)"
        ) from e
"""

"""
Справочник: отношение работ (assignment).
"""
def get_gosstroy_assignments() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/gosstroy/assignment/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Gosstroy API error (gosstroy/assignment/)")
        raise GosstroyError(
            "Ошибка при запросе к Gosstroy API (gosstroy/assignment/)"
        ) from e


"""
Получение списка всех ответственных организаций.
"""
def get_gosstroy_info() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/gosstroy/info/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Gosstroy API error (gosstroy/info/)")
        raise GosstroyError(
            "Ошибка при запросе к Gosstroy API (gosstroy/info/)"
        ) from e


"""
Статистика работ: количество по районам.
Можно указать конкретный район для фильтрации.
"""
def get_gosstroy_stats_district(
    district: Optional[str] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if district is not None:
        params["district"] = district

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/gosstroy/stats/district/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Gosstroy API error (gosstroy/stats/district/)")
        raise GosstroyError(
            "Ошибка при запросе к Gosstroy API (gosstroy/stats/district/)"
        ) from e


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        # Примеры простых тестовых вызовов

        gosstroy_map = get_gosstroy_map(location_radius=5)
        logger.info("Плановые работы для карты (пример): %s", str(gosstroy_map)[:300])

        gosstroy_item = get_gosstroy_by_id(id=539)
        logger.info("Плановые работы по id (пример): %s", str(gosstroy_item)[:300])

        gosstroy_types = get_gosstroy_types()
        logger.info("Типы работ (пример): %s", str(gosstroy_types)[:300])

        gosstroy_categories = get_gosstroy_categories()
        logger.info("Категории работ (пример): %s", str(gosstroy_categories)[:300])

        #не работает функция закомичена
        #gosstroy_statuses = get_gosstroy_statuses()
        #logger.info("Статусы работ (пример): %s", str(gosstroy_statuses)[:300])

        gosstroy_assignments = get_gosstroy_assignments()
        logger.info("Отношение работ (пример): %s", str(gosstroy_assignments)[:300])

        gosstroy_info = get_gosstroy_info()
        logger.info("Ответственные организации (пример): %s", str(gosstroy_info)[:300])

        stats_district = get_gosstroy_stats_district()
        logger.info("Статистика работ по районам (пример): %s", str(stats_district)[:300])

    except GosstroyError as e:
        logger.error("Gosstroy API test failed: %s", e)
