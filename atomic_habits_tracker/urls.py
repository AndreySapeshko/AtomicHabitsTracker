from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("habits.api.urls")),
    path("api/", include("users.api.urls")),
    path("api/", include("habit_instances.api.urls")),
]
