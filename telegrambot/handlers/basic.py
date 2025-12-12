import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from django.conf import settings

from telegrambot.services.sender import sender

logger = logging.getLogger("telegrambot")

router = Router()

WEB_URL = settings.WEB_APP_URL


@router.message(Command("start"))
async def start_cmd(msg: Message):
    logger.info(f"Start start_cmd with chat.id: {msg.chat.id}")
    text = (
        "👋 Привет! Я — бот Habit Tracker.\n\n"
        "Чтобы я мог отправлять напоминания:\n"
        "1) Открой веб-приложение\n"
        f"{WEB_URL}\n"
        "2) В профиле нажми «Привязать Telegram»\n"
        "3) Введи код здесь\n\n"
        "❓ Команды: /help"
    )
    await sender.send(msg.chat.id, text)


# @router.message()
# async def debug_all(message: types.Message):
#     print("🔥 FULL MESSAGE:", message.model_dump())
