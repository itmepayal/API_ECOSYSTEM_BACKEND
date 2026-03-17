from django.db import models
from core.models.base import BaseModel

class APICategory(BaseModel):
    """Group APIs by category."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
