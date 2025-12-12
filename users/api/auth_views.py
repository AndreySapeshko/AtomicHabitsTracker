from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "ok"}, status=status.HTTP_201_CREATED)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        telegram_profile = getattr(user, "telegram_profile", None)

        return Response(
            {
                "id": user.id,
                "email": user.email,
                "telegram_linked": telegram_profile.is_active if telegram_profile else False,
                "telegram_username": telegram_profile.username if telegram_profile else None,
            }
        )
