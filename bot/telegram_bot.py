"""
Telegram-бот «Городской советник».
Принимает вопросы пользователей и передаёт их в основной pipeline агента.
"""

import asyncio
import logging
import os

import httpx
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
APP_URL = os.environ.get("APP_URL", "http://web:5001")
INTERNAL_BOT_SECRET = os.environ["INTERNAL_BOT_SECRET"]

MAX_MESSAGE_LENGTH = 4096

# История диалогов: user_id -> list[dict]
user_histories: dict[int, list] = {}

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


def split_message(text: str) -> list[str]:
    """Разбивает длинное сообщение на части не длиннее MAX_MESSAGE_LENGTH."""
    if len(text) <= MAX_MESSAGE_LENGTH:
        return [text]

    parts = []
    while text:
        if len(text) <= MAX_MESSAGE_LENGTH:
            parts.append(text)
            break
        split_pos = text.rfind("\n", 0, MAX_MESSAGE_LENGTH)
        if split_pos == -1:
            split_pos = MAX_MESSAGE_LENGTH
        parts.append(text[:split_pos])
        text = text[split_pos:].lstrip("\n")
    return parts


async def call_agent(message: str, history: list) -> tuple[str, list]:
    """Отправляет сообщение в pipeline агента и возвращает (ответ, обновлённая история)."""
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{APP_URL}/api/bot/chat",
            json={"message": message, "history": history},
            headers={"X-Bot-Secret": INTERNAL_BOT_SECRET},
        )
        response.raise_for_status()
        data = response.json()
        return data["response"], data.get("history", [])


@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_histories[message.from_user.id] = []
    await message.answer(
        "Привет! Я «Городской советник» — AI-помощник для жителей Санкт-Петербурга.\n\n"
        "Помогу найти:\n"
        "• Ближайший МФЦ, поликлинику, школу или детский сад\n"
        "• Информацию о городских услугах, льготах и пособиях\n"
        "• Актуальные события и места города\n\n"
        "Просто задайте вопрос!\n\n"
        "/help — что я умею\n"
        "/clear — сбросить историю диалога"
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "«Городской советник» — интеллектуальный агент для жителей Санкт-Петербурга.\n\n"
        "Использую три источника данных:\n"
        "📚 База знаний — нормативные документы, FAQ госуслуг (gu.spb.ru)\n"
        "🏙 Городские API — МФЦ, поликлиники, школы, детсады, афиша, достопримечательности\n"
        "🔍 Поиск в интернете — актуальные новости и события\n\n"
        "Примеры вопросов:\n"
        "— Где ближайший МФЦ от Невского проспекта?\n"
        "— Как оформить субсидию на ЖКХ?\n"
        "— Какие льготы положены многодетным семьям?\n"
        "— Что посмотреть в Петербурге на этой неделе?\n\n"
        "/clear — сбросить историю диалога"
    )


@dp.message(Command("clear"))
async def cmd_clear(message: Message):
    user_histories[message.from_user.id] = []
    await message.answer("История диалога сброшена. Начинаем сначала!")


@dp.message()
async def handle_message(message: Message):
    text = (message.text or "").strip()
    if not text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение.")
        return

    user_id = message.from_user.id
    history = user_histories.get(user_id, [])

    await bot.send_chat_action(message.chat.id, "typing")

    try:
        response_text, updated_history = await call_agent(text, history)
        user_histories[user_id] = updated_history
        for part in split_message(response_text):
            await message.answer(part)

    except httpx.TimeoutException:
        log.warning(f"Timeout for user {user_id}")
        await message.answer(
            "Запрос обрабатывается слишком долго. Попробуйте переформулировать вопрос."
        )
    except httpx.HTTPStatusError as e:
        log.error(f"HTTP error for user {user_id}: {e.response.status_code} {e.response.text}")
        await message.answer("Произошла ошибка при обращении к агенту. Попробуйте позже.")
    except Exception as e:
        log.error(f"Unexpected error for user {user_id}: {e}")
        await message.answer("Произошла непредвиденная ошибка. Попробуйте позже.")


async def main():
    log.info("Запуск Telegram-бота «Городской советник»")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
