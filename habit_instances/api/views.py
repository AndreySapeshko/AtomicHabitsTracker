from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.core.cache import cache

from habit_instances.models import HabitInstance

from .serializers import HabitInstanceSerializer


class HabitInstanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HabitInstanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = HabitInstance.objects.filter(habit__user=self.request.user).select_related("habit")

        # today
        today_param = self.request.query_params.get("today")
        if today_param and today_param.lower() in ("1", "true", "yes"):
            today = timezone.localdate()
            qs = qs.filter(scheduled_datetime__date=today)

        # status
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)

        return qs

    @action(methods=["post"], detail=True)
    def mark_complete(self, request, pk=None):
        instance = self.get_object()
        if instance.status != HabitInstance.Status.SCHEDULED and instance.status != HabitInstance.Status.PENDING:
            return Response({"error": "Already processed"}, status=400)
        instance.mark_completed()
        return Response({"status": "completed"})

    @action(methods=["post"], detail=True)
    def mark_missed(self, request, pk=None):
        instance = self.get_object()
        if instance.status != HabitInstance.Status.SCHEDULED and instance.status != HabitInstance.Status.PENDING:
            return Response({"error": "Already processed"}, status=400)
        instance.mark_failed()
        return Response({"status": "missed"})


    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.habit.user != self.request.user:
            raise PermissionDenied("Вы не можете изменять чужой инстанц")

        instance = serializer.save()

        # Чистим кеш
        cache.delete(f"habit_details_{instance.habit.id}")
        cache.delete(f"habit_stats_{instance.habit.id}")

        return instance
