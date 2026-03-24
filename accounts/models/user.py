import uuid
import secrets
import hashlib
from datetime import timedelta

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.managers.user_manager import UserManager
from core.models.base import BaseModel
from core.constants import (
    ROLE_CHOICES,
    ROLE_USER,
    LOGIN_EMAIL,
    LOGIN_TYPE_CHOICES
)

# =========================================================
# USER MODEL
# =========================================================
class User(AbstractBaseUser, PermissionsMixin, BaseModel):

    # -------------------------
    # BASIC INFO
    # -------------------------
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=150, unique=True)
    avatar = models.URLField(blank=True, null=True)

    login_type = models.CharField(
        max_length=20,
        choices=LOGIN_TYPE_CHOICES,
        default=LOGIN_EMAIL
    )

    # -------------------------
    # ROLE & STATUS
    # -------------------------
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )

    is_blocked = models.BooleanField(default=False)
    blocked_reason = models.TextField(blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # -------------------------
    # LOGIN TRACKING
    # -------------------------
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_user_agent = models.CharField(max_length=512, null=True, blank=True)

    # -------------------------
    # TIMESTAMPS
    # -------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -------------------------
    # TOKEN MANAGEMENT
    # -------------------------
    refresh_token_hash = models.CharField(max_length=64, blank=True, null=True)
    refresh_token_expiry = models.DateTimeField(blank=True, null=True)

    forgot_password_token = models.CharField(max_length=64, blank=True, null=True)
    forgot_password_expiry = models.DateTimeField(blank=True, null=True)

    email_verification_token = models.CharField(max_length=64, blank=True, null=True)
    email_verification_expiry = models.DateTimeField(blank=True, null=True)

    # -------------------------
    # 2FA
    # -------------------------
    is_2fa_enabled = models.BooleanField(default=False)
    totp_secret = models.CharField(max_length=32, blank=True, null=True)

    # -------------------------
    # DJANGO CONFIG
    # -------------------------
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["username"]),
        ]

    def __str__(self):
        return self.email

    # -------------------------
    # AVATAR
    # -------------------------
    @property
    def avatar_url(self):
        if self.avatar and self.avatar.startswith("http"):
            return self.avatar
        return f"https://api.dicebear.com/7.x/adventurer/svg?seed={self.username}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            self.avatar = self.avatar_url
        super().save(*args, **kwargs)

    # -------------------------
    # TOKEN GENERATOR
    # -------------------------
    def generate_token(self, token_field, expiry_field, expiry_minutes=10):
        raw_token = secrets.token_hex(20)
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

        expiry = timezone.now() + timedelta(minutes=expiry_minutes)

        setattr(self, token_field, hashed_token)
        setattr(self, expiry_field, expiry)

        self.save(update_fields=[token_field, expiry_field])

        return raw_token


# =========================================================
# API KEY MODEL
# =========================================================
class APIKey(BaseModel):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="api_keys"
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    usage_limit = models.PositiveIntegerField(default=1000)
    usage_count = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["key"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.name}"
    