import time
import json
import requests
from rest_framework import serializers
from playground.models import APIPlayground

class APIPlaygroundSerializer(serializers.ModelSerializer):
    api_name = serializers.CharField(source="api.name", read_only=True)
    tested_by_email = serializers.EmailField(source="tested_by.email", read_only=True)

    class Meta:
        model = APIPlayground
        fields = "__all__"
        read_only_fields = [
            "tested_by",
            "response_body",
            "status_code",
            "response_time",
            "headers",
            "status",
            "error",
        ]

    def safe_parse(self, value):
        if not value:
            return {}
        if isinstance(value, dict):
            return value
        try:
            return json.loads(value)
        except:
            return {}

    def create(self, validated_data):
        request_obj = self.context.get("request")

        if request_obj and request_obj.user:
            validated_data["tested_by"] = request_obj.user

        url = validated_data.get("endpoint_url")

        method = validated_data.get("method")

        body = self.safe_parse(validated_data.get("request_body"))
        params = self.safe_parse(validated_data.get("query_params"))
        headers = self.safe_parse(validated_data.get("request_headers"))

        try:
            start_time = time.time()

            response = requests.request(
                method=method,
                url=url,
                json=body,
                params=params,
                headers=headers,
                timeout=10,
            )

            end_time = time.time()

            validated_data["response_body"] = self._parse_response(response)
            validated_data["status_code"] = response.status_code
            validated_data["response_time"] = round(end_time - start_time, 3)
            validated_data["headers"] = dict(response.headers.items())
            validated_data["status"] = "success" if response.ok else "failed"

        except requests.exceptions.Timeout:
            validated_data["status"] = "failed"
            validated_data["error"] = "Request timeout"
            validated_data["response_body"] = {"error": "Timeout"}
            validated_data["response_time"] = None

        except requests.exceptions.RequestException as e:
            validated_data["status"] = "failed"
            validated_data["error"] = str(e)
            validated_data["response_body"] = {"error": str(e)}
            validated_data["response_time"] = None

        return super().create(validated_data)

    def _parse_response(self, response):
        try:
            return response.json()
        except Exception:
            return {"raw": response.text}
        