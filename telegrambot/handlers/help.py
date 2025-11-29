from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def help_handler(message: types.Message):
    text = (
        "ℹ️ *Команды бота*\n\n"
        "/profile — ваш профиль и привычки на сегодня\n"
        "/habits — все привычки\n"
        "/today — задачи на сегодня\n"
        "/help — эта справка\n"
    )
    await message.answer(text, parse_mode="Markdown")
