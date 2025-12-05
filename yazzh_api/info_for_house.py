# Раздел Справка по дому из "https://yazzh.gate.petersburg.ru"
from typing import Optional, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class HouseInfoError(Exception):
    pass


"""
Фальсификация (раздел "Справка по дому").
"""
def get_uk_falsification(
    region: Optional[str] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id

    try:
        resp = requests.get(
            f"{main_api}/uk-falsification/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("HouseInfo API error (uk-falsification/)")
        raise HouseInfoError(
            "Ошибка при запросе к HouseInfo API (uk-falsification/)"
        ) from e


"""
Районная справка по building_id.
Параметр id (Номер building_id) обязателен.
"""
def get_district_info_by_building_id(
    id: str,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise HouseInfoError(
            "Параметр 'id' обязателен для запроса /districts-info/building-id/{id}"
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
            f"{main_api}/districts-info/building-id/{id}",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("HouseInfo API error (districts-info/building-id/{id})")
        raise HouseInfoError(
            "Ошибка при запросе к HouseInfo API (districts-info/building-id/{id})"
        ) from e


"""
Районная справка по наименованию района.
Параметр district_name обязателен.
"""
def get_district_info_by_district(
    district_name: str,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if district_name is None:
        raise HouseInfoError(
            "Параметр 'district_name' обязателен для запроса /districts-info/district/"
        )

    params: Dict[str, Any] = {"district_name": district_name}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/districts-info/district/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("HouseInfo API error (districts-info/district/)")
        raise HouseInfoError(
            "Ошибка при запросе к HouseInfo API (districts-info/district/)"
        ) from e


"""
Отключение горячей воды и электроэнергии по дому.
Параметр id обязателен.
"""
def get_disconnections(
    id: str,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise HouseInfoError(
            "Параметр 'id' обязателен для запроса /disconnections/"
        )

    params: Dict[str, Any] = {"id": id}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/disconnections/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("HouseInfo API error (disconnections/)")
        raise HouseInfoError(
            "Ошибка при запросе к HouseInfo API (disconnections/)"
        ) from e


"""
МФЦ, привязанные к дому по building_id.
Параметр id_building обязателен.
"""
def get_house_mfc(
    id_building: str,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id_building is None:
        raise HouseInfoError(
            "Параметр 'id_building' обязателен для запроса /mfc/"
        )

    params: Dict[str, Any] = {"id_building": id_building}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/mfc/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("HouseInfo API error (mfc/)")
        raise HouseInfoError(
            "Ошибка при запросе к HouseInfo API (mfc/)"
        ) from e


"""
Ближайшие МФЦ для заданных координат.
Параметр user_pos обязателен.
Формат user_pos: 'longitude latitude'.
"""
def get_nearest_mfc(
    user_pos: str,
    distance: Optional[int] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if user_pos is None:
        raise HouseInfoError(
            "Параметр 'user_pos' обязателен для запроса /mfc/nearest"
        )

    params: Dict[str, Any] = {"user_pos": user_pos}
    if distance is not None:
        params["distance"] = distance

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/mfc/nearest",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("HouseInfo API error (mfc/nearest)")
        raise HouseInfoError(
            "Ошибка при запросе к HouseInfo API (mfc/nearest)"
        ) from e


"""
Поликлиники, привязанные к дому по building_id.
Параметр id обязателен.
"""
def get_polyclinics(
    id: str,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise HouseInfoError(
            "Параметр 'id' обязателен для запроса /polyclinics/"
        )

    params: Dict[str, Any] = {"id": id}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/polyclinics/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("HouseInfo API error (polyclinics/)")
        raise HouseInfoError(
            "Ошибка при запросе к HouseInfo API (polyclinics/)"
        ) from e


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        falsification = get_uk_falsification()
        logger.info("Фальсификация УК (пример): %s", str(falsification)[:300])

        district_info = get_district_info_by_district(district_name="Адмиралтейский")
        logger.info("Районная справка по району (пример): %s", str(district_info)[:300])

        # Пример building_id можно получить по адресу пользователя исп функцию из yazzh_api.py -> get_building_id_by_address()
        building_info = get_district_info_by_building_id(id="210836")
        logger.info("Районная справка по building_id (пример): %s", str(building_info)[:300])

        mfc = get_house_mfc(id_building="210836")
        logger.info("МФЦ (пример): %s", str(mfc)[:300])

        nearest_mfc = get_nearest_mfc(user_pos="30.314130 59.938630", distance=2)
        logger.info("Ближайшие МФЦ (пример): %s", str(nearest_mfc)[:300])

        # Пример building_id можно получить по адресу пользователя исп функцию из yazzh_api.py -> get_building_id_by_address()
        polys = get_polyclinics(id="210836")
        logger.info("Поликлиники по дому (пример): %s", str(polys)[:300])

    except HouseInfoError as e:
        logger.error("HouseInfo API test failed: %s", e)
