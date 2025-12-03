from django.db.models import Count, Prefetch, Q

from habit_instances.models import HabitInstance
from habits.api.serializers import HabitSerializer
from habits.models import Habit


def _calculate_streak(habit):
    """
    Стрик = количество последовательных выполнений,
    начиная с последнего выполненного подряд без пропусков.
    """
    instances = HabitInstance.objects.filter(habit=habit).order_by("-scheduled_datetime")

    streak = 0

    for inst in instances:
        if inst.status in ("completed", "completed_late"):
            streak += 1
        else:
            break

    return streak


def get_habit_details(habit_id):
    habit = (
        Habit.objects.filter(id=habit_id)
        .prefetch_related(Prefetch("instances", queryset=HabitInstance.objects.order_by("scheduled_datetime")))
        .first()
    )

    instances = habit.instances.all() if habit else []
    # Счётчики статусов
    stats = instances.aggregate(
        completed=Count("id", filter=Q(status="completed")),
        missed=Count("id", filter=Q(status="missed")),
        pending=Count("id", filter=Q(status__in=["scheduled", "pending"])),
    )

    # --- Стрик ---
    streak = _calculate_streak(habit)

    # --- Прогресс: сколько осталось по лимиту ---
    remaining = max(habit.repeat_limit - stats["completed"], 0)

    return {
        "habit": HabitSerializer(habit).data,
        "progress": {
            "completed": stats["completed"],
            "missed": stats["missed"],
            "pending": stats["pending"],
            "remaining": remaining,
            "streak": streak,
        },
        "instances": [
            {
                "id": inst.id,
                "scheduled_datetime": inst.scheduled_datetime,
                "status": inst.status,
            }
            for inst in instances[:20]
        ],
    }
