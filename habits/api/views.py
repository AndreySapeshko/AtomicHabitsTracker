from django.core.cache import cache
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from habit_instances.models import HabitInstance
from habits.api.serializers import HabitSerializer
from habits.models import Habit
from habits.services.details import get_habit_details
from habits.services.stats import get_habit_stats


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
        is_pleasant = False, получим только полезные."""

        qs = (
            Habit.objects.filter(user=self.request.user)
            .select_related("related_pleasant_habit")
            .prefetch_related("reward_for")
        )

        is_pleasant = self.request.query_params.get("is_pleasant")
        if is_pleasant is not None:
            if is_pleasant.lower() == "true":
                qs = qs.filter(is_pleasant=True)
            elif is_pleasant.lower() == "false":
                qs = qs.filter(is_pleasant=False)

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        habit = self.get_object()
        if habit.user != self.request.user:
            raise PermissionDenied("Вы не можете изменять чужую привычку")

        instance = serializer.save()

        # Чистим кеш
        cache.delete(f"habit_details_{instance.id}")
        cache.delete(f"habit_stats_{instance.id}")

        return instance

    @action(detail=False, methods=["get"], url_path="public", url_name="public")
    def public_habits(self, request):
        """
        GET /api/habits/public/
        Публичные привычки (чужие).
        """
        queryset = Habit.objects.filter(is_public=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def details(self, request, pk=None):
        cache_key = f"habit_details_{pk}"
        data = cache.get(cache_key)

        if not data:
            data = get_habit_details(pk)
            cache.set(cache_key, data, 60)

        return Response(data)

    @action(detail=True, methods=["get"])
    def instances(self, request, pk=None):
        """
        GET /api/habits/{id}/instances/
        Список связанных HabitInstance.
        """

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

        return Response(
            [
                {
                    "id": inst.id,
                    "scheduled_datetime": inst.scheduled_datetime,
                    "confirm_deadline": inst.confirm_deadline,
                    "status": inst.status,
                    "completed_at": inst.completed_at,
                    "fix_deadline": inst.fix_deadline,
                }
                for inst in qs
            ]
        )

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        cache_key = f"habit_stats_{pk}"
        data = cache.get(cache_key)

        if not data:
            data = get_habit_stats(pk)
            cache.set(cache_key, data, timeout=60)  # 1 минута

        return Response(data)

    @action(detail=False, methods=["get"], url_path="instances/today")
    def instances_today(self, request):
        user = request.user
        now = timezone.now()

        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59)

        qs = (
            HabitInstance.objects.select_related("habit")
            .filter(
                habit__user=user,
                scheduled_datetime__gte=start,
                scheduled_datetime__lte=end,
            )
            .order_by("scheduled_datetime")
        )

        return Response(
            [
                {
                    "id": inst.id,
                    "scheduled_datetime": inst.scheduled_datetime,
                    "status": inst.status,
                    "habit": inst.habit_id,
                    "action": inst.habit.action,
                    "time": inst.scheduled_datetime.strftime("%H:%M"),
                }
                for inst in qs
            ]
        )
