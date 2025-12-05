# Раздел Объекты культурного наследия (ОКН) из "https://yazzh.gate.petersburg.ru"
from typing import Optional, List, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"

class OknError(Exception):
    pass

"""
Получение списка ОКН по building_id.
входные параметры: building_id обязательный параметр!
"""
def get_okn_by_building_id(
    building_id: str,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if building_id is None:
        raise OknError(
            "Параметр 'building_id' обязателен для запроса /okn/"
        )

    params: Dict[str, Any] = {
        "building_id": building_id,
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
            f"{main_api}/okn/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Okn API error (okn)")
        raise OknError(
            "Ошибка при запросе к Okn API (okn)"
        ) from e


"""
Получение ОКН по id.
входные параметры: id обязательный параметр!
"""
def get_okn_by_id(id: int) -> Dict[str, Any]:
    if id is None:
        raise OknError(
            "Параметр 'id' обязателен для запроса /okn/id/"
        )

    params: Dict[str, Any] = {
        "id": id,
    }

    try:
        resp = requests.get(
            f"{main_api}/okn/id/",
            params=params,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Okn API error (okn/id)")
        raise OknError(
            "Ошибка при запросе к Okn API (okn/id)"
        ) from e

if __name__ == "__main__":
    print(get_okn_by_building_id(building_id="54524"))
    print(get_okn_by_id(id=165))