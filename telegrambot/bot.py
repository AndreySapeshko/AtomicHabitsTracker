import logging

from aiogram import Bot
from django.conf import settings

logger = logging.getLogger("telegrambot")


def get_bot():
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning("⚠️ TELEGRAM_BOT_TOKEN is not set — bot is disabled")
        return None
    raise RuntimeError(f"🔥TELEGRAM_BOT_TOKEN: {settings.TELEGRAM_BOT_TOKEN}")
    return Bot(settings.TELEGRAM_BOT_TOKEN)
