# Раздел Информация об МФЦ (ЭГС) из "https://yazzh.gate.petersburg.ru"
from typing import Optional, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class MfcEgsError(Exception):
    pass


"""
Выводит перечень всех МФЦ.
"""
def get_mfc_all(
    region: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/mfc/all/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MfcEgs API error (mfc/all)")
        raise MfcEgsError(
            "Ошибка при запросе к MfcEgs API (mfc/all)"
        ) from e


"""
Список МФЦ по району.
"""
def get_mfc_by_district(
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
            f"{main_api}/mfc/district/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MfcEgs API error (mfc/district)")
        raise MfcEgsError(
            "Ошибка при запросе к MfcEgs API (mfc/district)"
        ) from e


"""
Информация об адресе и координатах МФЦ по building_id.
building_id обязательное поле
"""
def get_mfc_by_building_id(
    id_building: str,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if id_building is not None:
        params["id_building"] = id_building

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/mfc/id_building/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MfcEgs API error (mfc/id_building)")
        raise MfcEgsError(
            "Ошибка при запросе к MfcEgs API (mfc/id_building)"
        ) from e


"""
Показывает информацию конкретного МФЦ по ID.
входные параметры: id_mfc обязательный параметр!
"""
def get_mfc_by_id(
    id_mfc: int,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id_mfc is None:
        raise MfcEgsError(
            "Параметр 'id_mfc' обязателен для запроса /mfc/id_mfc/"
        )

    params: Dict[str, Any] = {"id_mfc": id_mfc}

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/mfc/id_mfc/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MfcEgs API error (mfc/id_mfc)")
        raise MfcEgsError(
            "Ошибка при запросе к MfcEgs API (mfc/id_mfc)"
        ) from e


if __name__ == "__main__":
    # print(get_mfc_all())
    #print(get_mfc_by_district(district="Адмиралтейский"))
    #print(get_mfc_by_district())

    #print(get_mfc_by_building_id(id_building="210836"))

    print(get_mfc_by_id(id_mfc=1))
    ...
