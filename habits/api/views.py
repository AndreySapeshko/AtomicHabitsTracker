from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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
        """Пользователь видит только свои привычки."""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="public", url_name="public")
    def public_habits(self, request):
        """
        GET /api/habits/public/
        Публичные привычки (чужие).
        """
        queryset = Habit.objects.filter(is_public=True, is_active=True)
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
