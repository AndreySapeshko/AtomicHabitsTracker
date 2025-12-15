import logging
from datetime import datetime, time
from zoneinfo import ZoneInfo

from celery import shared_task
from django.utils import timezone

from habit_instances.models import HabitInstance, HabitInstanceStatus
from habit_instances.services import create_instances_for_all_habits

logger = logging.getLogger("celery")

MSK = ZoneInfo("Europe/Moscow")
UTC = ZoneInfo("UTC")


@shared_task
def generate_daily_instances():
    created = create_instances_for_all_habits()
    return len(created)


@shared_task
def send_reminder_for_instance(instance_id: int):
    from habit_instances.models import HabitInstance
    from telegrambot.tasks import send_telegram_message

    instance = HabitInstance.objects.filter(id=instance_id).select_related("habit", "habit__user").first()
    if not instance:
        return

    habit = instance.habit
    profile = habit.user.telegram_profile

    if not profile or not profile.is_active:
        return

    text = (
        f"Напоминание по привычке:\n\n"
        f"🏷 {habit.action}\n"
        f"📍 {habit.place}\n"
        f"⏰ Выполнить до {instance.confirm_deadline.strftime('%H:%M')}\n\n"
        f"Отметьте результат:"
    )

    keyboard_dict = {
        "inline_keyboard": [
            [
                {"text": "👍 Выполнено", "callback_data": f"done:{instance.id}"},
                {"text": "⏳ Не успел", "callback_data": f"missed:{instance.id}"},
            ]
        ]
    }
    # Наш Celery task для отправки сообщения
    send_telegram_message.delay(profile.chat_id, text, keyboard_dict=keyboard_dict)


@shared_task
def schedule_reminders_for_today():
    """
    Планирует отправку напоминаний для всех инстансов на сегодня
    строго по времени habit.time_of_day
    """
    now = timezone.now()
    today = timezone.localdate()

    instances = HabitInstance.objects.filter(
        scheduled_datetime__date=today,
        status=HabitInstanceStatus.SCHEDULED,
    ).select_related("habit", "habit__user")

    for instance in instances:
        scheduled_utc = instance.scheduled_datetime

        # если время уже прошло — не планируем
        if scheduled_utc <= now:
            continue

        send_reminder_for_instance.apply_async(
            args=[instance.id],
            eta=scheduled_utc,
        )

        instance.status = HabitInstanceStatus.PENDING
        instance.save(update_fields=["status"])


@shared_task
def send_daily_digest():
    """
    Отправляет пользователю список привычек на сегодня (одним сообщением)
    """
    from django.contrib.auth import get_user_model

    from habit_instances.models import HabitInstance
    from telegrambot.tasks import send_telegram_message

    User = get_user_model()

    # 1. Сегодня по МСК
    now_msk = timezone.now().astimezone(MSK)
    today_msk = now_msk.date()

    # 2. Начало и конец дня по МСК
    start_msk = datetime.combine(today_msk, time.min, tzinfo=MSK)
    end_msk = datetime.combine(today_msk, time.max, tzinfo=MSK)

    # 3. Переводим в UTC, потому что scheduled_datetime хранится в UTC
    start_utc = start_msk.astimezone(UTC)
    end_utc = end_msk.astimezone(UTC)

    users = User.objects.all().select_related("telegram_profile")

    for user in users:
        profile = getattr(user, "telegram_profile", None)
        if not profile or not profile.is_active:
            continue

        instances = (
            HabitInstance.objects.filter(
                habit__user=user,
                scheduled_datetime__gte=start_utc,
                scheduled_datetime__lte=end_utc,
                status=HabitInstanceStatus.SCHEDULED,
            )
            .select_related("habit")
            .order_by("scheduled_datetime")
        )

        if not instances.exists():
            continue

        lines = ["📋 *Ваши привычки на сегодня:*", ""]

        for inst in instances:
            lines.append(f"⏰ {inst.scheduled_datetime.strftime('%H:%M')} — {inst.habit.action}")

        text = "\n".join(lines)

        send_telegram_message.delay(profile.chat_id, text)
