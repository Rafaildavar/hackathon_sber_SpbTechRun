# Раздел Плановые работы (ГАТИ) из "https://yazzh.gate.petersburg.ru"
from typing import Optional, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class GatiError(Exception):
    pass


"""
Ордера работ для отображения на карте.
Можно фильтровать по району, типу работы и/или по радиусу от точки.
"""
def get_gati_orders_map(
    district: Optional[str] = None,
    work_type: Optional[str] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if district is not None:
        params["district"] = district
    if work_type is not None:
        params["work_type"] = work_type
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

    try:
        resp = requests.get(
            f"{main_api}/gati/orders/map/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Gati API error (gati/orders/map/)")
        raise GatiError(
            "Ошибка при запросе к Gati API (gati/orders/map/)"
        ) from e


"""
Получение информации по ордеру работ по его id.
Параметр id обязателен.
"""
def get_gati_order_by_id(
    id: int,
    user_id: Optional[str] = None,
    app_version: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise GatiError(
            "Параметр 'id' обязателен для запроса /gati/orders/{id}"
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
            f"{main_api}/gati/orders/{id}",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Gati API error (gati/orders/{id})")
        raise GatiError(
            "Ошибка при запросе к Gati API (gati/orders/{id})"
        ) from e


"""
Получение списка типов работ (обработанный справочник).
"""
def get_gati_work_types() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/gati/orders/work-type/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Gati API error (gati/orders/work-type/)")
        raise GatiError(
            "Ошибка при запросе к Gati API (gati/orders/work-type/)"
        ) from e


"""
Получение списка типов работ «как есть» (сырой справочник).
"""
def get_gati_work_types_all() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/gati/orders/work-type-all/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Gati API error (gati/orders/work-type-all/)")
        raise GatiError(
            "Ошибка при запросе к Gati API (gati/orders/work-type-all/)"
        ) from e


"""
Получение списка всех ответственных организаций ГАТИ.
"""
def get_gati_info() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/gati/info/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Gati API error (gati/info/)")
        raise GatiError(
            "Ошибка при запросе к Gati API (gati/info/)"
        ) from e


"""
Ордера работ, количество по районам.
Можно указать район для фильтрации.
"""
def get_gati_orders_district(
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
            f"{main_api}/gati/orders/district/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Gati API error (gati/orders/district/)")
        raise GatiError(
            "Ошибка при запросе к Gati API (gati/orders/district/)"
        ) from e


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        orders_map = get_gati_orders_map(page=1, count=5)
        logger.info("Ордера для карты (пример): %s", str(orders_map)[:300])

        order_item = get_gati_order_by_id(id=76089)
        logger.info("Ордер по id (пример): %s", str(order_item)[:300])

        work_types = get_gati_work_types()
        logger.info("Типы работ (пример): %s", str(work_types)[:300])

        work_types_all = get_gati_work_types_all()
        logger.info("Типы работ (как есть) (пример): %s", str(work_types_all)[:300])

        info = get_gati_info()
        logger.info("Ответственные организации (пример): %s", str(info)[:300])

        orders_district = get_gati_orders_district()
        logger.info("Ордера по районам (пример): %s", str(orders_district)[:300])


    except GatiError as e:
        logger.error("GATI API test failed: %s", e)
