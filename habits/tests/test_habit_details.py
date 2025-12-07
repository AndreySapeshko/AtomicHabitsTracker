from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from habit_instances.models import HabitInstance
from habits.models import Habit
from habits.services.details import _calculate_streak, get_habit_details

User = get_user_model()

# -------------------------------------------------
# STREAK TESTS
# -------------------------------------------------


@pytest.mark.django_db
def test_streak_all_completed(habit):
    now = timezone.now()

    for i in range(3):
        HabitInstance.objects.create(
            habit=habit,
            scheduled_datetime=now - timedelta(days=i),
            confirm_deadline=now - timedelta(days=i) + timedelta(hours=5),
            fix_deadline=now - timedelta(days=i) + timedelta(hours=8),
            status="completed",
        )

    streak = _calculate_streak(habit)
    assert streak == 3


@pytest.mark.django_db
def test_streak_breaks_on_missed(habit):
    now = timezone.now()

    HabitInstance.objects.create(
        habit=habit,
        scheduled_datetime=now,
        confirm_deadline=now + timedelta(hours=5),
        fix_deadline=now + timedelta(hours=8),
        status="missed",
    )
    HabitInstance.objects.create(
        habit=habit,
        scheduled_datetime=now - timedelta(days=1),
        confirm_deadline=now + timedelta(hours=5),
        fix_deadline=now + timedelta(hours=8),
        status="completed",
    )

    streak = _calculate_streak(habit)
    assert streak == 0


@pytest.mark.django_db
def test_streak_stops_at_first_non_completed(habit):
    now = timezone.now()

    HabitInstance.objects.create(
        habit=habit,
        scheduled_datetime=now,
        confirm_deadline=now + timedelta(hours=5),
        fix_deadline=now + timedelta(hours=8),
        status="completed",
    )
    HabitInstance.objects.create(
        habit=habit,
        scheduled_datetime=now - timedelta(days=1),
        confirm_deadline=now + timedelta(hours=5),
        fix_deadline=now + timedelta(hours=8),
        status="scheduled",
    )
    HabitInstance.objects.create(
        habit=habit,
        scheduled_datetime=now - timedelta(days=2),
        confirm_deadline=now + timedelta(hours=5),
        fix_deadline=now + timedelta(hours=8),
        status="completed",
    )

    streak = _calculate_streak(habit)
    assert streak == 1


# -------------------------------------------------
# HABIT DETAILS TEST
# -------------------------------------------------


@pytest.mark.django_db
def test_get_habit_details_counts(habit_d):
    now = timezone.now()

    HabitInstance.objects.create(
        habit=habit_d,
        scheduled_datetime=now,
        confirm_deadline=now + timedelta(hours=5),
        fix_deadline=now + timedelta(hours=8),
        status="completed",
    )
    HabitInstance.objects.create(
        habit=habit_d,
        scheduled_datetime=now - timedelta(days=1),
        confirm_deadline=now + timedelta(hours=5),
        fix_deadline=now + timedelta(hours=8),
        status="missed",
    )
    HabitInstance.objects.create(
        habit=habit_d,
        scheduled_datetime=now - timedelta(days=2),
        confirm_deadline=now + timedelta(hours=5),
        fix_deadline=now + timedelta(hours=8),
        status="scheduled",
    )

    data = get_habit_details(habit_d.id)

    assert data["progress"]["completed"] == 1
    assert data["progress"]["missed"] == 1
    assert data["progress"]["pending"] == 1
    assert data["progress"]["remaining"] == 4
    assert data["progress"]["streak"] == 1


@pytest.mark.django_db
def test_get_habit_details_returns_instances(habit):
    now = timezone.now()

    inst = HabitInstance.objects.create(
        habit=habit,
        scheduled_datetime=now,
        status="completed",
        confirm_deadline=now + timedelta(hours=5),
        fix_deadline=now + timedelta(hours=8),
    )

    data = get_habit_details(habit.id)

    assert len(data["instances"]) == 1
    assert data["instances"][0]["id"] == inst.id


@pytest.mark.django_db
def test_instances_limit_20(habit_d):
    now = timezone.now()

    for i in range(25):
        HabitInstance.objects.create(
            habit=habit_d,
            scheduled_datetime=now - timedelta(days=i),
            status="completed",
            confirm_deadline=now - timedelta(days=i) + timedelta(hours=5),
            fix_deadline=now - timedelta(days=i) + timedelta(hours=8),
        )

    data = get_habit_details(habit_d.id)
    assert len(data["instances"]) == 20


# -------------------------------------------------
# HABIT MODEL: SAVE / CLEAN / STR
# -------------------------------------------------


@pytest.mark.django_db
def test_grace_and_fix_auto_set_on_save(user):
    habit = Habit.objects.create(
        user=user,
        action="Drink",
        place="Home",
        is_pleasant=False,
        reward_text="Candy",
        periodicity_days=3,
        repeat_limit=21,
    )

    assert habit.grace_minutes == 180
    assert habit.fix_minutes == 600


@pytest.mark.django_db
def test_clean_fails_for_invalid_pleasant(user):
    pleasant = Habit(
        user=user,
        action="Game",
        place="PC",
        is_pleasant=True,
        reward_text="INVALID",
    )

    with pytest.raises(ValidationError):
        pleasant.clean()


@pytest.mark.django_db
def test_clean_fails_when_both_rewards_filled(user):
    pleasant = Habit.objects.create(
        user=user,
        action="Movie",
        place="Home",
        is_pleasant=True,
    )

    habit = Habit(
        user=user,
        action="Sport",
        place="Gym",
        is_pleasant=False,
        related_pleasant_habit=pleasant,
        reward_text="Candy",
    )

    with pytest.raises(ValidationError):
        habit.clean()


@pytest.mark.django_db
def test_clean_only_one_reward_allowed(user):
    pleasant = Habit.objects.create(
        user=user,
        action="Movie",
        place="Home",
        is_pleasant=True,
    )

    habit = Habit(
        user=user,
        action="Run",
        place="Street",
        is_pleasant=False,
        related_pleasant_habit=pleasant,
    )

    habit.clean()


@pytest.mark.django_db
def test_clean_fails_if_pleasant_reward_not_pleasant(user):
    bad_reward = Habit.objects.create(
        user=user,
        action="Work",
        place="Office",
        is_pleasant=False,
        reward_text="Money",
    )

    habit = Habit(
        user=user,
        action="Sport",
        place="Gym",
        is_pleasant=False,
        related_pleasant_habit=bad_reward,
    )

    with pytest.raises(ValidationError):
        habit.clean()


@pytest.mark.django_db
def test_str(user):
    habit = Habit.objects.create(
        user=user,
        action="Run",
        place="Park",
        is_pleasant=False,
        reward_text="Candy",
    )

    assert str(habit) == "Habit(Run, pleasant=False)"
