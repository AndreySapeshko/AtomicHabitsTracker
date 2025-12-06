from django.db.models import Count, Prefetch, Q
from django.db.models.functions import TruncWeek
from django.utils import timezone

from habit_instances.models import HabitInstance
from habits.models import Habit


def _calculate_current_streak(instances):
    streak = 0
    for inst in reversed(instances):
        if inst.status in ["completed", "completed_late"]:
            streak += 1
        else:
            break
    return streak


def _calculate_max_streak(instances):
    max_streak = 0
    current = 0

    for inst in instances:
        if inst.status in ["completed", "completed_late"]:
            current += 1
        else:
            max_streak = max(max_streak, current)
            current = 0

    return max(max_streak, current)


def get_habit_stats(habit_id):
    try:
        habit = (
            Habit.objects.filter(id=habit_id)
            .prefetch_related(Prefetch("instances", queryset=HabitInstance.objects.order_by("scheduled_datetime")))
            .first()
        )
    except Habit.DoesNotExist:
        return None

    instances = habit.instances.all() if habit else []

    # Счётчики
    counts = instances.aggregate(
        total_completed=Count("id", filter=Q(status__in=["completed", "completed_late"])),
        total_missed=Count("id", filter=Q(status__in=["missed", "fix_expired"])),
        total_pending=Count("id", filter=Q(status__in=["scheduled", "pending"])),
    )

    # Стрики
    current_streak = _calculate_current_streak(instances)
    max_streak = _calculate_max_streak(instances)

    # Прогресс (для полезных habits)
    progress_percent = None
    if not habit.is_pleasant and habit.repeat_limit:
        progress_percent = round((counts["total_completed"] / habit.repeat_limit) * 100, 1)
        progress_percent = min(progress_percent, 100)

    # Последние 30 дней
    today = timezone.now().date()
    last30 = instances.filter(scheduled_datetime__date__gte=today - timezone.timedelta(days=30))

    last_30_days = {inst.scheduled_datetime.date().isoformat(): inst.status for inst in last30}

    # Статистика по неделям

    per_week = (
        HabitInstance.objects.filter(habit=habit)
        .annotate(week=TruncWeek("scheduled_datetime"))
        .values("week")
        .annotate(
            completed=Count("id", filter=Q(status="completed")),
            missed=Count("id", filter=Q(status="missed")),
        )
        .order_by("-week")
    )

    return {
        "habit_id": habit.id,
        "total_completed": counts["total_completed"],
        "total_missed": counts["total_missed"],
        "total_pending": counts["total_pending"],
        "current_streak": current_streak,
        "max_streak": max_streak,
        "limit": habit.repeat_limit,
        "progress_percent": progress_percent,
        "last_30_days": last_30_days,
        "per_week": per_week,
    }
