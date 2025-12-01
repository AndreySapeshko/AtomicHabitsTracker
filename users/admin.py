from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .model_files.profile import TelegramProfile
from .model_files.user import User


class TelegramProfileInline(admin.StackedInline):
    model = TelegramProfile
    can_delete = False
    fk_name = "user"
    extra = 0
    readonly_fields = ("chat_id", "binding_code", "is_active")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [TelegramProfileInline]
    ordering = ("email",)
    list_display = ("email", "is_staff", "is_superuser", "has_telegram", "telegram_chat_id")
    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_superuser"),
            },
        ),
    )

    @admin.display(description="Telegram привязан", boolean=True)
    def has_telegram(self, obj):
        return hasattr(obj, "telegramprofile") and obj.telegramprofile.is_active

    @admin.display(description="Telegram chat_id")
    def telegram_chat_id(self, obj):
        if hasattr(obj, "telegramprofile"):
            return obj.telegramprofile.chat_id
        return "—"
