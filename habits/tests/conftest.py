import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from users.tests.factory import UserFactory

from ..models import Habit
from .factory import HabitFactory

User = get_user_model()


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
def habit_d(user):
    return Habit.objects.create(
        user=user,
        action="Run",
        place="Park",
        is_pleasant=False,
        reward_text="Candy",
        periodicity_days=1,
        repeat_limit=5,
    )
