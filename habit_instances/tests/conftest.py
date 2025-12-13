from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from habits.models import Habit
from habits.tests.factory import HabitFactory
from users.tests.factory import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def auth_client(api_client, user):
    """Аутентифицированный клиент (обходит JWT через force_authenticate)."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def habit(user):
    return HabitFactory(user=user)


@pytest.fixture
def habit_now(user):
    return Habit.objects.create(
        user=user,
        action="Drink water",
        place="Home",
        time_of_day=(timezone.now() + timedelta(hours=4)).time(),
        is_active=True,
        is_pleasant=False,
    )


@pytest.fixture
def habit_instance(habit_now):
    from habit_instances.services import create_instance_for_habit

    return create_instance_for_habit(habit_now)
