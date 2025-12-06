import pytest
from django.utils import timezone

from habits.tests.factory import HabitFactory

from .factory import HabitInstanceFactory

# INSTANCES_URL = f"/api/habits/{id}/instances/"
TODAY_URL = "/api/habits/instances/today/"


def get_instances_url(habit):
    return f"/api/habits/{habit.id}/instances/"


@pytest.mark.django_db
def test_unauthenticated_cannot_access_instances(api_client, habit):
    url = get_instances_url(habit)
    response = api_client.get(url)
    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_list_instances_returns_only_user_data(auth_client, user):
    habit = HabitFactory(user=user)
    my_inst = HabitInstanceFactory(habit=habit)
    url = get_instances_url(habit)

    # чужой инстанс
    foreign_inst = HabitInstanceFactory()

    response = auth_client.get(url)
    assert response.status_code == 200

    data = response.json()
    if isinstance(data, dict) and "results" in data:
        data = data["results"]

    ids = {item["id"] for item in data}

    assert my_inst.id in ids
    assert foreign_inst.id not in ids


@pytest.mark.django_db
def test_list_instances_by_habit(auth_client, user):
    habit = HabitFactory(user=user)
    HabitInstanceFactory.create_batch(3, habit=habit)

    other_habit = HabitFactory(user=user)
    HabitInstanceFactory.create_batch(2, habit=other_habit)

    url = get_instances_url(habit)

    response = auth_client.get(url)
    assert response.status_code == 200

    data = response.json()
    if isinstance(data, dict) and "results" in data:
        data = data["results"]

    assert len(data) == 3


@pytest.mark.django_db
def test_today_instances(auth_client, user):
    # сегодня
    habit = HabitFactory(user=user)
    today_inst = HabitInstanceFactory(
        habit=habit,
        scheduled_datetime=timezone.now().replace(hour=10, minute=0),
    )

    # завтра
    tomorrow_inst = HabitInstanceFactory(
        habit=habit,
        scheduled_datetime=timezone.now() + timezone.timedelta(days=1),
    )

    response = auth_client.get(TODAY_URL)
    assert response.status_code == 200

    data = response.json()
    if isinstance(data, dict) and "results" in data:
        data = data["results"]

    ids = {item["id"] for item in data}

    assert today_inst.id in ids
    assert tomorrow_inst.id not in ids


@pytest.mark.django_db
def test_cannot_retrieve_foreign_today_instances(auth_client, user):
    habit = HabitFactory(user=user)
    HabitInstanceFactory.create_batch(3, habit=habit)

    other_user_habit = HabitFactory()
    HabitInstanceFactory.create_batch(2, habit=other_user_habit)

    url = get_instances_url(habit)

    response = auth_client.get(url)
    assert response.status_code == 200

    data = response.json()
    if isinstance(data, dict) and "results" in data:
        data = data["results"]

    assert len(data) == 3
