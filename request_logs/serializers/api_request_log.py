from rest_framework import serializers
from request_logs.models import APIRequestLog

class APIRequestLogSerializer(serializers.ModelSerializer):
    api_name = serializers.CharField(source="api.name", read_only=True)
    api_endpoint = serializers.CharField(source="api.endpoint", read_only=True)
    api_method = serializers.CharField(source="api.method", read_only=True)

    class Meta:
        model = APIRequestLog
        fields = [
            "id",
            "api",
            "api_name",
            "api_endpoint",
            "api_method",
            "api_key",
            "method",
            "status_code",
            "response_time",
            "ip_address",
            "path",
            "user_agent",
            "request_id",
            "created_at",
        ]
        read_only_fields = fields