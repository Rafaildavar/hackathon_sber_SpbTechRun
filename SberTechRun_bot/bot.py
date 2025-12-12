import logging
import aiomax
import config
import agent

bot = aiomax.Bot(config.TOKEN, default_format="markdown")

# Отправка информации о боте при нажатии кнопки "Начать" в мессенджере
@bot.on_bot_start()
async def info(pd: aiomax.BotStartPayload):
    await pd.send("Я повторяю за тобой")

# Функция будет выполняться при отправке любого сообщения
@bot.on_message()
async def handle_message(message: aiomax.Message):
    # Попытки получить идентификатор пользователя из доступных полей
    user_id = getattr(message, "sender_id", None) or getattr(message, "user_id", None)
    if user_id is None:
        sender = getattr(message, "sender", None) or getattr(message, "from_user", None)
        user_id = getattr(sender, "id", None) if sender is not None else "unknown"

    text = (message.content or "").strip()

    # Поддерживаем команду загрузки документа через текст:
    # /doc path/to/file.txt  — прочитаем локальный файл и передадим агенту
    if text.startswith("/doc "):
        path = text.split(" ", 1)[1].strip()
        response = await agent.handle_user_message(str(user_id), text=None, document_path=path)
        await message.send(response)
        return

    # Если в сообщении есть вложения/файлы — попробуем получить их содержимое и
    # передать в агент как текст документа. Поддерживаем несколько возможных
    # имён атрибутов (files, attachments, document).
    files = getattr(message, "files", None) or getattr(message, "attachments", None) or getattr(message, "document", None) or getattr(message, "documents", None)
    if files:
        # Обычно files - это итерируемая коллекция; обработаем первый файл.
        first = None
        try:
            # Если это словарь/Mapping
            if isinstance(files, dict):
                # берем первый ключ
                first = next(iter(files.values()))
            else:
                first = files[0] if hasattr(files, "__getitem__") else None
        except Exception:
            first = None

        content_text = None
        name = None
        if first is not None:
            # Попробуем извлечь URL или байты
            name = getattr(first, "name", None) or getattr(first, "filename", None) or getattr(first, "file_name", None)
            url = getattr(first, "url", None) or getattr(first, "file_url", None) or getattr(first, "download_url", None)
            data = getattr(first, "content", None) or getattr(first, "data", None)

            if data:
                # data может быть bytes или str
                if isinstance(data, bytes):
                    try:
                        content_text = data.decode("utf-8")
                    except Exception:
                        content_text = data.decode(errors="replace")
                else:
                    content_text = str(data)

            elif url and isinstance(url, str) and url.startswith("http"):
                # Скачиваем содержимое файла
                import aiohttp

                try:
                    async with aiohttp.ClientSession() as sess:
                        async with sess.get(url) as resp:
                            # Попробуем прочитать как текст utf-8
                            try:
                                content_text = await resp.text()
                            except Exception:
                                raw = await resp.read()
                                try:
                                    content_text = raw.decode("utf-8")
                                except Exception:
                                    content_text = raw.decode(errors="replace")
                except Exception as e:
                    await message.send(f"Не удалось скачать вложение: {e}")
                    return

        if content_text is not None:
            response = await agent.handle_user_message(str(user_id), text=None, document_text=content_text, document_name=name)
            await message.send(response)
            return

    # Обычное текстовое сообщение — передаем агенту
    response = await agent.handle_user_message(str(user_id), text=text)
    await message.send(response)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot.run()