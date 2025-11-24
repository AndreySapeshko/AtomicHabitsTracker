from rest_framework.routers import DefaultRouter

from habits.api.views import HabitViewSet

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habits")

urlpatterns = router.urls
