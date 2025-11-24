import asyncio

from aiogram import Bot
from django.conf import settings

from telegrambot.dispatcher import dp


async def main():
    bot = Bot(settings.TELEGRAM_BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
