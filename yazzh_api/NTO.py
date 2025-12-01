# Раздел Нестационарные торговые объекты (НТО) из "https://yazzh.gate.petersburg.ru"
from typing import Optional, List, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class NtoError(Exception):
    pass


"""
Получение НТО в соответствии с выбранными фильтрами (кэшируется).
"""
def get_nto(
    purpose: Optional[str] = None,
    trade_type: Optional[str] = None,
    trade_kind: Optional[str] = None,
    name_sub: Optional[str] = None,
    name_des: Optional[str] = None,
    arenda_exists: Optional[bool] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if purpose is not None:
        params["purpose"] = purpose
    if trade_type is not None:
        params["trade_type"] = trade_type
    if trade_kind is not None:
        params["trade_kind"] = trade_kind
    if name_sub is not None:
        params["name_sub"] = name_sub
    if name_des is not None:
        params["name_des"] = name_des
    if arenda_exists is not None:
        params["arenda_exists"] = arenda_exists
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
            f"{main_api}/nto/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("NTO API error (nto)")
        raise NtoError(
            "Ошибка при запросе к NTO API (nto)"
        ) from e


"""
Получение НТО по id.
входные параметры: id обязательный параметр!
"""
def get_nto_by_id(
    id: int,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise NtoError(
            "Параметр 'id' обязателен для запроса /nto/id/"
        )

    params: Dict[str, Any] = {
        "id": id,
    }

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/nto/id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("NTO API error (nto/id)")
        raise NtoError(
            "Ошибка при запросе к NTO API (nto/id)"
        ) from e


"""
Получение списка целей торговых объектов.
"""
def get_nto_purposes(
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
            f"{main_api}/nto/purpose/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("NTO API error (nto/purpose)")
        raise NtoError(
            "Ошибка при запросе к NTO API (nto/purpose)"
        ) from e


"""
Получение списка типов торговли.
"""
def get_nto_trade_types(
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
            f"{main_api}/nto/trade-type/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("NTO API error (nto/trade-type)")
        raise NtoError(
            "Ошибка при запросе к NTO API (nto/trade-type)"
        ) from e


"""
Получение списка типов торговых объектов.
"""
def get_nto_trade_kinds(
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
            f"{main_api}/nto/trade-kind/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("NTO API error (nto/trade-kind)")
        raise NtoError(
            "Ошибка при запросе к NTO API (nto/trade-kind)"
        ) from e


"""
Получение списка разрешённых видов торговли из договора.
"""
def get_nto_name_des(
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
            f"{main_api}/nto/name-des/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("NTO API error (nto/name-des)")
        raise NtoError(
            "Ошибка при запросе к NTO API (nto/name-des)"
        ) from e


if __name__ == "__main__":
    print(get_nto())
    #print(get_nto_by_id(id=38362))
    #print(get_nto_purposes())
    #print(get_nto_trade_types())
    #print(get_nto_trade_kinds())
    print(get_nto_name_des())
    ...
