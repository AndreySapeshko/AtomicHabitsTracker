from rest_framework.routers import DefaultRouter

from habit_instances.api.views import HabitInstanceViewSet

router = DefaultRouter()
router.register(r"habit_instance", HabitInstanceViewSet, basename="habit_instance")

urlpatterns = router.urls
