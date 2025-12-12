from django.contrib import admin

from .models import HabitInstance


@admin.register(HabitInstance)
class HabitInstanceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "habit",
        "user",
        "scheduled_datetime",
        "status",
    )
    list_filter = (
        "status",
        "scheduled_datetime",
        "habit__user",
    )
    search_fields = (
        "habit__action",
        "habit__user__email",
    )
    autocomplete_fields = ("habit",)

    @admin.display(description="User", ordering="habit__user__email")
    def user(self, obj: HabitInstance):
        return obj.habit.user
