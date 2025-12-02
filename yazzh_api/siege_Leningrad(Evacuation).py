# Раздел "Блокада Ленинграда («Эвакуация»)" из "https://yazzh.gate.petersburg.ru"
from typing import Optional, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

main_api = "https://yazzh.gate.petersburg.ru"

class EvacuationError(Exception):
    pass

"""
Количество эвакуированных.
"""
def get_evacuation_count() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/evacuation/count/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Evacuation API error (evacuation/count/)")
        raise EvacuationError(
            "Ошибка при запросе к Evacuation API (evacuation/count/)"
        ) from e


"""
Статьи об эвакуации.
"""
def get_evacuation_photos(
    user_id: Optional[str] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/evacuation/photos/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Evacuation API error (evacuation/photos/)")
        raise EvacuationError(
            "Ошибка при запросе к Evacuation API (evacuation/photos/)"
        ) from e

if __name__ == "__main__":
    print(get_evacuation_count())
    print(get_evacuation_photos())
    ...