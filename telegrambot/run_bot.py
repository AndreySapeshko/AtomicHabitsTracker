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


async def redis_listener(bot: Bot):
    """
    Separate coroutine that listens to Redis for outgoing commands.
    """
    r = aioredis.from_url("redis://localhost/0")
    logger.info("🚀 Start redis_listener")
    while True:
        # Blocking wait for a new command
        raw = await r.brpop("telegram:out")
        logger.info("Получена задача telegram:out")

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
    bot = Bot(settings.TELEGRAM_BOT_TOKEN)
    logger.info("🚀 Telegram bot started")

    # run polling + queue listener concurrently
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
