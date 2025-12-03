from habit_instances.models import HabitInstance


def bold(text: str) -> str:
    return f"<b>{text}</b>"


def italic(text: str) -> str:
    return f"<i>{text}</i>"


def habit_card(habit):
    return (
        f"{bold('🏷 Привычка:')} {habit.action}\n"
        f"{bold('📍 Место:')} {habit.place}\n"
        f"{bold('⏰ Время:')} {habit.time_of_day}\n"
        f"{bold('🔁 Частота:')} {habit.periodicity_days} дней\n"
        f"{bold('🔥 Статус:')} {'Активна' if habit.is_active else 'Неактивна'}\n"
    )


def instance_line(instance: HabitInstance):
    dt = instance.scheduled_datetime.strftime("%d.%m %H:%M")
    emoji = {
        "completed": "✔",
        "completed_late": "⏳",
        "missed": "❌",
        "pending": "⏸",
        "scheduled": "🕒",
    }.get(instance.status, "❔")

    return f"{emoji} {dt} — {instance.status}"
