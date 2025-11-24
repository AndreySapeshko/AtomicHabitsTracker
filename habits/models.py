from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


# Интервалы (вынесены за пределы класса — теперь доступны внутри)
HABIT_INTERVALS = [
    {"periodicity_days": 1, "grace_minutes": 60, "fix_minutes": 300},
    {"periodicity_days": 2, "grace_minutes": 120, "fix_minutes": 480},
    {"periodicity_days": 3, "grace_minutes": 180, "fix_minutes": 600},
    {"periodicity_days": 5, "grace_minutes": 240, "fix_minutes": 720},
    {"periodicity_days": 7, "grace_minutes": 60, "fix_minutes": 300},
]


def get_periodicity_choices():
    choices = []
    for interval in HABIT_INTERVALS:
        days = interval["periodicity_days"]
        unit = "дней"
        if days == 1:
            unit = "день"
        elif 1 < days < 5:
            unit = "дня"
        choices.append((days, f"{days} {unit}."))
    return choices


PERIODICITY_CHOICES = get_periodicity_choices()

LIMIT_CHOICES = [
    (21, "Стандарт 21 повтор"),
    (30, "Челендж 30 повторов"),
    (45, "Марафон 45 повторов"),
]


class Habit(models.Model):
    """
    Определение привычки (полезной или приятной).
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")

    action = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    time_of_day = models.TimeField()

    # Тип
    is_pleasant = models.BooleanField(default=False)

    related_pleasant_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reward_for",
        help_text="Приятная привычка – награда.",
    )

    reward_text = models.CharField(
        max_length=255, null=True, blank=True, help_text="Текстовая награда, если не pleasant habit."
    )

    periodicity_days = models.PositiveSmallIntegerField(
        choices=PERIODICITY_CHOICES, default=1, help_text="1, 2, 3, 5, 7 дней."
    )

    repeat_limit = models.PositiveSmallIntegerField(
        choices=LIMIT_CHOICES, default=21, help_text="21, 30, 45 повторов."
    )

    # Окна ожидания — теперь настоящие DB-поля
    grace_minutes = models.PositiveIntegerField()
    fix_minutes = models.PositiveIntegerField()

    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # Автоматическое назначение grace/fix по periodicity
        interval = next((i for i in HABIT_INTERVALS if i["periodicity_days"] == self.periodicity_days), None)

        if interval:
            self.grace_minutes = interval["grace_minutes"]
            self.fix_minutes = interval["fix_minutes"]

        super().save(*args, **kwargs)

    def clean(self):
        # Приятная привычка
        if self.is_pleasant:
            if self.related_pleasant_habit is not None:
                raise ValidationError("Приятная привычка не может иметь связанную награду.")
            if self.reward_text:
                raise ValidationError("Приятная привычка не может иметь текстовую награду.")

        else:
            # Полезная привычка — ровно одно наградное поле
            related = self.related_pleasant_habit
            reward = self.reward_text

            if bool(related) == bool(reward):
                raise ValidationError(
                    "Полезная привычка должна иметь либо pleasant habit, либо reward text (только одно)."
                )

            if related:
                if not related.is_pleasant:
                    raise ValidationError("В качестве награды может выступать только приятная привычка.")
                if related.user_id != self.user_id:
                    raise ValidationError("Наградная привычка должна принадлежать тому же пользователю.")

        super().clean()

    def __str__(self):
        return f"Habit({self.action}, pleasant={self.is_pleasant})"
