from django.core.management.base import BaseCommand

from telegrambot.run_bot import run


class Command(BaseCommand):
    help = "Run Telegram bot worker"

    def handle(self, *args, **options):
        self.stdout.write("🚀 Telegram worker started")
        run()
