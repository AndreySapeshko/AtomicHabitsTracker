from django.db import models
from django.utils import timezone


class HabitInstanceStatus(models.TextChoices):
    SCHEDULED = "scheduled", "Scheduled"
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    COMPLETED_LATE = "completed_late", "Completed Late"
    MISSED = "missed", "Missed"
    FIX_EXPIRED = "fix_expired", "Fix Expired"


class HabitInstance(models.Model):
    """
    Конкретный запуск привычки в определённый день-время.
    Создаётся планировщиком.
    """

    habit = models.ForeignKey(
        "habits.Habit",
        on_delete=models.CASCADE,
        related_name="instances"
    )

    scheduled_datetime = models.DateTimeField()
    confirm_deadline = models.DateTimeField()
    fix_deadline = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=HabitInstanceStatus.choices,
        default=HabitInstanceStatus.SCHEDULED
    )

    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["scheduled_datetime"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["scheduled_datetime"]),
        ]

    def __str__(self):
        return f"Instance({self.habit.action} at {self.scheduled_datetime} — {self.status})"

    @property
    def is_open_for_completion(self):
        now = timezone.now()
        return (
            self.status in {HabitInstanceStatus.SCHEDULED, HabitInstanceStatus.PENDING, HabitInstanceStatus.MISSED}
            and now <= self.fix_deadline
        )

