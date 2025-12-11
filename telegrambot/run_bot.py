import asyncio
import logging

from telegrambot.bot import get_bot

from .dispatcher import setup_routers
from .redis_listener import redis_in_listener, redis_listener

logger = logging.getLogger("telegrambot")


async def main():
    bot = get_bot()
    dp = setup_routers()

    # ✅ В CI бот просто не запускается
    if bot is None:
        logger.info("⚠️ Bot is disabled (CI or no token) — exiting")
        return

    logger.info("🚀 Telegram bot started")

    try:
        await asyncio.gather(
            redis_listener(bot),  # исходящие сообщения → Telegram
            redis_in_listener(dp, bot),  # входящие update из webhook
        )
    except asyncio.CancelledError:
        print("👋 Shutdown requested")
    finally:
        await bot.session.close()


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
