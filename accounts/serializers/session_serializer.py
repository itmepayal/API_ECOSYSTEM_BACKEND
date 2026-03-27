# =========================================================
# Django REST Framework
# =========================================================
from rest_framework import serializers

# =========================================================
# Accounts Models
# =========================================================
from accounts.models import UserSession

# =========================================================
# USER SESSION SERIALIZER
# =========================================================
class UserSessionSerializer(serializers.ModelSerializer):
    is_current = serializers.SerializerMethodField()

    class Meta:
        model = UserSession
        fields = [
            "id",
            "ip_address",
            "user_agent",
            "created_at",
            "last_activity",
            "expires_at",
            "is_current"
        ]

    def get_is_current(self, obj):
        request = self.context.get("request")
        return str(obj.id) == str(getattr(request, "session_id", None))

# =========================================================
# DELETE SINGLE SESSION
# =========================================================
class DeleteSessionSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()

# =========================================================
# LOGOUT ALL SESSIONS
# =========================================================
class LogoutAllSessionsSerializer(serializers.Serializer):
    confirm = serializers.BooleanField(required=False, default=True)

# =========================================================
# LOGOUT CURRENT SESSION
# =========================================================
class LogoutCurrentSessionSerializer(serializers.Serializer):
    confirm = serializers.BooleanField(required=False, default=True)
