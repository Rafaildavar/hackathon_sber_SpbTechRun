# Раздел Я родитель (Дополнительное образование, внешний) из "https://yazzh.gate.petersburg.ru"
from typing import Optional, List, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class ExternalEduError(Exception):
    pass


"""
Получение количества кружков и секций по районам, и общего количества.
"""
def get_external_edu_district_count(
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
            f"{main_api}/api/v2/external/edu/district/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "ExternalEdu API error (api/v2/external/edu/district)"
        )
        raise ExternalEduError(
            "Ошибка при запросе к ExternalEdu API (api/v2/external/edu/district)"
        ) from e


"""
Возвращает список районов по базе справочника доп. образования с учетом фильтра по имени.
"""
def get_external_edu_districts(
    search: Optional[str] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if search is not None:
        params["search"] = search

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/api/v2/external/edu/districts",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "ExternalEdu API error (api/v2/external/edu/districts)"
        )
        raise ExternalEduError(
            "Ошибка при запросе к ExternalEdu API (api/v2/external/edu/districts)"
        ) from e


"""
Возвращает список программ дополнительного образования в соответствии с фильтрами.
"""
def get_external_edu_programs(
    age: Optional[int] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: Optional[int] = None,
    address: Optional[str] = None,
    directivity: Optional[str] = None,
    district: Optional[int] = None,
    is_ovz: Optional[str] = None,
    search_name: Optional[str] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    age_range_min: Optional[int] = None,
    age_range_max: Optional[int] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if age is not None:
        params["age"] = age
    if latitude is not None:
        params["latitude"] = latitude
    if longitude is not None:
        params["longitude"] = longitude
    if radius is not None:
        params["radius"] = radius
    if address is not None:
        params["address"] = address
    if directivity is not None:
        params["directivity"] = directivity
    if district is not None:
        params["district"] = district
    if is_ovz is not None:
        params["is_ovz"] = is_ovz
    if search_name is not None:
        params["search_name"] = search_name
    if page is not None:
        params["page"] = page
    if count is not None:
        params["count"] = count
    if age_range_min is not None:
        params["age_range_min"] = age_range_min
    if age_range_max is not None:
        params["age_range_max"] = age_range_max

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/api/v2/external/edu/programs",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "ExternalEdu API error (api/v2/external/edu/programs)"
        )
        raise ExternalEduError(
            "Ошибка при запросе к ExternalEdu API (api/v2/external/edu/programs)"
        ) from e


"""
Возвращает данные о программе дополнительного образования по ее идентификатору.
входные параметры: program_id обязательный параметр!
"""
def get_external_edu_program_by_id(
    program_id: int,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if program_id is None:
        raise ExternalEduError(
            "Параметр 'program_id' обязателен для запроса /api/v2/external/edu/program/{program_id}"
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
            f"{main_api}/api/v2/external/edu/program/{program_id}",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "ExternalEdu API error (api/v2/external/edu/program/{program_id})"
        )
        raise ExternalEduError(
            "Ошибка при запросе к ExternalEdu API (api/v2/external/edu/program/{program_id})"
        ) from e


"""
Возвращает список directivity (направленностей кружков).
"""
def get_external_edu_directivity_list() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/api/v2/edu/directivity/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "ExternalEdu API error (api/v2/edu/directivity)"
        )
        raise ExternalEduError(
            "Ошибка при запросе к ExternalEdu API (api/v2/edu/directivity)"
        ) from e


"""
Метод для поиска. Получение списка всех наименований кружков.
"""
def get_external_edu_search_names(
    search_name: Optional[str] = None,
    age: Optional[int] = None,
    radius: Optional[int] = None,
    address: Optional[str] = None,
    directivity: Optional[str] = None,
    is_ovz: Optional[str] = None,
    age_range_min: Optional[int] = None,
    age_range_max: Optional[int] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if search_name is not None:
        params["search_name"] = search_name
    if age is not None:
        params["age"] = age
    if radius is not None:
        params["radius"] = radius
    if address is not None:
        params["address"] = address
    if directivity is not None:
        params["directivity"] = directivity
    if is_ovz is not None:
        params["is_ovz"] = is_ovz
    if age_range_min is not None:
        params["age_range_min"] = age_range_min
    if age_range_max is not None:
        params["age_range_max"] = age_range_max

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/api/v2/search_name/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "ExternalEdu API error (api/v2/search_name)"
        )
        raise ExternalEduError(
            "Ошибка при запросе к ExternalEdu API (api/v2/search_name)"
        ) from e


if __name__ == "__main__":
    #print(get_external_edu_district_count())

    #print(get_external_edu_districts())
    #print(get_external_edu_districts(search="Центральный"))

    #print(get_external_edu_programs())
    #print(get_external_edu_program_by_id(program_id=12475))
    print(get_external_edu_directivity_list())

    print(get_external_edu_search_names(search_name="футбол", age=10))
    print(get_external_edu_search_names())
