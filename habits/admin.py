from django.contrib import admin
from django.utils import timezone

from habit_instances.models import HabitInstance, HabitInstanceStatus

from .models import Habit


class CompletedHabitInstanceInline(admin.TabularInline):
    model = HabitInstance
    extra = 0
    can_delete = False
    fields = ("scheduled_datetime", "status")
    readonly_fields = ("scheduled_datetime", "status")
    verbose_name_plural = "Выполненные инстансы"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(
            status__in=[
                HabitInstanceStatus.COMPLETED,
                HabitInstanceStatus.COMPLETED_LATE,
            ]
        )


class MissedHabitInstanceInline(admin.TabularInline):
    model = HabitInstance
    extra = 0
    can_delete = False
    fields = ("scheduled_datetime", "status")
    readonly_fields = ("scheduled_datetime", "status")
    verbose_name_plural = "Пропущенные инстансы"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(
            status__in=[
                HabitInstanceStatus.MISSED,
                HabitInstanceStatus.FIX_EXPIRED,
            ]
        )


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "action",
        "is_pleasant",
        "next_instance_time",
        "completed_count",
        "missed_count",
    )
    list_filter = ("is_pleasant",)
    search_fields = ("action", "user__email")
    autocomplete_fields = ("user",)

    inlines = [CompletedHabitInstanceInline, MissedHabitInstanceInline]

    @admin.display(description="Следующий инстанс")
    def next_instance_time(self, obj: Habit):
        now = timezone.now()
        next_instance = (
            HabitInstance.objects.filter(habit=obj, scheduled_datetime__gte=now).order_by("scheduled_datetime").first()
        )
        if not next_instance:
            return "—"
        return f"{next_instance.scheduled_datetime} ({next_instance.status})"

    @admin.display(description="Выполнено")
    def completed_count(self, obj: Habit):
        return HabitInstance.objects.filter(
            habit=obj,
            status__in=[
                HabitInstanceStatus.COMPLETED,
                HabitInstanceStatus.COMPLETED_LATE,
            ],
        ).count()

    @admin.display(description="Пропущено")
    def missed_count(self, obj: Habit):
        return HabitInstance.objects.filter(
            habit=obj,
            status__in=[
                HabitInstanceStatus.MISSED,
                HabitInstanceStatus.FIX_EXPIRED,
            ],
        ).count()
