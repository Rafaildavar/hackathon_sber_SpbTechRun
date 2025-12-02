# Раздел Новости из "https://yazzh.gate.petersburg.ru"
from typing import Optional, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class NewsError(Exception):
    pass


"""
Получение списка новостей в соответствии с выбранными фильтрами.
Параметры building и district взаимно исключают друг друга.
"""
def get_news(
    yazzh_type: Optional[str] = None,
    building: Optional[str] = None,
    district: Optional[str] = None,
    description: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if yazzh_type is not None:
        params["yazzh_type"] = yazzh_type
    if building is not None:
        params["building"] = building
    if district is not None:
        params["district"] = district
    if description is not None:
        params["description"] = description
    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date
    if page is not None:
        params["page"] = page
    if count is not None:
        params["count"] = count

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/news/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("News API error (news/)")
        raise NewsError(
            "Ошибка при запросе к News API (news/)"
        ) from e


"""
Объект раздела Новости по id.
входные параметры: id обязательный параметр!
формат id: id,type (ЭГС, Городские, Районные, Муниципальные)
"""
def get_news_by_id(
    id: str,
    region_id: Optional[str] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if id is None:
        raise NewsError(
            "Параметр 'id' обязателен для запроса /news/id/"
        )

    params: Dict[str, Any] = {"id": id}
    if region_id is not None:
        params["region_id"] = region_id

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/news/id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("News API error (news/id/)")
        raise NewsError(
            "Ошибка при запросе к News API (news/id/)"
        ) from e


"""
Получение списка всех ролей для новостей.
"""
def get_news_roles(
    region: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/news/role/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("News API error (news/role/)")
        raise NewsError(
            "Ошибка при запросе к News API (news/role/)"
        ) from e


"""
Получение списка всех районов для фильтра новостей.
"""
def get_news_districts(
    region: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/news/districts/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("News API error (news/districts/)")
        raise NewsError(
            "Ошибка при запросе к News API (news/districts/)"
        ) from e


"""
Получение списка ТОП новостей в соответствии с выбранными фильтрами.
входные параметры: district и start_date обязательные параметры!
"""
def get_top_news(
    district: str,
    start_date: str,
    page: Optional[int] = None,
    count: Optional[int] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if district is None:
        raise NewsError(
            "Параметр 'district' обязателен для запроса /news/top"
        )

    params: Dict[str, Any] = {"district": district}
    if start_date is not None:
        params["start_date"] = start_date
    if page is not None:
        params["page"] = page
    if count is not None:
        params["count"] = count

    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/news/top",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("News API error (news/top)")
        raise NewsError(
            "Ошибка при запросе к News API (news/top)"
        ) from e


if __name__ == "__main__":
    #print(get_news())
    #print(get_news(yazzh_type="Студенчество", district="Адмиралтейский"))

    #print(get_news_by_id(id="86914,Районные"))
    print(get_news_roles())
    print(get_news_districts())
    print(get_top_news(district="Адмиралтейский", start_date="2025-11-21"))
    ...
