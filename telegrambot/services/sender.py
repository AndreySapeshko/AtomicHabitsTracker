from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from telegrambot.bot import bot


class TelegramSender:

    def __init__(self, bot: Bot):
        self.bot = bot

    async def send(self, chat_id: int, text: str, kb=None):
        await self.bot.send_message(chat_id, text, reply_markup=kb, parse_mode="HTML")

    def habit_link_keyboard(self, habit_id: int):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📊 Статистика", callback_data=f"stats:{habit_id}")],
                [InlineKeyboardButton(text="📄 Детали", callback_data=f"habit:{habit_id}")],
            ]
        )

    def instance_status_keyboard(self, instance_id: int):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✔️ Выполнено", callback_data=f"done:{instance_id}")],
                [InlineKeyboardButton(text="❌ Не успел", callback_data=f"missed:{instance_id}")],
            ]
        )


sender = TelegramSender(bot)
