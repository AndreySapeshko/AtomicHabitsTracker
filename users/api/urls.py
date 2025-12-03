from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.api.auth_views import MeView, RegisterView
from users.api.telegram_views import BindTelegramView, CreateBindingCodeView

urlpatterns = [
    path("telegram/create_binding/", CreateBindingCodeView.as_view()),
    path("telegram/bind/", BindTelegramView.as_view()),
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", MeView.as_view(), name="auth_me"),
]
