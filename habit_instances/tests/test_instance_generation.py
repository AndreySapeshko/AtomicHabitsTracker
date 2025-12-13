import pytest

from habit_instances.models import HabitInstance
from habit_instances.services import create_instances_for_all_habits


@pytest.mark.django_db
def test_generate_daily_instances_creates_instances(habit):
    instances = create_instances_for_all_habits()

    assert len(instances) == 1
    instance = instances[0]

    assert instance.habit == habit
    assert instance.status == "scheduled"
    assert instance.scheduled_datetime.tzinfo is not None


@pytest.mark.django_db
def test_generate_daily_instances_is_idempotent(habit):
    create_instances_for_all_habits()
    create_instances_for_all_habits()

    assert HabitInstance.objects.count() == 1
