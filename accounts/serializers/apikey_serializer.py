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
        fields = ["id", "key", "usage_limit", "created_at"]
        read_only_fields = ["key", "created_at"]
