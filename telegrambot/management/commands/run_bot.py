import asyncio

from aiogram import Bot
from django.conf import settings
from django.core.management.base import BaseCommand

from telegrambot.dispatcher import dp


class Command(BaseCommand):
    help = "Run Telegram bot in long-polling mode"

    def handle(self, *args, **options):
        token = settings.TELEGRAM_BOT_TOKEN
        if not token:
            self.stderr.write("❌ TELEGRAM_BOT_TOKEN is not set in settings.")
            return

        bot = Bot(token)
        self.stdout.write("🤖 Telegram bot started (long polling)...")

        asyncio.run(dp.start_polling(bot))
