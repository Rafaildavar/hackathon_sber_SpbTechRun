# Инструкция по запуску приложения

## Что было исправлено:

1. ✅ Исправлена ошибка с зарезервированным словом `metadata` в SQLAlchemy - переименовано в `message_metadata`
2. ✅ Обновлен устаревший `on_event` на современный `lifespan` для FastAPI
3. ✅ Созданы таблицы в базе данных (chats, messages)

## Запуск приложения:

### 1. Убедитесь, что PostgreSQL запущен:
```bash
docker-compose up -d
```

### 2. Запустите приложение:
```bash
python app.py
```

Или через uvicorn напрямую:
```bash
uvicorn app:app --host 0.0.0.0 --port 5001 --reload
```

### 3. Откройте в браузере:
- Главная страница: http://localhost:5001/
- Страница чата: http://localhost:5001/chat
- API документация: http://localhost:5001/docs

## Структура базы данных:

- **users** - пользователи
- **chats** - чаты пользователей
- **messages** - сообщения в чатах

Все таблицы создаются автоматически при первом запуске приложения.

## API эндпоинты для чатов:

- `GET /api/chats` - получить список чатов
- `POST /api/chats` - создать новый чат
- `GET /api/chats/{chat_id}` - получить чат по ID
- `PUT /api/chats/{chat_id}` - обновить чат
- `DELETE /api/chats/{chat_id}` - удалить чат
- `GET /api/chats/{chat_id}/messages` - получить сообщения чата
- `POST /api/chats/{chat_id}/messages` - создать сообщение

