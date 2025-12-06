import logging

from aiogram import Router, types
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from django.conf import settings
from django.utils import timezone

from habit_instances.models import HabitInstance
from telegrambot.services.sender import sender
from users.models import TelegramProfile

logger = logging.getLogger("telegrambot")

WEB_URL = settings.WEB_APP_URL

router = Router()


@router.message(Command("profile"))
async def profile_handler(message: types.Message):
    logger.info("Start profile_handler")
    chat_id = message.chat.id
    logger.info(f"chat_id: {chat_id}")
    # 1. Проверяем привязку Telegram
    try:
        profile = await sync_to_async(
            lambda: TelegramProfile.objects.select_related("user").get(chat_id=chat_id, is_active=True)
        )()
    except TelegramProfile.DoesNotExist:
        await sender.send(
            message.chat.id,
            "❗ Ваш Telegram не привязан к аккаунту.\n" "Перейдите в личный кабинет и создайте код привязки."
        )
        return

    user = profile.user

    # 2. Получаем инстансы на сегодня
    today = timezone.localdate()

    instances = await sync_to_async(
        lambda: list(
            HabitInstance.objects.filter(
                habit__user=user, scheduled_datetime__date=today, status__in=["scheduled", "pending"]
            )
            .select_related("habit")
            .order_by("scheduled_datetime")
        )
    )()

    # 3. Строим текст ответа
    text = [
        "👤 <b>Ваш профиль</b>\n",
        f"</b>Email:</b> {user.email}",
        f"<b>Telegram:</b> {profile.username or '—'}\n",
        "<b>Telegram:</b> привязан ✔️",
        "",
        "📌 <b>Привычки на сегодня:</b>",
        f"\n🌐 Открыть приложение: {WEB_URL}",
    ]

    STATUS_ICONS = {
        "scheduled": "🕒",
        "pending": "⏳",
        "completed": "✔️",
        "completed_late": "✔️⏱",
        "missed": "❌",
        "fix_expired": "⛔",
    }

    if not instances:
        text.append("_Нет активных привычек на сегодня_")
    else:
        for idx, inst in enumerate(instances, start=1):
            time = inst.scheduled_datetime.strftime("%H:%M")
            status = inst.status.replace("_", " ")
            icon = STATUS_ICONS.get(inst.status, "")
            habit = inst.habit.action

            text.append(f"{idx}. {habit} — {time} {icon} ({status})")

    text_line = "\n".join(text)
    await sender.send(message.chat.id, text_line)
