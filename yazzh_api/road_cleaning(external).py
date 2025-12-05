# Раздел Уборка дорог (внешний) из "https://yazzh.gate.petersburg.ru"
from typing import Optional, List, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class ExternalDusError(Exception):
    pass


"""
Возвращает данные по уборочному транспорту вокруг точки с заданными координатами.
"""
def get_external_dus_vehicles_around(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if latitude is not None:
        params["latitude"] = latitude
    if longitude is not None:
        params["longitude"] = longitude

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/api/v2/external/dus/get-vehicles-around",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "ExternalDus API error (api/v2/external/dus/get-vehicles-around)"
        )
        raise ExternalDusError(
            "Ошибка при запросе к ExternalDus API (api/v2/external/dus/get-vehicles-around)"
        ) from e


"""
Возвращает данные по организациям вокруг точки с заданными координатами.
"""
def get_external_dus_organisations_around(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if latitude is not None:
        params["latitude"] = latitude
    if longitude is not None:
        params["longitude"] = longitude

    try:
        resp = requests.get(
            f"{main_api}/api/v2/external/dus/get-organisations-around",
            params=params,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "ExternalDus API error (api/v2/external/dus/get-organisations-around)"
        )
        raise ExternalDusError(
            "Ошибка при запросе к ExternalDus API (api/v2/external/dus/get-organisations-around)"
        ) from e


"""
Возвращает данные по количеству убранного снега за последние три года.
"""
def get_external_dus_snow_for_last_three_years() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/api/v2/external/dus/get-snow-for-last-three-years",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "ExternalDus API error (api/v2/external/dus/get-snow-for-last-three-years)"
        )
        raise ExternalDusError(
            "Ошибка при запросе к ExternalDus API (api/v2/external/dus/get-snow-for-last-three-years)"
        ) from e


"""
Возвращает данные по количеству убранного снега за предыдущие сутки.
"""
def get_external_dus_snow_for_previous_day() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/api/v2/external/dus/get-snow-for-previous-day",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "ExternalDus API error (api/v2/external/dus/get-snow-for-previous-day)"
        )
        raise ExternalDusError(
            "Ошибка при запросе к ExternalDus API (api/v2/external/dus/get-snow-for-previous-day)"
        ) from e


"""
Возвращает данные по маршрутам уборочной техники вокруг точки с заданными координатами.
"""
def get_external_dus_tracks_around(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    feets: Optional[int] = None,
    count: Optional[int] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if latitude is not None:
        params["latitude"] = latitude
    if longitude is not None:
        params["longitude"] = longitude
    if feets is not None:
        params["feets"] = feets
    if count is not None:
        params["count"] = count

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/api/v2/external/dus/get-tracks-around",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "ExternalDus API error (api/v2/external/dus/get-tracks-around)"
        )
        raise ExternalDusError(
            "Ошибка при запросе к ExternalDus API (api/v2/external/dus/get-tracks-around)"
        ) from e


"""
Возвращает текущий сезон времени года (Лето или Зима).
"""
def get_external_dus_season(
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/api/v2/external/dus/get-season/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "ExternalDus API error (api/v2/external/dus/get-season/)"
        )
        raise ExternalDusError(
            "Ошибка при запросе к ExternalDus API (api/v2/external/dus/get-season/)"
        ) from e


if __name__ == "__main__":
    print(get_external_dus_vehicles_around(latitude=59.935658, longitude=30.32772))

    print(get_external_dus_organisations_around(latitude=59.935658, longitude=30.32772))
    print(get_external_dus_snow_for_last_three_years())
    print(get_external_dus_snow_for_previous_day())
    #print(get_external_dus_tracks_around(latitude=59.935658, longitude=30.32772))
    print(get_external_dus_season())

