import pytest
from rest_framework.test import APIClient

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
