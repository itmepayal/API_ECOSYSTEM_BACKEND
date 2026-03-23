from rest_framework import serializers
from accounts.models import APIKey

class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ["id", "key", "usage_limit", "created_at"]
        read_only_fields = ["key", "created_at"]
        