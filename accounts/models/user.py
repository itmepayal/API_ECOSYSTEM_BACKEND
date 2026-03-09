import secrets
import hashlib
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from accounts.managers import UserManager
from core.constants import ROLE_CHOICES, ROLE_USER

class User(AbstractBaseUser, PermissionsMixin):

    # --------------------------
    # BASIC INFO
    # --------------------------
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=150, unique=True)
    avatar = models.URLField(blank=True, null=True)

    # --------------------------
    # ROLE
    # --------------------------
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )

    # --------------------------
    # ACCOUNT STATUS
    # --------------------------
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    # --------------------------
    # TOKEN MANAGEMENT
    # --------------------------
    refresh_token_hash = models.CharField(max_length=64, blank=True, null=True)
    refresh_token_expiry = models.DateTimeField(blank=True, null=True)

    forgot_password_token = models.CharField(max_length=255, blank=True, null=True)
    forgot_password_expiry = models.DateTimeField(blank=True, null=True)

    email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    email_verification_expiry = models.DateTimeField(blank=True, null=True)

    # --------------------------
    # TWO FACTOR AUTHENTICATION
    # --------------------------
    is_2fa_enabled = models.BooleanField(default=False)
    totp_secret = models.CharField(max_length=32, blank=True, null=True)

    # --------------------------
    # DJANGO CONFIG
    # --------------------------
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email

    # --------------------------
    # TOKEN GENERATOR
    # --------------------------
    def generate_token(self, token_field, expiry_field, expiry_minutes=10):
        raw_token = secrets.token_hex(20)
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

        expiry = timezone.now() + timezone.timedelta(minutes=expiry_minutes)

        setattr(self, token_field, hashed_token)
        setattr(self, expiry_field, expiry)

        self.save(update_fields=[token_field, expiry_field])

        return raw_token