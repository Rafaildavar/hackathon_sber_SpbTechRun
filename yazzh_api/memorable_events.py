#Раздел Памятные события из "https://yazzh.gate.petersburg.ru"
from typing import Optional, List, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"

class MemorableEventsError(Exception):
    pass

"""
Получение списка всех памятных событий.
"""
def get_memorable_dates() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/memorable_dates/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MemorableEvents API error (memorable_dates)")
        raise MemorableEventsError(
            "Ошибка при запросе к MemorableEvents API (memorable_dates)"
        ) from e

"""
Получение информации о памятном событии по ID.
входные параметры: id события обязательный параметр!
"""
def get_memorable_dates_by_ids(ids: int) -> Dict[str, Any]:
    if ids is None:
        raise MemorableEventsError(
            "Параметр 'ids' обязателен для запроса /memorable_dates/ids/"
        )

    params: Dict[str, Any] = {"ids": ids}
    try:
        resp = requests.get(
            f"{main_api}/memorable_dates/ids/",
            params=params,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MemorableEvents API error (memorable_dates/ids)")
        raise MemorableEventsError(
            "Ошибка при запросе к MemorableEvents API (memorable_dates/ids)"
        ) from e

"""
Получение списка памятных событий по дате.
входные параметры: day и month обязательные параметры!
"""
def get_memorable_dates_by_date(day: int, month: int) -> Dict[str, Any]:
    params: Dict[str, Any] = {
        "day": day,
        "month": month,
    }

    try:
        resp = requests.get(
            f"{main_api}/memorable_dates/date/",
            params=params,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MemorableEvents API error (memorable_dates/date)")
        raise MemorableEventsError(
            "Ошибка при запросе к MemorableEvents API (memorable_dates/date)"
        ) from e

if __name__ == "__main__":
    #print(get_memorable_dates())
    #print(get_memorable_dates_by_ids(1))
    print(get_memorable_dates_by_date(day=23, month=2))
    ...