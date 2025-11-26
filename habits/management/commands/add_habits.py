from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from habits.models import Habit

User = get_user_model()


class Command(BaseCommand):
    help = "Added test habit"

    def handle(self, *args, **options):
        user = User.objects.get(id=1)
        Habit.objects.create(
            user=user,
            action="Test action",
            place="Test place",
            time_of_day="14:30",
            reward_text="Test reward_text",
            periodicity_days=1,
        )
