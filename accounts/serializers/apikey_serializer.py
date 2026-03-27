# =========================================================
# Django Rest Framework
# =========================================================
from rest_framework import serializers

# =========================================================
# Accounts Models
# =========================================================
from accounts.models import APIKey

# =========================================================
# Serializer
# =========================================================
class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = [
            "id",
            "name",
            "prefix",
            "usage_limit",
            "usage_count",
            "expires_at",
            "created_at",
        ]
        read_only_fields = ["prefix", "usage_count", "created_at"]

    def validate_expires_at(self, value):
        if value and value <= timezone.now():
            raise serializers.ValidationError("Expiration must be in the future")
        return value
    