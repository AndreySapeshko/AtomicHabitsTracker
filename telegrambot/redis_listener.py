import json
import logging

import redis.asyncio as aioredis
from aiogram import Bot, types
from django.conf import settings

logger = logging.getLogger("telegrambot")


async def redis_in_listener(dp, bot):
    if not getattr(settings, "USE_REDIS", True):
        logger.info("⚠️ Redis is disabled — redis_in_listener will not start")
        return

    r = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

    logger.info("🚀 Start redis_in_listener (входящие апдейты)")

    while True:
        try:
            _, data = await r.brpop("telegram:in")

            payload = json.loads(data)

            try:
                update = types.Update.model_validate(payload)
            except Exception as e:
                logger.error(f"❌ Ошибка при парсинге Update: {e}")
                continue

            await dp.feed_update(bot, update)

        except Exception as e:
            logger.error(f"❌ Ошибка в redis_in_listener: {e}")


def json_to_markup(keyboard: dict):
    markup = None
    if keyboard:
        from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

        buttons = []
        for row in keyboard["inline_keyboard"]:
            btn_row = [InlineKeyboardButton(text=b["text"], callback_data=b["callback_data"]) for b in row]
            buttons.append(btn_row)

        markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


async def redis_listener(bot: Bot):
    if not getattr(settings, "USE_REDIS", True):
        logger.info("⚠️ Redis is disabled — redis_listener will not start")
        return

    r = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    logger.info("🚀 Start redis_listener")

    while True:
        raw = await r.brpop("telegram:out")
        _, data = raw

        try:
            payload = json.loads(data)
        except Exception:
            logger.error("Invalid JSON in telegram:out")
            continue

        await bot.send_message(
            payload["chat_id"],
            payload["text"],
            reply_markup=json_to_markup(payload.get("keyboard")),
        )
