import logging

from celery import shared_task

from habit_instances.services import create_instances_for_all_habits

logger = logging.getLogger("celery")


@shared_task
def generate_daily_instances():
    created = create_instances_for_all_habits()
    return len(created)


@shared_task
def send_reminder_for_instance(instance_id: int):
    logger.info("Старт задачи send_reminder_for_instance")
    from habit_instances.models import HabitInstance
    from telegrambot.tasks import send_telegram_message

    instance = HabitInstance.objects.filter(id=instance_id).select_related("habit", "habit__user").first()
    logger.info(f"instance с id={instance_id} получен")
    if not instance:
        return logger.info(f"instance с id={instance_id} None")

    habit = instance.habit
    profile = habit.user.telegram_profile

    if not profile or not profile.is_active:
        return logger.info("Телеграмм не подключен")

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
    logger.info("Запуск задачи send_telegram_message")
    send_telegram_message.delay(profile.chat_id, text, keyboard_dict=keyboard_dict)
    logger.info("Отработала задача send_telegram_message")
