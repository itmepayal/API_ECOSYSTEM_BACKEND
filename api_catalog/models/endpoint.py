from django.db import models
from core.models.base import BaseModel
from api_catalog.models.category import APICategory

class APIEndpoint(BaseModel):
    """Main API endpoint model."""
    METHOD_CHOICES = [
        ("GET", "GET"),
        ("POST", "POST"),
        ("PUT", "PUT"),
        ("DELETE", "DELETE"),
    ]

    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        APICategory, on_delete=models.CASCADE, related_name="apis"
    )
    endpoint = models.CharField(max_length=500)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    description = models.TextField()
    is_public = models.BooleanField(default=True)
    request_schema = models.JSONField(blank=True, null=True)
    response_schema = models.JSONField(blank=True, null=True)
    example_request = models.JSONField(blank=True, null=True)
    example_response = models.JSONField(blank=True, null=True)
    rate_limit = models.IntegerField(default=100)

    def __str__(self):
        return self.name
    