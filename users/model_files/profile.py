from django.conf import settings
from django.db import models


class TelegramProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="telegram_profile")

    chat_id = models.CharField(max_length=64, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.CharField(max_length=64, default="UTC")
    is_active = models.BooleanField(default=False)
    binding_code = models.CharField(max_length=32, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["chat_id"], name="unique_chat_id_not_null", condition=~models.Q(chat_id=None)
            )
        ]

    def __str__(self):
        return f"TelegramProfile({self.user.email} active={self.is_active})"
