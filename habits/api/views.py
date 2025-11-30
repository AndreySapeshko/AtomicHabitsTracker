from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from habit_instances.models import HabitInstance
from habits.api.serializers import HabitSerializer
from habits.models import Habit


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Только владелец может менять свои привычки.
    Публичные — доступны только для чтения.
    """

    def has_object_permission(self, request, view, obj):
        # безопасные методы: GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # изменять может только владелец
        return obj.user_id == request.user.id


class HabitViewSet(viewsets.ModelViewSet):
    """
    CRUD для привычек пользователя.
    Дополнительно:
      - /public/ — список публичных привычек
      - /{id}/instances/ — связанные инстансы (для статистики)
    """

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """Пользователь видит только свои привычки.
        Указав значение is_pleasant = True, получим только приятные,
        is_pleasant = False, получим только полезные. """

        qs = Habit.objects.filter(user=self.request.user)

        is_pleasant = self.request.query_params.get("is_pleasant")
        if is_pleasant is not None:
            if is_pleasant.lower() == "true":
                qs = qs.filter(is_pleasant=True)
            elif is_pleasant.lower() == "false":
                qs = qs.filter(is_pleasant=False)

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="public", url_name="public")
    def public_habits(self, request):
        """
        GET /api/habits/public/
        Публичные привычки (чужие).
        """
        queryset = Habit.objects.filter(ё=True, is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="instances", url_name="instances")
    def instances(self, request, pk=None):
        """
        GET /api/habits/{id}/instances/
        Список связанных HabitInstance.
        """
        habit = self.get_object()
        queryset = habit.instances.order_by("-scheduled_datetime")
        data = [
            {
                "id": i.id,
                "scheduled": i.scheduled_datetime,
                "status": i.status,
                "completed_at": i.completed_at,
                "confirm_deadline": i.confirm_deadline,
                "fix_deadline": i.fix_deadline,
            }
            for i in queryset
        ]
        return Response(data)

    @action(detail=True, methods=["get"])
    def details(self, request, pk=None):
        habit = self.get_object()

        # --- История инстансов ---
        instances = (
            HabitInstance.objects
            .filter(habit=habit)
            .order_by("-scheduled_datetime")
        )

        # Счётчики статусов
        completed = instances.filter(status="completed").count()
        missed = instances.filter(status="missed").count()
        pending = instances.filter(status__in=["scheduled", "pending"]).count()

        # --- Стрик ---
        streak = self._calculate_streak(habit)

        # --- Прогресс: сколько осталось по лимиту ---
        remaining = max(habit.repeat_limit - completed, 0)

        return Response({
            "habit": HabitSerializer(habit).data,
            "progress": {
                "completed": completed,
                "missed": missed,
                "pending": pending,
                "remaining": remaining,
                "streak": streak,
            },
            "instances": [
                {
                    "id": inst.id,
                    "scheduled_datetime": inst.scheduled_datetime,
                    "status": inst.status,
                }
                for inst in instances[:20]
            ]
        })

    # 🔥 Логика вычисления streak
    def _calculate_streak(self, habit):
        """
        Стрик = количество последовательных выполнений,
        начиная с последнего выполненного подряд без пропусков.
        """
        instances = (
            HabitInstance.objects
            .filter(habit=habit)
            .order_by("-scheduled_datetime")
        )

        streak = 0

        for inst in instances:
            if inst.status in ("completed", "completed_late"):
                streak += 1
            else:
                break

        return streak

    @action(detail=True, methods=["get"])
    def instances(self, request, pk=None):
        habit = self.get_object()

        qs = HabitInstance.objects.filter(habit=habit).order_by("-scheduled_datetime")

        # фильтр по статусу
        status = request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)

        # фильтр по дате
        date = request.query_params.get("date")
        if date:
            qs = qs.filter(scheduled_datetime__date=date)

        return Response([
            {
                "id": inst.id,
                "scheduled_datetime": inst.scheduled_datetime,
                "confirm_deadline": inst.confirm_deadline,
                "status": inst.status,
            }
            for inst in qs
        ])

