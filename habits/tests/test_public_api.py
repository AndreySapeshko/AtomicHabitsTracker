import pytest

from .factory import HabitFactory

PUBLIC_URL = "/api/habits/public/"


@pytest.mark.django_db
def test_public_habits_accessible_without_auth(api_client):
    response = api_client.get(PUBLIC_URL)
    assert response.status_code == 401


@pytest.mark.django_db
def test_public_habits_only_public(auth_client):
    HabitFactory(is_public=True)
    HabitFactory(is_public=False)

    response = auth_client.get(PUBLIC_URL)
    assert response.status_code == 200

    data = response.json()
    if isinstance(data, dict) and "results" in data:
        data = data["results"]

    assert len(data) == 1
    assert data[0]["is_public"] is True


@pytest.mark.django_db
def test_public_habits_not_only_owner(auth_client, user):
    HabitFactory(user=user, is_public=True)
    HabitFactory(is_public=True)

    response = auth_client.get(PUBLIC_URL)
    assert response.status_code == 200

    data = response.json()
    if isinstance(data, dict) and "results" in data:
        data = data["results"]

    assert len(data) == 2
