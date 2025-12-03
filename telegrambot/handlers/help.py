import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from django.conf import settings

from telegrambot.services.sender import sender

logger = logging.getLogger("telegrambot")

WEB_URL = settings.WEB_APP_URL

router = Router()


@router.message(Command("help"))
async def help_handler(msg: Message):
    logger.info("Start help_handle")
    text = (
        "ℹ️ <b>Справка по командам</b>\n\n"
        "👤 /profile — ваш профиль\n"
        "📘 /habits — все привычки\n"
        "🗓️ /today — задания на сегодня\n"
        "ℹ️ /help — справка\n\n"
        "🔧 Служебные команды:\n"
        "   /bind — как привязать Telegram\n"
        "   /unbind — отвязать Telegram\n"
        f"🌐 Веб-приложение: {WEB_URL}"
    )
    await sender.send(msg.chat.id, text)
