from unittest.mock import patch

import pytest
from django.utils import timezone

from habit_instances.tasks import send_daily_digest
from habit_instances.tests.factory import HabitInstanceFactory
from habits.tests.factory import HabitFactory
from telegrambot.tests.factory import ProfileFactory
from users.tests.factory import UserFactory


@pytest.mark.django_db
def test_daily_digest_sends_message():
    user = UserFactory()
    profile = ProfileFactory(user=user)
    habit = HabitFactory(user=user)
    HabitInstanceFactory(habit=habit, scheduled_datetime=timezone.now())

    with patch("telegrambot.tasks.send_telegram_message.delay") as mocked_send:
        send_daily_digest()

        mocked_send.assert_called_once()
        args, kwargs = mocked_send.call_args

        assert profile.chat_id in args
        assert "Ваши привычки на сегодня" in args[1]


@pytest.mark.django_db
def test_no_digest_if_no_instances(user):
    with patch("telegrambot.tasks.send_telegram_message.delay") as mocked_send:
        send_daily_digest()
        mocked_send.assert_not_called()
