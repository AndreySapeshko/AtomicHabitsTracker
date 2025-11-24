from datetime import datetime, timedelta

from django.utils import timezone

from habit_instances.models import HabitInstance, HabitInstanceStatus
from habits.models import Habit


def get_next_scheduled_datetime(habit: Habit) -> datetime:
    """
    Возвращает datetime следующего выполнения привычки.
    Простой MVP:
      - следующее выполнение = сегодня + periodicity_days
      - время = habit.time_of_day
    """
    now = timezone.now()
    next_date = now.date() + timedelta(days=habit.periodicity_days)
    scheduled = timezone.make_aware(datetime.combine(next_date, habit.time_of_day))
    return scheduled


def should_generate_instance(habit: Habit) -> bool:
    """
    Проверяем, нужно ли создавать новый инстанс.
    - Если все лимиты исчерпаны → False
    - Если на нужную дату инстанс уже есть → False
    """

    if habit.is_pleasant:
        return False  # pleasant привычки не генерируем

    # Проверка лимита повторений
    count = habit.instances.count()
    if habit.repeat_limit is not None and count >= habit.repeat_limit:
        return False

    next_date = timezone.now().date() + timedelta(days=habit.periodicity_days)

    exists = habit.instances.filter(scheduled_datetime__date=next_date).exists()

    return not exists


def create_instance_for_habit(habit: Habit) -> HabitInstance | None:
    """
    Создаёт HabitInstance, если нужно.
    Возвращает созданный объект или None.
    """

    if not should_generate_instance(habit):
        return None

    scheduled = get_next_scheduled_datetime(habit)

    # Вычисляем окна дедлайнов
    confirm_deadline = scheduled + timedelta(minutes=habit.grace_minutes)
    fix_deadline = scheduled + timedelta(minutes=habit.fix_minutes)

    instance = HabitInstance.objects.create(
        habit=habit,
        scheduled_datetime=scheduled,
        confirm_deadline=confirm_deadline,
        fix_deadline=fix_deadline,
        status=HabitInstanceStatus.SCHEDULED,
    )

    return instance


def create_instances_for_all_habits():
    habits = Habit.objects.filter(is_active=True)

    created = []

    for habit in habits:
        instance = create_instance_for_habit(habit)
        if instance:
            created.append(instance)

    return created
