from django.core.management.base import BaseCommand
from django.utils import timezone

from habit_instances.models import HabitInstance, HabitInstanceStatus
from habit_instances.tasks import send_reminder_for_instance
from habits.models import Habit


class Command(BaseCommand):
    help = "Test bot send_reminder_for_instance"

    def handle(self, *args, **options):
        habit = Habit.objects.filter(is_pleasant=False, user=1).first()

        instance = HabitInstance.objects.create(
            habit=habit,
            scheduled_datetime=timezone.now(),
            confirm_deadline=timezone.now() + timezone.timedelta(minutes=30),
            fix_deadline=timezone.now() + timezone.timedelta(minutes=60),
            status=HabitInstanceStatus.SCHEDULED,
        )

        send_reminder_for_instance.delay(instance.id)
