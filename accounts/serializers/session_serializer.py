from rest_framework import serializers
from accounts.models.session import UserSession

# =========================================================
# User Session Serializer
# =========================================================
class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = ["id", "ip_address", "user_agent", "created_at", "last_activity", "is_active"]
    