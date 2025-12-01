from django.core.cache import cache
from django.db.models import Count, Q
from django.db.models.functions import TruncWeek
from django.utils import timezone
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

    @action(detail=False, methods=["get"], url_path="public", url_name="public")
    def public_habits(self, request):
        """
        GET /api/habits/public/
        Публичные привычки (чужие).
        """
        queryset = Habit.objects.filter(ё=True, is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def _build_details(self):
        habit = self.get_object()

        # --- История инстансов ---
        instances = HabitInstance.objects.filter(habit=habit).order_by("-scheduled_datetime")

        # Счётчики статусов
        stats = instances.aggregate(
            completed=Count("id", filter=Q(status="completed")),
            missed=Count("id", filter=Q(status="missed")),
            pending=Count("id", filter=Q(status__in=["scheduled", "pending"])),
        )

        # --- Стрик ---
        streak = self._calculate_streak(habit)

        # --- Прогресс: сколько осталось по лимиту ---
        remaining = max(habit.repeat_limit - stats["completed"], 0)

        return {
            "habit": HabitSerializer(habit).data,
            "progress": {
                "completed": stats["completed"],
                "missed": stats["missed"],
                "pending": stats["pending"],
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
            ],
        }

    @action(detail=True, methods=["get"])
    def details(self, request, pk=None):
        cache_key = f"habit_details_{pk}"
        data = cache.get(cache_key)

        if not data:
            data = self._build_details()
            cache.set(cache_key, data, 60)

        return Response(data)

    # 🔥 Логика вычисления streak
    def _calculate_streak(self, habit):
        """
        Стрик = количество последовательных выполнений,
        начиная с последнего выполненного подряд без пропусков.
        """
        instances = HabitInstance.objects.filter(habit=habit).order_by("-scheduled_datetime")

        streak = 0

        for inst in instances:
            if inst.status in ("completed", "completed_late"):
                streak += 1
            else:
                break

        return streak

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
    def _calculate_stats(self):
        habit = self.get_object()

        instances = HabitInstance.objects.filter(habit=habit).order_by("scheduled_datetime")

        # Счётчики
        counts = instances.aggregate(
            total_completed=Count("id", filter=Q(status__in=["completed", "completed_late"])),
            total_missed=Count("id", filter=Q(status__in=["missed", "fix_expired"])),
            total_pending=Count("id", filter=Q(status__in=["scheduled", "pending"])),
        )

        # Стрики
        current_streak = self._calculate_current_streak(instances)
        max_streak = self._calculate_max_streak(instances)

        # Прогресс (для полезных habits)
        progress_percent = None
        if not habit.is_pleasant and habit.repeat_limit:
            progress_percent = round((counts["total_completed"] / habit.repeat_limit) * 100, 1)
            progress_percent = min(progress_percent, 100)

        # Последние 30 дней
        today = timezone.now().date()
        last30 = instances.filter(scheduled_datetime__date__gte=today - timezone.timedelta(days=30))

        last_30_days = {inst.scheduled_datetime.date().isoformat(): inst.status for inst in last30}

        # Статистика по неделям

        per_week = (
            HabitInstance.objects.filter(habit=habit)
            .annotate(week=TruncWeek("scheduled_datetime"))
            .values("week")
            .annotate(
                completed=Count("id", filter=Q(status="completed")),
                missed=Count("id", filter=Q(status="missed")),
            )
            .order_by("-week")
        )

        return {
            "habit_id": habit.id,
            "total_completed": counts["total_completed"],
            "total_missed": counts["total_missed"],
            "total_pending": counts["total_pending"],
            "current_streak": current_streak,
            "max_streak": max_streak,
            "limit": habit.repeat_limit,
            "progress_percent": progress_percent,
            "last_30_days": last_30_days,
            "per_week": per_week,
        }

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        cache_key = f"habit_stats_{pk}"
        data = cache.get(cache_key)

        if not data:
            data = self._calculate_stats()
            cache.set(cache_key, data, timeout=60)  # 1 минута

        return Response(data)

    def _calculate_current_streak(self, instances):
        streak = 0
        for inst in reversed(instances):
            if inst.status in ["completed", "completed_late"]:
                streak += 1
            else:
                break
        return streak

    def _calculate_max_streak(self, instances):
        max_streak = 0
        current = 0

        for inst in instances:
            if inst.status in ["completed", "completed_late"]:
                current += 1
            else:
                max_streak = max(max_streak, current)
                current = 0

        return max(max_streak, current)
