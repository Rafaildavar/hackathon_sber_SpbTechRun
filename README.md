# Городской советник

Интеллектуальный AI-помощник для жителей Санкт-Петербурга. Отвечает на повседневные вопросы о городе и городских службах, используя базу знаний, городские API и веб-поиск.

## Возможности

- Поиск ближайших МФЦ, поликлиник, школ, детских садов по адресу или району
- Информация о государственных услугах, льготах и пособиях
- Ответы на вопросы по документам, загруженным пользователем
- Веб-поиск актуальных городских новостей и событий
- Веб-интерфейс с историей чатов и профилем пользователя
- Telegram-бот с историей диалога в сессии

## Архитектура

```
┌─────────────────────────────────────────────────────┐
│                    Пользователь                      │
│           Web-интерфейс / Telegram-бот               │
└────────────────────┬────────────────────────────────┘
                     │
          ┌──────────▼──────────┐
          │   Web App (5001)    │  FastAPI + UI + Auth
          │      app.py         │  PostgreSQL (история чатов)
          └──────────┬──────────┘
                     │
     ┌───────────────▼───────────────────┐
     │     LangGraph Multi-Agent (AI)    │
     │                                   │
     │  toxicity -> router -> clarify    │
     │    -> retrieve -> context         │
     │    -> conversational LLM          │
     └──────┬────────────┬───────────────┘
            │            │
   ┌────────▼───┐  ┌─────▼──────────┐
   │  Qdrant    │  │  RAG-сервер    │  BM25 + Vector Search
   │ (6333)     │  │  (6500)        │  + Reranker
   └────────────┘  └──────┬─────────┘
                          │
               ┌──────────▼──────────┐
               │   LLM: Qwen2.5-32B  │  via CAILA.io
               │   Tavily Web Search │
               └─────────────────────┘
```

### Агентный pipeline

| Агент | Функция |
|-------|---------|
| ToxicityAgent | Фильтрация токсичных сообщений |
| ParserAgent | Обработка загруженных документов |
| RouterAgent | Определение источников данных (RAG / API / Web) |
| ClarificationAgent | Запрос уточнений при неоднозначном запросе |
| RetrievalAgent | Параллельный поиск в RAG, городских API, интернете |
| ContextAgent | Подготовка контекста и истории диалога |
| ConversationalAgent | Генерация финального ответа через LLM |

## Стек технологий

| Компонент | Технология |
|-----------|-----------|
| Web-фреймворк | FastAPI |
| Агентный граф | LangGraph |
| LLM | Qwen2.5-32B (CAILA.io, OpenAI-совместимый API) |
| Эмбеддинги | intfloat/multilingual-e5-base |
| Reranker | cross-encoder/mmarco-mMiniLMv2-L12-H384-v1 |
| Векторная БД | Qdrant |
| Keyword-поиск | BM25 |
| Веб-поиск | Tavily API |
| База данных | PostgreSQL 15 |
| ORM | SQLAlchemy 2 |
| Аутентификация | passlib (bcrypt) |
| Telegram-бот | aiogram 3.x |
| Контейнеризация | Docker / Docker Compose |

## Быстрый старт

### Требования

- Docker и Docker Compose
- Python 3.12+ (для локального запуска без Docker)

### Запуск через Docker

1. Скопируйте файл с переменными окружения:
   ```bash
   cp .env.example .env
   ```

2. Заполните `.env` своими ключами (см. раздел «Конфигурация»).

3. Запустите все сервисы:
   ```bash
   docker-compose up --build
   ```

4. Откройте веб-интерфейс: http://localhost:5001

### Локальный запуск (без Docker)

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   pip install uv
   uv pip install --system -r server/pyproject.toml
   ```

2. Запустите PostgreSQL и Qdrant:
   ```bash
   docker-compose up postgres qdrant -d
   ```

3. Запустите RAG-сервер:
   ```bash
   cd server/src && python main.py
   ```

4. Запустите основное приложение:
   ```bash
   python app.py
   ```

5. (Опционально) Запустите Telegram-бота:
   ```bash
   cd bot && pip install -r requirements.txt && python telegram_bot.py
   ```

## Конфигурация

Все настройки задаются через `.env` (скопируйте из `.env.example`):

| Переменная | Описание |
|-----------|----------|
| `LLM_TOKEN` | API-ключ CAILA.io |
| `LLM_URL` | Endpoint CAILA.io |
| `LLM_MODEL` | Имя модели |
| `TAVILY_API_KEY` | API-ключ Tavily для веб-поиска |
| `POSTGRES_USER` | Пользователь PostgreSQL |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL |
| `POSTGRES_DB` | Имя базы данных |
| `SECRET_KEY` | Секретный ключ для сессий |
| `TELEGRAM_BOT_TOKEN` | Токен Telegram-бота (получить у @BotFather) |
| `INTERNAL_BOT_SECRET` | Секрет для авторизации бота в web-приложении |

Конфигурация AI-сервера хранится в `server/src/config.yml` и может быть переопределена переменными окружения.

## Структура проекта

```
├── app.py                          # Основное веб-приложение (порт 5001)
├── database.py                     # SQLAlchemy модели (User, Chat, Message)
├── Dockerfile                      # Docker-образ веб-приложения
├── docker-compose.yml              # Оркестрация всех сервисов
├── requirements.txt                # Зависимости веб-приложения
├── .env.example                    # Шаблон переменных окружения
│
├── server/                         # AI-бэкенд (порт 6500)
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── src/
│       ├── main.py
│       ├── config.yml              # Конфигурация AI-сервера
│       ├── config/Config.py        # Загрузчик конфигурации
│       ├── core/
│       │   ├── langgraph_multi_agent/
│       │   │   ├── main.py         # UrbanAdvisorSystem (граф агентов)
│       │   │   ├── state.py        # UrbanAdvisorState
│       │   │   ├── prompts.yml     # Промпты для LLM
│       │   │   └── agents/         # 7 агентов
│       │   └── services/           # LLM, Qdrant, BM25, Reranker
│       └── endpoints/              # FastAPI endpoints
│
├── bot/                            # Telegram-бот
│   ├── telegram_bot.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── resources/                      # Фронтенд
│   ├── templates/                  # HTML (Jinja2)
│   └── static/                     # CSS, JS, изображения
│
└── yazzh_api/                      # Модули городских данных (25+)
```

## Примеры использования

```
— Где ближайший МФЦ от метро Площадь Восстания?
— Какие документы нужны для получения субсидии на ЖКХ?
— Список детских садов в Московском районе
— Какие льготы положены многодетным семьям в Петербурге?
— Как записаться к врачу через госуслуги?
— Что посмотреть туристу в Санкт-Петербурге?
```

## Сервисы

| Сервис | URL / Порт |
|--------|-----------|
| Веб-интерфейс | http://localhost:5001 |
| AI API (Swagger) | http://localhost:6500/docs |
| Qdrant Dashboard | http://localhost:6333/dashboard |
| PostgreSQL | localhost:5435 |
