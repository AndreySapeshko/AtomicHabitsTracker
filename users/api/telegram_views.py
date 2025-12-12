import json
import logging
import uuid

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from telegrambot.tasks import process_update_task
from users.model_files.profile import TelegramProfile

logger = logging.getLogger("telegrambot")


class CreateBindingCodeView(APIView):
    """Создание кодя для привязки Telegram аккаунта пользователя"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile, _ = TelegramProfile.objects.get_or_create(user=request.user)
        code = "bind" + uuid.uuid4().hex[:8].upper()
        profile.binding_code = code
        profile.save()

        return Response({"code": code})


class BindTelegramView(APIView):
    """Реализация привязки Telegram аккаунта пользователя,
    вызывается отправкой боту кода полученного в web-приложении."""

    permission_classes = []

    def post(self, request):
        chat_id = request.data.get("chat_id")
        code = request.data.get("code")
        username = request.data.get("username")

        if not chat_id or not code:
            return Response({"error": "chat_id and code required"}, status=400)

        try:
            profile = TelegramProfile.objects.get(binding_code=code)
        except TelegramProfile.DoesNotExist:
            return Response({"error": "Invalid binding code"}, status=404)

        profile.chat_id = str(chat_id)
        profile.username = username
        profile.is_active = True
        profile.binding_code = None
        profile.save()

        return Response({"status": "ok"})


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            process_update_task.delay(payload)
        except Exception as e:
            print("Webhook error:", e)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "invalid"})
