from django.db import models
from core.models.base import BaseModel
from accounts.models import User
from api_catalog.models import APIEndpoint

class APIPlayground(BaseModel):
    """Stores playground/test data for APIs."""
    api = models.ForeignKey(APIEndpoint, on_delete=models.CASCADE)
    tested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    request_body = models.JSONField(blank=True, null=True)
    response_body = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.api.name} tested by {self.tested_by}"