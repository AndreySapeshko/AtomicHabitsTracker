import pytest
from django.core.exceptions import ValidationError

from .factory import HabitFactory


@pytest.mark.django_db
def test_pleasant_habit_cannot_have_reward():
    habit = HabitFactory(is_pleasant=True, reward_text="Some reward")

    with pytest.raises(ValidationError):
        habit.full_clean()


@pytest.mark.django_db
def test_useful_habit_must_have_reward_or_pleasant():
    habit = HabitFactory(is_pleasant=False, reward_text=None, related_pleasant_habit=None)

    with pytest.raises(ValidationError):
        habit.full_clean()
