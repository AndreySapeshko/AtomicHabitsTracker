# tests/habits/test_api.py
import pytest
from django.urls import reverse

from habits.models import Habit
from users.tests.factory import UserFactory

from .factory import HabitFactory

HABITS_URL = "/api/habits/"


@pytest.mark.django_db
def test_unauthenticated_cannot_access_habits(api_client):
    response = api_client.get(HABITS_URL)
    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_list_habits_returns_only_user_habits(auth_client, user):
    # привычки текущего пользователя
    HabitFactory.create_batch(2, user=user)
    # привычка другого пользователя
    other_user = UserFactory()
    HabitFactory(user=other_user)

    response = auth_client.get(HABITS_URL)

    assert response.status_code == 200
    data = response.json()
    if isinstance(data, dict) and "results" in data:
        results = data["results"]
    else:
        results = data

    assert len(results) == 2
    for item in results:
        assert item["user"] == user.id


@pytest.mark.django_db
def test_create_habit_success(auth_client, user):
    payload = {
        "action": "Do push-ups",
        "place": "Home",
        "time_of_day": "08:00",
        "is_pleasant": False,
        "reward_text": "Watch YouTube for 10 minutes",
        "periodicity_days": 1,
        "repeat_limit": 21,
        "is_public": False,
    }

    response = auth_client.post(HABITS_URL, payload, format="json")
    assert response.status_code == 201, response.content

    data = response.json()
    assert data["action"] == payload["action"]
    assert data["user"] == user.id
    assert Habit.objects.filter(id=data["id"]).exists()


@pytest.mark.django_db
def test_create_pleasant_habit_with_reward_is_invalid(auth_client):
    payload = {
        "action": "Drink coffee",
        "place": "Kitchen",
        "time_of_day": "08:00",
        "is_pleasant": True,
        "reward_text": "Extra croissant",  # запрещено для pleasant
        "periodicity_days": 1,
        "repeat_limit": 21,
    }

    response = auth_client.post(HABITS_URL, payload, format="json")
    assert response.status_code == 400
    data = response.json()
    assert any(key in data for key in ("reward_text", "non_field_errors", "reward"))


@pytest.mark.django_db
def test_create_useful_habit_without_reward_or_pleasant_is_invalid(auth_client):
    payload = {
        "action": "Read a book",
        "place": "Living room",
        "time_of_day": "20:00",
        "is_pleasant": False,
        "reward_text": None,
        "related_pleasant_habit": None,
        "periodicity_days": 1,
        "repeat_limit": 21,
    }

    response = auth_client.post(HABITS_URL, payload, format="json")
    assert response.status_code == 400
    data = response.json()

    assert "non_field_errors" in data or "reward_text" in data


@pytest.mark.django_db
def test_retrieve_habit_detail(auth_client, habit):
    url = f"{HABITS_URL}{habit.id}/"

    response = auth_client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == habit.id
    assert data["action"] == habit.action


@pytest.mark.django_db
def test_cannot_retrieve_other_user_habit(auth_client):
    # привычка другого пользователя
    habit = HabitFactory()

    url = f"{HABITS_URL}{habit.id}/"
    response = auth_client.get(url)

    assert response.status_code in (403, 404)


@pytest.mark.django_db
def test_partial_update_habit(auth_client, habit):
    url = f"{HABITS_URL}{habit.id}/"
    payload = {"action": "Updated Action"}

    response = auth_client.patch(url, payload, format="json")
    assert response.status_code == 200

    habit.refresh_from_db()
    assert habit.action == "Updated Action"


@pytest.mark.django_db
def test_cannot_update_other_user_habit(auth_client):
    # чужая привычка
    other_habit = HabitFactory()
    url = f"{HABITS_URL}{other_habit.id}/"

    response = auth_client.patch(url, {"action": "Hack"}, format="json")
    assert response.status_code in (403, 404)


@pytest.mark.django_db
def test_delete_habit(auth_client, habit):
    url = f"{HABITS_URL}{habit.id}/"

    response = auth_client.delete(url)
    assert response.status_code in (204, 200, 202)

    assert not Habit.objects.filter(id=habit.id).exists()


@pytest.mark.django_db
def test_cannot_delete_other_user_habit(auth_client):
    other_habit = HabitFactory()
    url = f"{HABITS_URL}{other_habit.id}/"

    response = auth_client.delete(url)
    assert response.status_code in (403, 404)
    assert Habit.objects.filter(id=other_habit.id).exists()
