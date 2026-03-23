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
    LOGIN_GOOGLE, 
    LOGIN_TYPE_CHOICES
)

# =========================================================
# User Model
# =========================================================
class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    # -----------------------------------------------------
    # BASIC USER INFORMATION
    # -----------------------------------------------------
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=150, unique=True)
    avatar = models.URLField(blank=True, null=True)
    login_type = models.CharField(
        max_length=20,
        choices=LOGIN_TYPE_CHOICES,
        default=LOGIN_EMAIL
    )

    # -----------------------------------------------------
    # ROLE BASED ACCESS CONTROL
    # -----------------------------------------------------
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )

    # -----------------------------------------------------
    # ACCOUNT STATUS FLAGS
    # -----------------------------------------------------
    is_blocked = models.BooleanField(default=False)    
    blocked_reason = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # -----------------------------------------------------
    # TIMESTAMP FIELDS
    # -----------------------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -----------------------------------------------------
    # TOKEN MANAGEMENT
    # -----------------------------------------------------
    refresh_token_hash = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )

    # Expiration time of refresh token
    refresh_token_expiry = models.DateTimeField(
        blank=True,
        null=True
    )

    # Token used for password reset functionality
    forgot_password_token = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # Expiry time for password reset token
    forgot_password_expiry = models.DateTimeField(
        blank=True,
        null=True
    )

    # Token used for email verification
    email_verification_token = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # Expiry time for email verification token
    email_verification_expiry = models.DateTimeField(
        blank=True,
        null=True
    )


    # -----------------------------------------------------
    # TWO FACTOR AUTHENTICATION (2FA)
    # -----------------------------------------------------
    # Indicates if 2FA is enabled for the user
    is_2fa_enabled = models.BooleanField(default=False)

    # Secret key used for generating TOTP codes
    totp_secret = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )


    # -----------------------------------------------------
    # DJANGO AUTHENTICATION CONFIGURATION
    # -----------------------------------------------------
    # Email is used as the unique identifier for login
    USERNAME_FIELD = "email"

    # Required fields when creating a user via createsuperuser
    REQUIRED_FIELDS = ["username"]

    # Custom user manager
    objects = UserManager()

    # -----------------------------------------------------
    # DATABASE INDEX CONFIGURATION
    # -----------------------------------------------------
    class Meta:
        """
        Adds database indexes to improve query performance.
        """
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["username"]),
        ]


    # -----------------------------------------------------
    # STRING REPRESENTATION
    # -----------------------------------------------------
    def __str__(self):
        """
        Return the string representation of the user.
        """
        return self.email


    # -----------------------------------------------------
    # TOKEN GENERATOR
    # -----------------------------------------------------
    def generate_token(self, token_field, expiry_field, expiry_minutes=10):
        """
        Generate a secure token and store its hashed version.

        Parameters
        ----------
        token_field : str
            Model field where hashed token will be stored.

        expiry_field : str
            Model field where token expiry time will be stored.

        expiry_minutes : int
            Number of minutes before the token expires.

        Returns
        -------
        str
            Raw token that can be sent to the user (via email).
        """

        # Generate a secure random token
        raw_token = secrets.token_hex(20)

        # Hash the token before storing it in the database
        hashed_token = hashlib.sha256(
            raw_token.encode()
        ).hexdigest()

        expiry = timezone.now() + timedelta(minutes=expiry_minutes)

        setattr(self, token_field, hashed_token)
        setattr(self, expiry_field, expiry)

        self.save(update_fields=[token_field, expiry_field])

        return raw_token

class APIKey(BaseModel):
    """API keys for accessing endpoints."""
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_keys")
    usage_limit = models.IntegerField(default=1000)

    def __str__(self):
        return f"{self.user.username} - {self.key}"
    