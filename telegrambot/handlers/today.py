from aiogram import Router, types
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from django.utils import timezone

from habit_instances.models import HabitInstance, HabitInstanceStatus
from users.models import TelegramProfile

router = Router()


@router.message(Command("today"))
async def today_handler(message: types.Message):
    chat_id = message.chat.id

    try:
        profile = await sync_to_async(
            lambda: TelegramProfile.objects.select_related("user").get(chat_id=chat_id, is_active=True)
        )()
    except TelegramProfile.DoesNotExist:
        await message.answer("❗ Telegram не привязан. Используйте /profile.")
        return

    today = timezone.localdate()

    user = profile.user

    instances = await sync_to_async(
        lambda: list(
            HabitInstance.objects.filter(
                habit__user=user,
                scheduled_datetime__date=today,
                status__in=[
                    HabitInstanceStatus.PENDING,
                    HabitInstanceStatus.SCHEDULED,
                ],
            )
            .select_related("habit")
            .order_by("scheduled_datetime")
        )
    )()

    if not instances:
        await message.answer("На сегодня нет ожидающих привычек.\nПосмотрите /habits")
        return

    lines = ["📅 *Привычки на сегодня*\n"]

    STATUS_ICONS = {
        "scheduled": "🕒",
        "pending": "⏳",
        "completed": "✔️",
        "completed_late": "✔️⏱",
        "missed": "❌",
        "fix_expired": "⛔",
    }

    for i, inst in enumerate(instances, start=1):
        t = inst.scheduled_datetime.strftime("%H:%M")
        status = inst.status.replace("_", " ")
        icon = STATUS_ICONS.get(inst.status, "")
        lines.append(f"{i}. {inst.habit.action} — {t} {icon} ({status})")

    await message.answer("\n".join(lines), parse_mode="Markdown")
