from rest_framework import serializers
from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    grace_minutes = serializers.IntegerField(read_only=True)
    fix_minutes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user", "grace_minutes", "fix_minutes")

    def validate(self, data):
        """
        Бизнес-валидация привычек на уровне API.
        """

        # текущая инстанс-модель (для PATCH)
        instance = getattr(self, "instance", None)

        # значение after update/patch
        is_pleasant = data.get("is_pleasant", instance.is_pleasant if instance else None)
        related = data.get("related_pleasant_habit", instance.related_pleasant_habit if instance else None)
        reward = data.get("reward_text", instance.reward_text if instance else None)

        # --- Приятная привычка ---
        if is_pleasant:
            if related is not None:
                raise serializers.ValidationError("Приятная привычка не может иметь связанную награду.")
            if reward:
                raise serializers.ValidationError("Приятная привычка не может иметь текстовую награду.")

        # --- Полезная привычка ---
        else:
            if bool(related) == bool(reward):
                raise serializers.ValidationError(
                    "Полезная привычка должна иметь ровно одну награду: pleasant или текстовую."
                )

            if related:
                if not related.is_pleasant:
                    raise serializers.ValidationError("В качестве награды можно выбрать только приятную привычку.")
                if related.user_id != self.context["request"].user.id:
                    raise serializers.ValidationError(
                        "Связанная приятная привычка должна принадлежать текущему пользователю."
                    )

        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
