from django.contrib import admin
from accounts.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "username",
        "role",
        "is_verified",
        "is_staff",
        "is_active",
        "created_at",
    )

    search_fields = ("email", "username")

    list_filter = (
        "role",
        "is_verified",
        "is_staff",
        "is_active",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("email", "username", "avatar")
        }),

        ("Role", {
            "fields": ("role",)
        }),

        ("Account Status", {
            "fields": ("is_verified", "is_active", "is_staff")
        }),

        ("Security", {
            "fields": (
                "refresh_token_hash",
                "refresh_token_expiry",
                "forgot_password_token",
                "forgot_password_expiry",
                "email_verification_token",
                "email_verification_expiry",
            )
        }),

        ("Two Factor Authentication", {
            "fields": ("is_2fa_enabled", "totp_secret")
        }),

        ("Metadata", {
            "fields": ("created_at",)
        }),
    )
    