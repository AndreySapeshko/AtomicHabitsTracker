import pytest

from habit_instances.models import HabitInstanceStatus

from .factory import HabitInstanceFactory


@pytest.mark.django_db
def test_habit_instance_mark_completed():
    inst = HabitInstanceFactory()

    inst.mark_completed()

    assert inst.status in [
        HabitInstanceStatus.COMPLETED,
        HabitInstanceStatus.COMPLETED_LATE,
    ]
    assert inst.completed_at is not None


@pytest.mark.django_db
def test_habit_instance_mark_failed():
    inst = HabitInstanceFactory()

    inst.mark_failed()

    assert inst.status in [HabitInstanceStatus.MISSED, HabitInstanceStatus.FIX_EXPIRED]
