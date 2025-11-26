import logging

from aiogram import Router, types
from aiogram.filters import Command

logger = logging.getLogger("celery")

router = Router()


# @router.message()
# async def debug_all(message: types.Message):
#     print("🔥 FULL MESSAGE:", message.model_dump())


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    print("🔥 REAL CHAT ID:", message.chat.id)
    await message.answer("Привет! Я бот для отслеживания привычек.\n" "Перейди в приложение и привяжи свой Telegram.")
