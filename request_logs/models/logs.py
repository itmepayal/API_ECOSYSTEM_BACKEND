import uuid
from django.db import models

from core.models.base import BaseModel
from accounts.models.user import APIKey
from api_catalog.models.endpoint import APIEndpoint


class APIRequestLog(BaseModel):
    api = models.ForeignKey(APIEndpoint, on_delete=models.SET_NULL, null=True)
    api_key = models.ForeignKey(APIKey, on_delete=models.SET_NULL, null=True, blank=True)

    method = models.CharField(max_length=10)
    status_code = models.IntegerField()

    response_time = models.FloatField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    path = models.CharField(max_length=500, db_index=True)
    user_agent = models.TextField(blank=True, null=True)

    request_id = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=["api"]),
            models.Index(fields=["api_key"]),
            models.Index(fields=["status_code"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["method"]),
            models.Index(fields=["path"]),
        ]

    def __str__(self):
        api_name = self.api.name if self.api else "Unknown API"
        return f"{api_name} - {self.status_code}"