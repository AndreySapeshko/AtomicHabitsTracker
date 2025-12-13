from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone

from habit_instances.models import HabitInstance
from habit_instances.tasks import schedule_reminders_for_today


@pytest.mark.django_db
def test_schedule_reminders_calls_apply_async(habit):

    habit_instance = HabitInstance.objects.create(
        habit=habit,
        scheduled_datetime=timezone.now() + timedelta(hours=4),
        confirm_deadline=timezone.now() + timedelta(hours=3),
        fix_deadline=timezone.now() + timedelta(hours=4),
        status="scheduled",
    )
    with patch("habit_instances.tasks.send_reminder_for_instance.apply_async") as mocked_apply:
        print(f"habit_instance: {habit_instance}")
        schedule_reminders_for_today()

        mocked_apply.assert_called_once()

        _, kwargs = mocked_apply.call_args
        assert "eta" in kwargs


@pytest.mark.django_db
def test_no_reminder_for_past_time(habit_instance):
    habit_instance.scheduled_datetime = timezone.now() - timezone.timedelta(hours=1)
    habit_instance.save()

    with patch("habit_instances.tasks.send_reminder_for_instance.apply_async") as mocked_apply:
        schedule_reminders_for_today()
        mocked_apply.assert_not_called()
