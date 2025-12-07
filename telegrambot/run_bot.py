import asyncio
import json
import logging

import redis.asyncio as aioredis
from aiogram import Bot
from django.conf import settings

from telegrambot.dispatcher import dp, setup_routers

logger = logging.getLogger("telegrambot")


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


def get_bot():
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning("⚠️ TELEGRAM_BOT_TOKEN is not set — bot is disabled")
        return None

    return Bot(settings.TELEGRAM_BOT_TOKEN)


async def redis_listener(bot: Bot):
    if not getattr(settings, "USE_REDIS", True):
        logger.info("⚠️ Redis is disabled — redis_listener will not start")
        return

    r = aioredis.from_url("redis://localhost/0")
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


async def main():
    setup_routers()

    bot = get_bot()

    # ✅ В CI бот просто не запускается
    if bot is None:
        logger.info("⚠️ Bot is disabled (CI or no token) — exiting")
        return

    logger.info("🚀 Telegram bot started")

    try:
        await asyncio.gather(
            dp.start_polling(bot),
            redis_listener(bot),
        )
    except asyncio.CancelledError:
        print("👋 Shutdown requested")
    finally:
        await bot.session.close()


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
