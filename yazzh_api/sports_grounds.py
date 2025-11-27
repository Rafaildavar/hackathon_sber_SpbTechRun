#Раздел спортплощадки из "https://yazzh.gate.petersburg.ru"
from typing import Optional, List, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"

class SportGroundsError(Exception):
    pass

"""
Получение спортплощадок в соответствии с выбранными фильтрами.
"""
def get_sportgrounds(
    types: Optional[str] = None,
    ovz: Optional[bool] = None,
    light: Optional[bool] = None,
    district: Optional[str] = None,
    season: Optional[str] = "Все", #Лето, Зима, Все
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    page: Optional[int] = 1,
    count: Optional[int] = 10,
    region: Optional[str] = "78",
) -> Dict[str, Any]:

    params: Dict[str, Any] = {
        "types": types,        # вид спорта, через запятую без пробела
        "ovz": ovz,            # особые потребности
        "light": light,        # освещение
        "district": district,  # район
        "season": season,      # сезон активности
        "location_latitude": location_latitude,
        "location_longitude": location_longitude,
        "location_radius": location_radius,
        "page": page,
        "count": count,
    }
    # убираем None
    params = {k: v for k, v in params.items() if v is not None}

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/sportgrounds/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("SportGrounds API error (sportgrounds)")
        raise SportGroundsError(
            "Ошибка при запросе к SportGrounds API (sportgrounds)"
        ) from e


"""
Получение информации о спортплощадке по id.
входные параметры: id спортплощадки обязательный параметр!
"""
def get_sportgrounds_by_id(
    id: Optional[int] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = "78") -> Dict[str, Any]:

    if id is None:
        raise SportGroundsError(
            "Параметр 'id' обязателен для запроса /sportgrounds/id/"
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
            f"{main_api}/sportgrounds/id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("SportGrounds API error (sportgrounds/id)")
        raise SportGroundsError(
            "Ошибка при запросе к SportGrounds API (sportgrounds/id)"
        ) from e


"""
Получение общего количества спортплощадок.
входные параметры: можно оставить без фильтров
"""
def get_sportgrounds_count(
    region: Optional[str] = "78") -> Dict[str, Any]:

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/sportgrounds/count/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("SportGrounds API error (sportgrounds/count)")
        raise SportGroundsError(
            "Ошибка при запросе к SportGrounds API (sportgrounds/count)"
        ) from e

"""
Общее количество спортивных площадок в указанном районе г. Санкт-Петербург.
входные параметры: можно оставить без фильтров
"""
def get_sportgrounds_count_district(
    district: Optional[str] = None,
    region: Optional[str] = "78") -> Dict[str, Any]:

    params: Dict[str, Any] = {
        "district": district,
    }
    params = {k: v for k, v in params.items() if v is not None}

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/sportgrounds/count/district/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("SportGrounds API error (sportgrounds/count/district)")
        raise SportGroundsError(
            "Ошибка при запросе к SportGrounds API (sportgrounds/count/district)"
        ) from e

"""
Виды спорта по сезонам года
(Сезон выбирается на стороне сервиса, здесь только регион.)
без входных параметров
"""
def get_sportgrounds_types() -> Dict[str, Any]:
    headers = {"region": "78"}
    try:
        resp = requests.get(
            f"{main_api}/sportgrounds/types/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("SportGrounds API error (sportgrounds/types)")
        raise SportGroundsError(
            "Ошибка при запросе к SportGrounds API (sportgrounds/types)"
        ) from e

"""
Получение спортплощадок для карты в соответствии с выбранными фильтрами.
входные параметры: можно оставить без фильтров
"""
def get_sportgrounds_map(
    types: Optional[str] = None,
    ovz: Optional[bool] = None,
    light: Optional[bool] = None,
    season: Optional[str] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    region: Optional[str] = "78") -> Dict[str, Any]:

    params: Dict[str, Any] = {
        "types": types,                  # вид спорта, через запятую без пробела
        "ovz": ovz,                      # особые потребности
        "light": light,                  # освещение
        "season": season,                # сезон активности
        "location_latitude": location_latitude,
        "location_longitude": location_longitude,
        "location_radius": location_radius,
    }
    params = {k: v for k, v in params.items() if v is not None}

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/sportgrounds/map/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("SportGrounds API error (sportgrounds/map)")
        raise SportGroundsError(
            "Ошибка при запросе к SportGrounds API (sportgrounds/map)"
        ) from e

if __name__ == "__main__":
    #print(get_sportgrounds())
    #print(get_sportgrounds(season="Лето", ovz=bool("true")))

    #print(get_sportgrounds_by_id(id=619))

    #print(get_sportgrounds_count())

    #print(get_sportgrounds_count_district())
    #print(get_sportgrounds_count_district(district="Приморский"))

    #print(get_sportgrounds_types())

    #print(get_sportgrounds_map())
    print(get_sportgrounds_map(types="Бадминтон,Баскетбол,Бильярд"))

    ...