import uuid
import hashlib
import secrets
from datetime import timedelta

from django.db import models
from django.utils import timezone

from accounts.models import User
from core.models.base import BaseModel

# =========================================================
# USER SESSION MODEL
# =========================================================
class UserSession(BaseModel):
    # -----------------------------------------------------
    # RELATIONSHIP
    # -----------------------------------------------------
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    # -----------------------------------------------------
    # SECURITY
    # -----------------------------------------------------
    token_hash = models.CharField(
        max_length=64,
        unique=True,
        help_text="SHA256 hash of session token"
    )

    # -----------------------------------------------------
    # DEVICE & NETWORK INFO
    # -----------------------------------------------------
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text="User IP address"
    )

    user_agent = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text="Browser / device information"
    )
    
    # -----------------------------------------------------
    # EXPIRY MANAGEMENT
    # -----------------------------------------------------
    expires_at = models.DateTimeField(
        help_text="Session expiration time"
    )

    # -----------------------------------------------------
    # TIMESTAMPS
    # -----------------------------------------------------
    last_activity = models.DateTimeField(auto_now=True)

    # -----------------------------------------------------
    # DATABASE INDEXES
    # -----------------------------------------------------
    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["token_hash"]),
        ]

    # -----------------------------------------------------
    # STRING REPRESENTATION
    # -----------------------------------------------------
    def __str__(self):
        return f"{self.user.email} - session"

    # -----------------------------------------------------
    # TOKEN GENERATION
    # -----------------------------------------------------
    @staticmethod
    def generate_session_token():
        raw_token = secrets.token_hex(32)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

        return raw_token, token_hash

    # -----------------------------------------------------
    # SET SESSION EXPIRY
    # -----------------------------------------------------
    def set_expiry(self, days=7):
        self.expires_at = timezone.now() + timedelta(days=days)