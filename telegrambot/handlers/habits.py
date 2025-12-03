import logging
import re

from aiogram import Router, types
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from django.conf import settings

from habits.models import Habit
from habits.services.stats import get_habit_stats
from telegrambot.services.formatter import bold
from telegrambot.services.sender import sender
from users.models import TelegramProfile

logger = logging.getLogger("telegrambot")

WEB_URL = settings.WEB_APP_URL

router = Router()


@router.message(Command("habits"))
async def habits_handler(message: types.Message):
    logger.info("Start habits_handler")
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
        await message.answer(f"У вас пока нет привычек.\nДобавьте их в веб-версии.\n🌐 Открыть приложение: {WEB_URL}")
        return

    text = bold("📘 Ваши привычки\n")

    for i, h in enumerate(habits, start=1):
        t = h.time_of_day.strftime("%H:%M")
        text += f"{i}. {h.action} — {t}. \n   --> /habit_{h.id}  --> /stats_{h.id}\n"

    await sender.send(message.chat.id, text)

    @router.message(Command(re.compile(r"habit_\d+")))
    async def habit_details_cmd(msg: types.Message):
        logger.info(f"Start habit_details_cmd with: {msg.text}")
        chat_id = msg.chat.id
        try:
            habit_id = int(msg.text.split("_")[1])
        except Exception:
            await sender.send(chat_id, "Неверный формат команды.")
            return

        habit = await sync_to_async(lambda: Habit.objects.filter(id=habit_id).first())()
        if not habit:
            await sender.send(chat_id, "Привычка не найдена.")
            return

        from telegrambot.services.formatter import habit_card

        text = habit_card(habit)

        await sender.send(chat_id, text)


@router.message(Command(re.compile(r"stats_\d+")))
async def habit_stats_cmd(msg: types.Message):
    habit_id = int(msg.text.split("_")[1])
    stats = await sync_to_async(get_habit_stats)(habit_id)

    text = (
        f"📊 <b>Статистика</b>\n\n"
        f"🔥 Текущий стрик: {stats['current_streak']}\n"
        f"🏆 Макс стрик: {stats['max_streak']}\n"
        f"✔ Выполнено: {stats['total_completed']}\n"
        f"❌ Пропущено: {stats['total_missed']}\n"
        f"⏳ Ожидание: {stats['total_pending']}\n"
    )

    await sender.send(msg.chat.id, text)
