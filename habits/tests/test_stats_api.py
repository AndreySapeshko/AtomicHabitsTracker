from unittest.mock import patch

import pytest
from django.utils import timezone

from habit_instances.models import HabitInstanceStatus
from habit_instances.tests.factory import HabitInstanceFactory

from .factory import HabitFactory

# Маршрут статистики одной привычки
STATS_URL = "/api/habits/{id}/stats/"
HABITS_URL = "/api/habits/"


@pytest.mark.django_db
def test_stats_unauthenticated(api_client):
    response = api_client.get(STATS_URL.format(id=1))
    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_stats_forbidden_for_foreign_habit(auth_client):
    habit = HabitFactory()  # чужой

    response = auth_client.get(STATS_URL.format(id=habit.id))
    assert response.status_code in (403, 404)


@pytest.mark.django_db
def test_stats_streak(auth_client, user):
    habit = HabitFactory(user=user)

    # прошлые дни — пропущены
    for i in range(2):
        HabitInstanceFactory(
            habit=habit,
            scheduled_datetime=timezone.now() - timezone.timedelta(days=5 - i),
            status=HabitInstanceStatus.MISSED,
        )

    # три последних дня — выполнены
    for i in range(3):
        HabitInstanceFactory(
            habit=habit,
            scheduled_datetime=timezone.now() - timezone.timedelta(days=2 - i),
            status=HabitInstanceStatus.COMPLETED,
        )

    response = auth_client.get(STATS_URL.format(id=habit.id))
    assert response.status_code == 200
    data = response.json()

    assert data["current_streak"] == 3
    assert data["max_streak"] >= 3


@pytest.mark.django_db
def test_stats_empty(auth_client, user):
    habit = HabitFactory(user=user)

    response = auth_client.get(STATS_URL.format(id=habit.id))
    assert response.status_code == 200

    data = response.json()

    assert data["total_completed"] == 0
    assert data["total_missed"] == 0
    assert data["total_pending"] == 0
    assert data["current_streak"] == 0


@pytest.mark.django_db
def test_stats_status_distribution(auth_client, user):
    habit = HabitFactory(user=user)

    HabitInstanceFactory(habit=habit, status=HabitInstanceStatus.COMPLETED)
    HabitInstanceFactory(habit=habit, status=HabitInstanceStatus.COMPLETED_LATE)
    HabitInstanceFactory(habit=habit, status=HabitInstanceStatus.MISSED)

    response = auth_client.get(STATS_URL.format(id=habit.id))
    assert response.status_code == 200
    data = response.json()

    assert data["total_completed"] >= 2
    assert data["total_missed"] >= 1


@pytest.mark.django_db
def test_stats_weekly_chart(auth_client, user):
    habit = HabitFactory(user=user)

    monday = timezone.now().replace(hour=10, minute=0) - timezone.timedelta(days=timezone.now().weekday())
    tuesday = monday + timezone.timedelta(days=1)

    HabitInstanceFactory(habit=habit, scheduled_datetime=monday, status=HabitInstanceStatus.COMPLETED)
    HabitInstanceFactory(habit=habit, scheduled_datetime=tuesday, status=HabitInstanceStatus.MISSED)

    response = auth_client.get(STATS_URL.format(id=habit.id))
    assert response.status_code == 200

    weekly = response.json()["per_week"]
    total_result = 0
    for week in weekly:
        total_result += week["completed"] + week["missed"]
    assert total_result >= 2


@pytest.mark.django_db
@patch("habits.api.views.cache")
def test_stats_cached(redis_mock, auth_client, user):
    habit = HabitFactory(user=user)

    # имитируем, что в кеше лежит готовый ответ
    redis_mock.get.return_value = {"cached": True}

    response = auth_client.get(STATS_URL.format(id=habit.id))
    data = response.json()
    assert response.status_code == 200
    assert data["cached"] is True
    redis_mock.get.assert_called_once()


@pytest.mark.django_db
@patch("habits.api.views.cache")
def test_stats_cache_invalidated_on_instance_update(invalidate_mock, auth_client, user):
    habit = HabitFactory(user=user)

    # когда меняем статус, должна быть инвалидация
    url = f"{HABITS_URL}{habit.id}/"
    payload = {"action": "Updated Action"}

    response = auth_client.patch(url, payload, format="json")
    assert response.status_code == 200

    invalidate_mock.delete.assert_any_call(f"habit_stats_{habit.id}")
    assert invalidate_mock.delete.call_count == 2
