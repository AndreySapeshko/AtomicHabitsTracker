import uuid

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.model_files.profile import TelegramProfile


class CreateBindingCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile, _ = TelegramProfile.objects.get_or_create(user=request.user)
        code = uuid.uuid4().hex[:8].upper()
        profile.binding_code = code
        profile.save()

        return Response({"binding_code": code})


class BindTelegramView(APIView):

    def post(self, request):
        chat_id = request.data.get("chat_id")
        code = request.data.get("code")

        if not chat_id or not code:
            return Response({"error": "chat_id and code required"}, status=400)

        try:
            profile = TelegramProfile.objects.get(binding_code=code)
        except TelegramProfile.DoesNotExist:
            return Response({"error": "Invalid binding code"}, status=404)

        profile.chat_id = str(chat_id)
        profile.is_active = True
        profile.binding_code = None
        profile.save()

        return Response({"status": "ok"})
