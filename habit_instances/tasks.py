from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from celery import shared_task

from habit_instances.services import create_instances_for_all_habits


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
        return  # telegram не подключён

    text = (
        f"Напоминание по привычке:\n\n"
        f"🏷 {habit.action}\n"
        f"📍 {habit.place}\n"
        f"⏰ Выполнить до {instance.confirm_deadline.strftime('%H:%M')}\n\n"
        f"Отметьте результат:"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👍 Выполнено", callback_data=f"done:{instance.id}"),
                InlineKeyboardButton(text="⏳ Не успел", callback_data=f"missed:{instance.id}"),
            ]
        ]
    )
    # Наш Celery task для отправки сообщения
    send_telegram_message.delay(profile.chat_id, text, reply_markup=keyboard)
