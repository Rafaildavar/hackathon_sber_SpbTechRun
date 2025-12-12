import logging
import aiomax
import bot_config
import agent
from aiomax.buttons import CallbackButton, KeyboardBuilder

bot = aiomax.Bot(bot_config.TOKEN, default_format="markdown")

# Состояния пользователей для регистрации
user_states = {}


def get_main_menu_keyboard():
    """Создать главное меню с кнопками"""
    builder = KeyboardBuilder()
    builder.row(
        CallbackButton("Новый чат", payload="new_chat"),
        CallbackButton("Помощь", payload="help")
    )
    return builder.to_list()


def get_clear_keyboard():
    """Кнопка очистки контекста"""
    builder = KeyboardBuilder()
    builder.row(
        CallbackButton("🔄 Очистить контекст", payload="clear_context")
    )
    return builder.to_list()


# Отправка приветственного сообщения при нажатии кнопки "Начать" в мессенджере
@bot.on_bot_start()
async def info(pd: aiomax.BotStartPayload):
    welcome_message = """Привет! Я городской помощник. Задавай мне вопросы о Санкт-Петербурге.

**Команды:**
/help - показать справку
/new_chat - начать новый диалог
/clear - очистить контекст"""

    await pd.send(welcome_message, keyboard=get_main_menu_keyboard())


# Обработка callback-кнопок
@bot.on_button_callback()
async def handle_callback(callback: aiomax.Callback):
    user_id = str(callback.from_user.id) if callback.from_user else "unknown"

    if callback.payload == "new_chat":
        # Создаем новый чат
        result = agent.clear_memory(user_id)
        if result:
            await callback.answer()
            await callback.message.send(
                "🆕 Начат новый диалог. История очищена.\n\nЗадайте ваш вопрос:",
                keyboard=get_clear_keyboard()
            )
        else:
            await callback.answer("Ошибка при создании нового чата")

    elif callback.payload == "clear_context":
        # Очищаем контекст
        result = agent.clear_memory(user_id)
        if result:
            await callback.answer()
            await callback.message.send(
                "🔄 Контекст очищен. Начинаем заново!\n\nЗадайте ваш вопрос:",
                keyboard=get_clear_keyboard()
            )
        else:
            await callback.answer("Ошибка при очистке контекста")

    elif callback.payload == "help":
        await callback.answer()
        help_text = """**Справка по использованию бота**

**Основные команды:**
/help - показать эту справку
/new_chat - начать новый диалог
/clear - очистить контекст текущего чата

**Как задавать вопросы:**
• Просто напишите свой вопрос
• Я помогу найти информацию о Санкт-Петербурге
• Могу работать с документами

**Примеры вопросов:**
• "Где находится Эрмитаж?"
• "Как получить справку в МФЦ?"
• "Расскажи о Василеостровском районе"

Задавайте любые вопросы о городе!"""
        await callback.message.send(help_text, keyboard=get_main_menu_keyboard())

# Функция будет выполняться при отправке любого сообщения
@bot.on_message()
async def handle_message(message: aiomax.Message):
    # Попытки получить идентификатор пользователя из доступных полей
    user_id = getattr(message, "sender_id", None) or getattr(message, "user_id", None)
    if user_id is None:
        sender = getattr(message, "sender", None) or getattr(message, "from_user", None)
        user_id = getattr(sender, "id", None) if sender is not None else "unknown"

    user_id = str(user_id)
    text = (message.content or "").strip()

    # Обработка команд
    if text.startswith("/"):
        await handle_command(message, user_id, text)
        return

    # Проверяем есть ли вложения в message.body.attachments
    if hasattr(message, 'body') and message.body and hasattr(message.body, 'attachments') and message.body.attachments:
        attachments = message.body.attachments
        if len(attachments) > 0:
            # Берем первое вложение
            attachment = attachments[0]

            # Получаем URL и имя файла
            url = getattr(attachment, 'url', None)
            filename = getattr(attachment, 'filename', None)

            # Если нет filename (например ShareAttachment), пытаемся извлечь из URL
            if not filename and url:
                filename = url.split('/')[-1].split('?')[0]

            print(f"📎 Processing attachment: {filename} from {url}")

            if url and filename:
                # Скачиваем файл
                import aiohttp

                try:
                    # Отправляем уведомление о начале обработки
                    await message.send(f"📄 Обрабатываю файл {filename}...")

                    async with aiohttp.ClientSession() as sess:
                        async with sess.get(url) as resp:
                            # Скачиваем как байты
                            data = await resp.read()

                            # Проверяем, является ли это PDF
                            is_pdf = filename.lower().endswith('.pdf') or \
                                     'application/pdf' in resp.headers.get('Content-Type', '')

                            if is_pdf:
                                # Парсим PDF
                                print(f"📄 Parsing PDF: {filename}")
                                from agent import parse_pdf_from_bytes
                                content_text = parse_pdf_from_bytes(data)
                            else:
                                # Попробуем прочитать как текст utf-8
                                try:
                                    content_text = data.decode("utf-8")
                                except Exception:
                                    content_text = data.decode(errors="replace")

                            # Отправляем в агента
                            response = await agent.handle_user_message(
                                str(user_id),
                                text=None,
                                document_text=content_text,
                                document_name=filename
                            )

                            # Отправляем подтверждение
                            await message.send(f"✅ Файл обработан и добавлен в контекст\n\n{response}", keyboard=get_clear_keyboard())
                            return

                except Exception as e:
                    print(f"❌ Error downloading attachment: {e}")
                    await message.send(f"❌ Не удалось обработать файл: {e}")
                    return

    # Обычное текстовое сообщение — передаем агенту
    if text:
        response = await agent.handle_user_message(str(user_id), text=text)
        await message.send(response, keyboard=get_clear_keyboard())


async def handle_command(message: aiomax.Message, user_id: str, text: str):
    """Обработка команд бота"""
    command = text.split()[0].lower()

    if command == "/start":
        welcome_message = """Привет! Я городской помощник. Задавай мне вопросы о Санкт-Петербурге.

**Команды:**
/help - показать справку
/new_chat - начать новый диалог
/clear - очистить контекст"""
        await message.send(welcome_message, keyboard=get_main_menu_keyboard())

    elif command == "/help":
        help_text = """**Справка по использованию бота**

**Основные команды:**
/help - показать эту справку
/new_chat - начать новый диалог
/clear - очистить контекст текущего чата

**Как задавать вопросы:**
• Просто напишите свой вопрос
• Я помогу найти информацию о Санкт-Петербурге
• Могу работать с документами (отправьте PDF или текстовый файл)

**Примеры вопросов:**
• "Где находится Эрмитаж?"
• "Как получить справку в МФЦ?"
• "Расскажи о Василеостровском районе"

Задавайте любые вопросы о городе!"""
        await message.send(help_text, keyboard=get_main_menu_keyboard())

    elif command == "/new_chat" or command == "/clear":
        result = agent.clear_memory(user_id)
        if result:
            await message.send(
                "🆕 Начат новый диалог. История очищена.\n\nЗадайте ваш вопрос:",
                keyboard=get_clear_keyboard()
            )
        else:
            await message.send("Ошибка при создании нового чата. Попробуйте позже.")

    else:
        await message.send(
            f"Неизвестная команда: {command}\n\nИспользуйте /help для списка команд.",
            keyboard=get_main_menu_keyboard()
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("🤖 Городской помощник - бот для MAX запущен!")
    print("📱 Готов к работе...")
    bot.run()