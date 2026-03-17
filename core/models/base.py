from django.db import models
from django.utils import timezone
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True) 

    class Meta:
        abstract = True  

    def soft_delete(self):
        self.is_active = False
        self.save(update_fields=["is_active"])

    def restore(self):
        self.is_active = True
        self.save(update_fields=["is_active"])

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        