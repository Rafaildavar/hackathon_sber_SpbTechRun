#Раздел мой питомец из "https://yazzh.gate.petersburg.ru"
from typing import Optional, List, Dict, Any
import logging
import requests

logger = logging.getLogger(__name__)

geo_api = "https://yazzh-geo.gate.petersburg.ru/api/v2"
main_api = "https://yazzh.gate.petersburg.ru"

class MyPetsAPIError(Exception):
    pass

# Получение списка всех ветклиник, Площадок, парков и приютов
# входные параметры: можно оставить без фильтров
def get_mypets_all_category(
    location_latitude: Optional[float] = None,
    location_longitude: Optional[float] = None,
    location_radius: Optional[int] = None,
    types: Optional[List[str]] = None,
    region: str = "78") -> Dict[str, Any]:

    params: Dict[str, Any] = {
        "location_latitude": location_latitude,
        "location_longitude": location_longitude,
        "location_radius": location_radius,
        "type": types #Ветклиника, Площадка, Парк, Приют
    }
    headers = {"region": region}

    # убираем параметры с None
    params = {k: v for k, v in params.items() if v is not None}
    try:
        resp = requests.get(
            f"{main_api}/mypets/all-category/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MyPets API error")
        raise MyPetsAPIError("Ошибка при запросе к MyPets API") from e

# /mypets/all-category/id/ - надо добавлять?

#Поиск по введеным символам (не менее трех, без учета регистра) по базе пород (breed)
# входные параметры: можно оставить без фильтров
def get_mypets_animal_breeds(
    specie: Optional[str] = None, #Собака, Кошка, Грызун, Кролик, Птица, Рептилия
    breed: Optional[str] = None,
    region: str = "78") -> Dict[str, Any]:

    if breed is not None and len(breed) < 3:
        raise MyPetsAPIError("Параметр 'breed' должен быть не короче 3 символов")

    params: Dict[str, Any] = {
        "specie": specie,
        "breed": breed,
    }
    # убираем None из параметров
    params = {k: v for k, v in params.items() if v is not None}

    headers = {"region": region}

    try:
        resp = requests.get(
            f"{main_api}/mypets/animal-breeds/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MyPets API error (animal-breeds)")
        raise MyPetsAPIError("Ошибка при запросе к MyPets API (animal-breeds)") from e

#Возвращает значения полей "вид животного" и "название праздника"
# Без входных параметров
def get_mypets_holidays() -> Dict[str, Any]:
    try:
        resp = requests.get(
            f"{main_api}/mypets/holidays/",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MyPets API error (holidays)")
        raise MyPetsAPIError("Ошибка при запросе к MyPets API (holidays)") from e


"""
 Вывод статей по выбранным видам животных.
 :param specie: Вид животного (Общее, Собака, Кошка, Грызун, Кролик, Птица, Рептилия, story).
                Можно передать несколько через запятую, слитно. Если None — все, кроме story.
 :param page: Номер страницы (минимум 1)
 :param size: Количество статей (1 — случайная, 0 — все, максимум 1000)
 :param app_version: Значение для заголовка 'app-version'
 :param region: Код региона (заголовок 'region')
 :return: JSON-ответ от API
 # входные параметры: можно оставить без фильтров
 """
def get_mypets_posts(
    specie: Optional[str] = None,
    page: Optional[int] = 1,
    size: Optional[int] = 10,
    region: str = "78") -> Dict[str, Any]:

    params: Dict[str, Any] = {
        "specie": specie,
        "page": page,
        "size": size,
    }
    params = {k: v for k, v in params.items() if v is not None}

    headers: Dict[str, str] = {"region": region}

    try:
        resp = requests.get(
            f"{main_api}/mypets/posts/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MyPets API error (posts)")
        raise MyPetsAPIError("Ошибка при запросе к MyPets API (posts)") from e

"""
    Вывод статьи по id.
    :param id: ID поста (обязателен для запроса)!
    :param app_version: Значение для заголовка 'app-version'
    :param user_id: Значение для заголовка 'user-id'
    :param region: Значение для заголовка 'region' (по умолчанию 78)
    :return: JSON-ответ от API
"""
def get_mypets_posts_id(
    id: Optional[int] = None,
    app_version: Optional[str] = None,
    user_id: Optional[str] = None,
    region: Optional[str] = "78") -> Dict[str, Any]:

    if id is None:
        raise MyPetsAPIError("Параметр 'id' обязателен для запроса /mypets/posts/id/")

    params = {"id": id}
    headers: Dict[str, str] = {}
    if region is not None:
        headers["region"] = region
    if app_version is not None:
        headers["app-version"] = app_version
    if user_id is not None:
        headers["user-id"] = user_id

    try:
        resp = requests.get(
            f"{main_api}/mypets/posts/id/",
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MyPets API error (posts/id)")
        raise MyPetsAPIError("Ошибка при запросе к MyPets API (posts/id)") from e

"""
    Вывод советов по выбранным видам животных.
    :specie Вид животного: Собака, Кошка, Грызун, Кролик, Птица, Рептилия !через запятую слитно!
    # входные параметры: можно оставить без фильтров
"""
def get_mypets_recommendations(
    specie: Optional[str] = None,
    page: Optional[int] = 1,
    size: Optional[int] = 10) -> Dict[str, Any]:

    params: Dict[str, Any] = {
        "specie": specie,  # Собака, Кошка, Грызун, Кролик, Птица, Рептилия
        "page": page,
        "size": size,   # 1 — случайный совет, 0 — все
    }
    params = {k: v for k, v in params.items() if v is not None}

    try:
        resp = requests.get(
            f"{main_api}/mypets/recommendations/",
            params=params,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception("MyPets API error (recommendations)")
        raise MyPetsAPIError("Ошибка при запросе к MyPets API (recommendations)") from e


if __name__ == "__main__":
    #print(get_mypets_all_category(types=["Ветклиника", "Площадка"]))
    #print(get_mypets_animal_breeds())
    #print(get_mypets_holidays())
    #print(get_mypets_posts())
    #print(get_mypets_posts_id(id=30))

    print(get_mypets_recommendations())
    #print(get_mypets_recommendations(specie="Птица"))