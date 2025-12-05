# Раздел Школы: Запись в первые классы из "https://yazzh.gate.petersburg.ru"
from typing import Optional, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class SchoolError(Exception):
    pass


"""
Вид организации (справочник).
"""
def get_school_kinds(
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/school/kind/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("School API error (school/kind/)")
        raise SchoolError(
            "Ошибка при запросе к School API (school/kind/)"
        ) from e


"""
Справочник по профилям школ (Естественно-научный, Гуманитарный и т.п.).
"""
def get_school_profiles(
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/school/profile/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("School API error (school/profile/)")
        raise SchoolError(
            "Ошибка при запросе к School API (school/profile/)"
        ) from e


"""
Метод для карты школ.
Фильтры:
- org_type — вид организации (Гимназия, Лицей и т.п.)
- profile — профиль (Естественно-научный, Гуманитарный и т.п.)
- subject — специализация (Математика, Физика и т.д.)
- available_spots — наличие свободных мест (0/1, только для scheme=1)
- scheme=1 — период набора 2-й волны; scheme=2 — остальной период.
"""
def get_school_map(
    org_type: Optional[str] = None,
    profile: Optional[str] = None,
    subject: Optional[str] = None,
    available_spots: Optional[int] = None,
    scheme: Optional[int] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if org_type is not None:
        params["org_type"] = org_type
    if profile is not None:
        params["profile"] = profile
    if subject is not None:
        params["subject"] = subject
    if available_spots is not None:
        params["available_spots"] = available_spots
    if scheme is not None:
        params["scheme"] = scheme

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/school/map/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("School API error (school/map/)")
        raise SchoolError(
            "Ошибка при запросе к School API (school/map/)"
        ) from e


"""
Объект раздела Школы по id.
Параметр id обязателен.
Параметр scheme:
- scheme=1 — период набора 2-й волны;
- scheme=2 — остальной период.
"""
def get_school_by_id(
    id: int,
    scheme: Optional[int] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise SchoolError(
            "Параметр 'id' обязателен для запроса /school/{id}"
        )

    params: Dict[str, Any] = {}
    if scheme is not None:
        params["scheme"] = scheme

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/school/{id}",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("School API error (school/{id})")
        raise SchoolError(
            "Ошибка при запросе к School API (school/{id})"
        ) from e


"""
Метод статистики (только для scheme=1), возвращающий данные по свободным местам в 1-х классах.
Можно фильтровать по району.
"""
def get_school_stat(
    district: Optional[str] = None,
    scheme: Optional[int] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if district is not None:
        params["district"] = district
    if scheme is not None:
        params["scheme"] = scheme

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/school/stat/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("School API error (school/stat/)")
        raise SchoolError(
            "Ошибка при запросе к School API (school/stat/)"
        ) from e


"""
Метод по конфликтным комиссиям.
Параметр district обязателен (район города).
"""
def get_school_commissions(
    district: str,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    if district is None:
        raise SchoolError(
            "Параметр 'district' обязателен для запроса /school/commissions/"
        )

    params: Dict[str, Any] = {"district": district}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/school/commissions/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("School API error (school/commissions/)")
        raise SchoolError(
            "Ошибка при запросе к School API (school/commissions/)"
        ) from e


"""
Справочник по специализациям (предметам).
"""
def get_school_subjects(
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/school/subject/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("School API error (school/subject/)")
        raise SchoolError(
            "Ошибка при запросе к School API (school/subject/)"
        ) from e


"""
Полезная информация по разделу «Школы».
"""
def get_school_helpful(
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/school/helpful/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("School API error (school/helpful/)")
        raise SchoolError(
            "Ошибка при запросе к School API (school/helpful/)"
        ) from e


"""
Общая сумма свободных мест в школах в указанном районе г. Санкт-Петербург.
"""
def get_available_spots_by_district(
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
            f"{main_api}/school/available-spots/district/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("School API error (school/available-spots/district/)")
        raise SchoolError(
            "Ошибка при запросе к School API (school/available-spots/district/)"
        ) from e


"""
Общая сумма свободных мест в школах по адресу (building_id или fias_id дома).
Параметр building_id обязателен.
Параметр scheme:
- scheme=1 — период набора 2-й волны;
- scheme=2 — остальной период.
"""
def get_linked_schools(
    building_id: str,
    scheme: Optional[int] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    if building_id is None:
        raise SchoolError(
            "Параметр 'building_id' обязателен для запроса /school/linked/{building_id}"
        )

    params: Dict[str, Any] = {}
    if scheme is not None:
        params["scheme"] = scheme

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/school/linked/{building_id}",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("School API error (school/linked/{building_id})")
        raise SchoolError(
            "Ошибка при запросе к School API (school/linked/{building_id})"
        ) from e


"""
Объекты раздела Школы по ОГРН.
Параметр ogrn обязателен.
"""
def get_school_by_ogrn(
    ogrn: str,
) -> Dict[str, Any]:
    if ogrn is None:
        raise SchoolError(
            "Параметр 'ogrn' обязателен для запроса /school/ogrn/{ogrn}"
        )

    try:
        resp = requests.get(
            f"{main_api}/school/ogrn/{ogrn}",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("School API error (school/ogrn/{ogrn})")
        raise SchoolError(
            "Ошибка при запросе к School API (school/ogrn/{ogrn})"
        ) from e


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        kinds = get_school_kinds()
        logger.info("Виды организаций (пример): %s", str(kinds)[:300])

        profiles = get_school_profiles()
        logger.info("Профили школ (пример): %s", str(profiles)[:300])

        subjects = get_school_subjects()
        logger.info("Специализации (пример): %s", str(subjects)[:300])

        helpful = get_school_helpful()
        logger.info("Полезная информация (пример): %s", str(helpful)[:300])

        school_map = get_school_map(
            org_type="Гимназия",
            profile="Гуманитарный",
            scheme=2,
        )
        logger.info("Карта школ (пример): %s", str(school_map)[:300])

        stat = get_school_stat(district="Адмиралтейский", scheme=1)
        logger.info("Статистика по свободным местам (пример): %s", str(stat)[:300])

        available = get_available_spots_by_district(district="Адмиралтейский")
        logger.info(
            "Свободные места по району (пример): %s",
            str(available)[:300],
        )

        commissions = get_school_commissions(district="Адмиралтейский")
        logger.info("Конфликтные комиссии (пример): %s", str(commissions)[:300])

        # Примеры запросов, требующих реальных id/ogrn:
        school = get_school_by_id(id=73)
        logger.info("Школа по id (пример): %s", str(school)[:300])

        # building_id можно получить по адресу пользователя исп функцию из yazzh_api.py -> get_building_id_by_address()
        linked = get_linked_schools(building_id="210836")
        logger.info("Школы по адресу (пример): %s", str(linked))

        by_ogrn = get_school_by_ogrn(ogrn="1027807585300")
        logger.info("Школы по ОГРН (пример): %s", str(by_ogrn)[:300])

    except SchoolError as e:
        logger.error("School API test failed: %s", e)
