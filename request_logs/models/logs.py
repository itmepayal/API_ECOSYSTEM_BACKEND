from django.db import models
from core.models.base import BaseModel
from accounts.models.user import APIKey
from api_catalog.models import APIEndpoint

class APIRequestLog(BaseModel):
    """Tracks every API request made."""
    api = models.ForeignKey(APIEndpoint, on_delete=models.CASCADE)
    api_key = models.ForeignKey(APIKey, on_delete=models.SET_NULL, null=True, blank=True)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    response_time = models.FloatField() 
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.api.name} - {self.status_code}"
