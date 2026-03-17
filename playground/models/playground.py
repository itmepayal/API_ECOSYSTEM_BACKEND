from django.db import models
from core.models.base import BaseModel
from accounts.models import User
from api_catalog.models import APIEndpoint


class APIPlayground(BaseModel):
    """Stores playground/test data for APIs."""

    api = models.ForeignKey(APIEndpoint, on_delete=models.CASCADE)

    tested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    method = models.CharField(max_length=10)
    endpoint_url = models.URLField(blank=True, null=True)
    request_body = models.JSONField(blank=True, null=True)
    query_params = models.JSONField(null=True, blank=True)
    request_headers = models.JSONField(null=True, blank=True)

    response_body = models.JSONField(blank=True, null=True)
    status_code = models.IntegerField(null=True, blank=True)
    response_time = models.FloatField(null=True, blank=True)
    headers = models.JSONField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("success", "Success"),
            ("failed", "Failed"),
        ],
        default="success"
    )

    error = models.TextField(null=True, blank=True)

    def __str__(self):
        user = self.tested_by.email if self.tested_by else "Anonymous"
        return f"{self.api.name} tested by {user}"