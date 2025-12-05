# Раздел Блокада Ленинграда из "https://yazzh.gate.petersburg.ru"
from typing import Optional, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"


class BlockadeError(Exception):
    pass


"""
Фотографии Блокадного Ленинграда.
Возвращает массив фото и комментарии к ним в случайном порядке
(период обновления примерно 1 минута).
"""
def get_blockade_photos(
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
            f"{main_api}/blocade/photos/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Blockade API error (blocade/photos/)")
        raise BlockadeError(
            "Ошибка при запросе к Blockade API (blocade/photos/)"
        ) from e


"""
Общее количество медалей «За оборону Ленинграда».
"""
def get_blockade_medals_count() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/blocade/medals/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Blockade API error (blocade/medals/)")
        raise BlockadeError(
            "Ошибка при запросе к Blockade API (blocade/medals/)"
        ) from e


"""
Медаль памяти — поиск награжденных.

Можно фильтровать по:
- place_id: id организации,
- place: место работы,
- birth: точный год рождения,
- birth_start / birth_end: диапазон годов рождения,
- name: ФИО награжденного (регистронезависимый поиск по неполному совпадению),
а также задавать пагинацию (page, count) и region_id для шеринга.
"""
def get_blockade_persons(
    place_id: Optional[int] = None,
    place: Optional[str] = None,
    birth: Optional[int] = None,
    birth_start: Optional[int] = None,
    birth_end: Optional[int] = None,
    name: Optional[str] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    region_id: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if place_id is not None:
        params["place_id"] = place_id
    if place is not None:
        params["place"] = place
    if birth is not None:
        params["birth"] = birth
    if birth_start is not None:
        params["birth_start"] = birth_start
    if birth_end is not None:
        params["birth_end"] = birth_end
    if name is not None:
        params["name"] = name
    if page is not None:
        params["page"] = page
    if count is not None:
        params["count"] = count
    if region_id is not None:
        params["region_id"] = region_id

    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/blocade/persons/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Blockade API error (blocade/persons/)")
        raise BlockadeError(
            "Ошибка при запросе к Blockade API (blocade/persons/)"
        ) from e


"""
Места работы награжденных.

Можно отфильтровать по части названия места работы (place)
и управлять пагинацией (page, count).
"""
def get_blockade_person_places(
    place: Optional[str] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    user_id: Optional[str] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if place is not None:
        params["place"] = place
    if page is not None:
        params["page"] = page
    if count is not None:
        params["count"] = count

    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/blocade/persons/place/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Blockade API error (blocade/persons/place/)")
        raise BlockadeError(
            "Ошибка при запросе к Blockade API (blocade/persons/place/)"
        ) from e


"""
Мини-истории о блокаде.

Без параметра name возвращает случайную подборку историй.
При указании name — подборку историй с совпадением ФИО
(регистронезависимый поиск по неполному совпадению).
"""
def get_blockade_stories(
    name: Optional[str] = None,
    page: Optional[int] = None,
    count: Optional[int] = None,
    user_id: Optional[str] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if name is not None:
        params["name"] = name
    if page is not None:
        params["page"] = page
    if count is not None:
        params["count"] = count

    headers: Dict[str, str] = {}
    if user_id is not None:
        headers["user-id"] = user_id
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/blocade/story/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Blockade API error (blocade/story/)")
        raise BlockadeError(
            "Ошибка при запросе к Blockade API (blocade/story/)"
        ) from e

"""
Объекты раздела Карта по выбранным типам в заданном радиусе.
Параметры:
- obj_types: строка с типами объектов через запятую без пробела.
  Если не указано — будут выбраны объекты всех типов
  (справочник типов: /blocade/map_items/obj_types/).
- working: отображение функционирующих организаций:
    1 — функционирует,
    0 — не функционирует,
    None — все объекты.
- location_latitude / location_longitude: координаты центра поиска.
- location_radius: радиус поиска в км (до 160).
"""
def get_blockade_map_items_by_radius(
    obj_types: Optional[str] = None,
    working: Optional[int] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if obj_types is not None:
        params["obj_types"] = obj_types
    if working is not None:
        params["working"] = working
    if location_latitude is not None:
        params["location_latitude"] = location_latitude
    if location_longitude is not None:
        params["location_longitude"] = location_longitude
    if location_radius is not None:
        params["location_radius"] = location_radius

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/blocade/map_items/by_radius/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Blockade API error (blocade/map_items/by_radius/)")
        raise BlockadeError(
            "Ошибка при запросе к Blockade API (blocade/map_items/by_radius/)"
        ) from e


"""
Объект раздела Карта по id.
Входной параметр object_id обязателен.
"""
def get_blockade_map_item_by_id(
    object_id: int,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if object_id is None:
        raise BlockadeError(
            "Параметр 'object_id' обязателен для запроса /blocade/map_items/by_id/"
        )

    params: Dict[str, Any] = {"object_id": object_id}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/blocade/map_items/by_id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Blockade API error (blocade/map_items/by_id/)")
        raise BlockadeError(
            "Ошибка при запросе к Blockade API (blocade/map_items/by_id/)"
        ) from e


"""
Типы объектов раздела Карта.
Используется для фильтрации в /blocade/map_items/by_radius/.
"""
def get_blockade_map_obj_types(
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/blocade/map_items/obj_types/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Blockade API error (blocade/map_items/obj_types/)")
        raise BlockadeError(
            "Ошибка при запросе к Blockade API (blocade/map_items/obj_types/)"
        ) from e


"""
Объекты раздела Хроника за конкретную дату.

Параметр:
- date: дата в формате yyyy-mm-dd (пример: 1941-09-08).
"""
def get_blockade_chronicle_by_exact_date(
    date: Optional[str] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if date is not None:
        params["date"] = date

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/blocade/chronicle_items/by_exact_date/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Blockade API error (blocade/chronicle_items/by_exact_date/)")
        raise BlockadeError(
            "Ошибка при запросе к Blockade API (blocade/chronicle_items/by_exact_date/)"
        ) from e


"""
Объекты раздела Хроника за конкретные день и месяц.

Входные параметры day и month обязательны.
"""
def get_blockade_chronicle_by_day_month(
    day: int,
    month: int,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    if day is None:
        raise BlockadeError(
            "Параметр 'day' обязателен для запроса /blocade/chronicle_items/by_day_month"
        )
    if month is None:
        raise BlockadeError(
            "Параметр 'month' обязателен для запроса /blocade/chronicle_items/by_day_month"
        )

    params: Dict[str, Any] = {
        "day": day,
        "month": month,
    }

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/blocade/chronicle_items/by_day_month",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Blockade API error (blocade/chronicle_items/by_day_month)")
        raise BlockadeError(
            "Ошибка при запросе к Blockade API (blocade/chronicle_items/by_day_month)"
        ) from e


"""
Объект раздела Хроника по id.
Входной параметр object_id обязателен.
"""
def get_blockade_chronicle_by_id(
    object_id: int,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if object_id is None:
        raise BlockadeError(
            "Параметр 'object_id' обязателен для запроса /blocade/chronicle_items/by_id/"
        )

    params: Dict[str, Any] = {"object_id": object_id}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/blocade/chronicle_items/by_id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Blockade API error (blocade/chronicle_items/by_id/)")
        raise BlockadeError(
            "Ошибка при запросе к Blockade API (blocade/chronicle_items/by_id/)"
        ) from e


"""
Объекты раздела Наследие по выбранным типам в заданном радиусе.

Параметры аналогичны разделу Карта:
- obj_types: типы объектов через запятую без пробела
  (справочник типов: /blocade/heritage_items/obj_types/),
- location_latitude / location_longitude: координаты центра,
- location_radius: радиус поиска в км (до 160).
"""
def get_blockade_heritage_items_by_radius(
    obj_types: Optional[str] = None,
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    if obj_types is not None:
        params["obj_types"] = obj_types
    if location_latitude is not None:
        params["location_latitude"] = location_latitude
    if location_longitude is not None:
        params["location_longitude"] = location_longitude
    if location_radius is not None:
        params["location_radius"] = location_radius

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/blocade/heritage_items/by_radius/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Blockade API error (blocade/heritage_items/by_radius/)")
        raise BlockadeError(
            "Ошибка при запросе к Blockade API (blocade/heritage_items/by_radius/)"
        ) from e


"""
Объект раздела Наследие по id.
Входной параметр object_id обязателен.
"""
def get_blockade_heritage_item_by_id(
    object_id: int,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if object_id is None:
        raise BlockadeError(
            "Параметр 'object_id' обязателен для запроса /blocade/heritage_items/by_id/"
        )

    params: Dict[str, Any] = {"object_id": object_id}

    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id
    if region is not None:
        headers["region"] = region

    try:
        resp = requests.get(
            f"{main_api}/blocade/heritage_items/by_id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Blockade API error (blocade/heritage_items/by_id/)")
        raise BlockadeError(
            "Ошибка при запросе к Blockade API (blocade/heritage_items/by_id/)"
        ) from e


"""
Типы объектов раздела Наследие.
Используется для фильтрации в /blocade/heritage_items/by_radius/.
"""
def get_blockade_heritage_obj_types(
    app_version: Optional[str] = None,
) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    if app_version is not None:
        headers["app-version"] = app_version

    try:
        resp = requests.get(
            f"{main_api}/blocade/heritage_items/obj_types/",
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("Blockade API error (blocade/heritage_items/obj_types/)")
        raise BlockadeError(
            "Ошибка при запросе к Blockade API (blocade/heritage_items/obj_types/)"
        ) from e

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        photos = get_blockade_photos()
        logger.info("Фотографии (пример ответа): %s", str(photos)[:300])

        medals = get_blockade_medals_count()
        logger.info("Количество медалей (пример ответа): %s", medals)

        persons = get_blockade_persons(name="Иван")
        logger.info("Поиск награжденных по имени (пример): %s", str(persons)[:300])

        places = get_blockade_person_places()
        logger.info("Места работы (пример): %s", str(places)[:300])

        stories = get_blockade_stories()
        logger.info("Мини-истории (пример): %s", str(stories)[:300])

        # --- Карта блокады ---
        map_obj_types = get_blockade_map_obj_types()
        logger.info("Карта: типы объектов (пример): %s", str(map_obj_types)[:300])

        map_items = get_blockade_map_items_by_radius(
            location_latitude=59.93,
            location_longitude=30.33,
            location_radius=5,
        )
        logger.info("Карта: объекты по радиусу (пример): %s", str(map_items)[:300])

        map_item = get_blockade_map_item_by_id(object_id=1)
        logger.info("Карта: объект по id (пример): %s", str(map_item)[:300])

        # --- Хроника ---
        chronicle_exact = get_blockade_chronicle_by_exact_date(date="1941-09-08")
        logger.info("Хроника: по точной дате (пример): %s", str(chronicle_exact)[:300])

        chronicle_dm = get_blockade_chronicle_by_day_month(day=8, month=9)
        logger.info("Хроника: по дню и месяцу (пример): %s", str(chronicle_dm)[:300])

        chronicle_by_id = get_blockade_chronicle_by_id(object_id=1)
        logger.info("Хроника: объект по id (пример): %s", str(chronicle_by_id)[:300])

        # --- Наследие ---
        heritage_obj_types = get_blockade_heritage_obj_types()
        logger.info("Наследие: типы объектов (пример): %s", str(heritage_obj_types)[:300])

        heritage_items = get_blockade_heritage_items_by_radius(
            location_latitude=59.93,
            location_longitude=30.33,
            location_radius=5,
        )
        logger.info("Наследие: объекты по радиусу (пример): %s", str(heritage_items)[:300])

        heritage_item = get_blockade_heritage_item_by_id(object_id=2)
        logger.info("Наследие: объект по id (пример): %s", str(heritage_item)[:300])

    except BlockadeError as e:
        logger.error("Blockade API test failed: %s", e)
