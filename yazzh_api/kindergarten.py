#Раздел Детские сады из "https://yazzh.gate.petersburg.ru"
from typing import Optional, List, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"

class KindergartenError(Exception):
    pass

"""
Получение детских садов в соответствии с выбранными фильтрами.
входные параметры: можно оставить без фильтров
входные параметры, например: district="Приморский", age_year=3
"""
def get_dou(
    legal_form: Optional[str] = None,
    district: Optional[str] = None,
    age_year: Optional[int] = None,
    age_month: Optional[int] = None,
    group_type: Optional[str] = None,
    group_shift: Optional[str] = None,
    edu_program: Optional[List[str]] = None,   # массив строк
    available_spots: Optional[int] = 1,     # 0 или 1
    disabled_type: Optional[str] = None,
    recovery_type: Optional[str] = None,
    doo_status: Optional[str] = None,
    doutitle: Optional[str] = None,
    app_version: Optional[str] = None) -> Dict[str, Any]:

    params: Dict[str, Any] = {
        "legal_form": legal_form,
        "district": district,
        "age_year": age_year,
        "age_month": age_month,
        "group_type": group_type,
        "group_shift": group_shift,
        "edu_program": edu_program,
        "available_spots": available_spots,
        "disabled_type": disabled_type,
        "recovery_type": recovery_type,
        "doo_status": doo_status,
        "doutitle": doutitle,
    }

    params = {k: v for k, v in params.items() if v is not None}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/dou/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Kindergarten API error (dou)")
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (dou)"
        ) from e

"""
Объекты раздела «Детские сады»
входные параметры: можно оставить без фильтров
"""
def get_dou_by_id(
    building_id: Optional[str] = None,
    group_name: Optional[str] = None,
    doo_full: Optional[str] = "Государственное", #(Государственное/Негосударственное)
    district: Optional[str] = None,
    age_year: Optional[int] = 0,
    age_month: Optional[int] = 0,
    group_type: Optional[str] = None,
    group_shift: Optional[str] = None,
    edu_program: Optional[str] = None,
    available_spots: Optional[int] = 0,   # 0 или 1 — отключено
    disabled_type: Optional[str] = None,
    recovery_type: Optional[str] = None,
    doo_status: Optional[str] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = "78") -> Dict[str, Any]:

    params: Dict[str, Any] = {
        "building_id": building_id,
        "group_name": group_name,
        "doo_full": doo_full,
        "district": district,
        "age_year": age_year,
        "age_month": age_month,
        "group_type": group_type,
        "group_shift": group_shift,
        "edu_program": edu_program,
        "available_spots": available_spots,
        "disabled_type": disabled_type,
        "recovery_type": recovery_type,
        "doo_status": doo_status,
    }
    params = {k: v for k, v in params.items() if v is not None}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/dou/by_id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Kindergarten API error (dou/by_id)")
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (dou/by_id)"
        ) from e

"""
Получение списка всех районов для раздела «Детские сады».
"""
def get_dou_district() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/dou/district/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Kindergarten API error (dou/district)")
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (dou/district)"
        ) from e

"""
Получение списка всех групп
"""
def get_dou_group_name() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/dou/group-name/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Kindergarten API error (/dou/group-name/)")
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (/dou/group-name/)"
        ) from e

"""
Получение списка всех Специфик групп
"""
def get_dou_group_type() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/dou/group-type/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Kindergarten API error (/dou/group-type/)")
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (/dou/group-type/)"
        ) from e

"""
Получение списка всех Режимов работы групп
"""
def get_dou_group_shift() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/dou/group-shift/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Kindergarten API error (/dou/group-shift/)")
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (/dou/group-shift/)"
        ) from e

"""
Получение списка всех Видов образовательных программ
"""
def get_dou_edu_program() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/dou/edu-program/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Kindergarten API error (/dou/edu-program/)")
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (/dou/edu-program/)"
        ) from e

"""
Получение списка всех Типов групп с ОВЗ
"""
def get_dou_disabled_type() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/dou/disabled-type/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Kindergarten API error (/dou/disabled-type/)")
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (/dou/disabled-type/)"
        ) from e

"""
Получение списка всех Типов оздоровительных
"""
def get_dou_recovery_type() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/dou/recovery-type/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Kindergarten API error (/dou/recovery-type/)")
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (/dou/recovery-type/)"
        ) from e

"""
Получение списка всех Типов принадлежности детских садов
"""
def get_dou_legal_form() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/dou/legal-form/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Kindergarten API error (/dou/legal-form/)")
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (/dou/legal-form/)"
        ) from e

"""
не работает
Получение списка всех типов групп с ОВЗ, относящихся к указанной специфике группы.
def get_dou_group_type_disabled_type(
    group_type: Optional[str] = None,
    app_version: Optional[str] = None) -> Dict[str, Any]:

    params: Dict[str, Any] = {"group_type": group_type}
    params = {k: v for k, v in params.items() if v is not None}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/dou/group-type/disabled-type/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Kindergarten API error (dou/group-type/disabled-type)")
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (dou/group-type/disabled-type)"
        ) from e
"""

"""
Общая сумма свободных мест в детских садах СПБ
"""
def get_dou_available_spots() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/dou/available-spots/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Kindergarten API error (/dou/available-spots/)")
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (/dou/available-spots/)"
        ) from e

"""
Общая сумма свободных мест в детских садах в указанном районе г. Санкт-Петербург.
входные параметры: можно оставить без фильтров, или например district="Центральный"
"""
def get_dou_available_spots_district(
    district: Optional[str] = None,
    app_version: Optional[str] = None) -> Dict[str, Any]:

    params: Dict[str, Any] = {
        "district": district,
    }
    params = {k: v for k, v in params.items() if v is not None}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/dou/available-spots/district/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(
            "Kindergarten API error (dou/available-spots/district)"
        )
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (dou/available-spots/district)"
        ) from e

"""
Получение списка всех сокращенных наименований детских садов
"""
def get_dou_dou_title() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/dou/dou-title/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Kindergarten API error (/dou/dou-title/)")
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (/dou/dou-title/)"
        ) from e

"""
Получение списка всех ответственных организаций по району.
входные параметры: district - район обязательный параметр!
"""
def get_dou_commissions(district: str) -> Dict[str, Any]:
    if district is None:
        raise KindergartenError(
            "Параметр 'district' обязателен для запроса /dou/commissions/"
        )

    params: Dict[str, Any] = {
        "district": district,
    }

    try:
        resp = requests.get(
            f"{main_api}/dou/commissions/",
            params=params,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Kindergarten API error (dou/commissions)")
        raise KindergartenError(
            "Ошибка при запросе к Kindergarten API (dou/commissions)"
        ) from e

if __name__ == "__main__":
    # Все гос. сады в Приморском районе для ребёнка 3 лет
    #print(get_dou(district="Приморский", age_year=3))
    #print(get_dou())

    #print(get_dou_by_id(district="приморский"))

    #print(get_dou_district())
    #print(get_dou_group_name())
    #print(get_dou_group_type())
    #print(get_dou_group_shift())
    #print(get_dou_edu_program())
    #print(get_dou_disabled_type())
    #print(get_dou_recovery_type())
    #print(get_dou_legal_form())

    #print(get_dou_available_spots())

    #print(get_dou_available_spots_district())
    #print(get_dou_available_spots_district(district="Центральный"))

    #print(get_dou_dou_title())
    print(get_dou_commissions("Центральный"))
    ...