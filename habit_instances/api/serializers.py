from rest_framework import serializers

from habit_instances.models import HabitInstance


class HabitInstanceSerializer(serializers.ModelSerializer):
    habit_action = serializers.CharField(source="habit.action", read_only=True)

    class Meta:
        model = HabitInstance
        fields = [
            "id",
            "habit",
            "habit_action",
            "scheduled_datetime",
            "confirm_deadline",
            "status",
        ]
        read_only_fields = ["scheduled_datetime", "confirm_deadline", "status"]
