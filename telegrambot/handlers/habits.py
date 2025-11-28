from aiogram import Router, types
from aiogram.filters import Command
from asgiref.sync import sync_to_async

from habits.models import Habit
from users.models import TelegramProfile

router = Router()


@router.message(Command("habits"))
async def habits_handler(message: types.Message):
    chat_id = message.chat.id

    # --- Проверяем привязку ---
    try:
        profile = await sync_to_async(
            lambda: TelegramProfile.objects.select_related("user").get(chat_id=chat_id, is_active=True)
        )()
    except TelegramProfile.DoesNotExist:
        await message.answer("❗ Telegram не привязан.\nИспользуйте /profile чтобы проверить статус.")
        return

    user = profile.user

    habits = await sync_to_async(lambda: list(Habit.objects.filter(user=user).order_by("time_of_day")))()

    if not habits:
        await message.answer("У вас пока нет привычек.\nДобавьте их в веб-версии.")
        return

    lines = ["📘 *Ваши привычки*\n"]

    for i, h in enumerate(habits, start=1):
        t = h.time_of_day.strftime("%H:%M")
        lines.append(f"{i}. {h.action} — {t}")

    lines.append("\nПосмотреть задания на сегодня: /today")

    await message.answer("\n".join(lines), parse_mode="Markdown")
