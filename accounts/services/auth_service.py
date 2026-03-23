import hashlib
import uuid

from google.oauth2 import id_token
from google.auth.transport import requests

from django.utils import timezone
from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from accounts.models import User
from accounts.selectors.user_selector import get_user_by_email

from core.constants import LOGIN_EMAIL, LOGIN_GOOGLE
from core.email.send_email import send_email


class AuthService:

    # =====================================================
    # INTERNAL HELPERS 
    # =====================================================
    @staticmethod
    def _validate_token(token: str):
        """
        Ensures token is valid and not garbage input.
        """
        if not token or not isinstance(token, str):
            raise ValidationError("Invalid token")

        if token in ["undefined", "null", ""]:
            raise ValidationError("Invalid token")

        if len(token) < 20:  
            raise ValidationError("Invalid token format")

        return token.strip()

    @staticmethod
    def _hash_token(token: str):
        return hashlib.sha256(token.encode()).hexdigest()
    
    @staticmethod
    def generate_tokens(user):
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }

    # =====================================================
    # Register User
    # =====================================================
    @staticmethod
    def register_user(email, username, password):

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            login_type=LOGIN_EMAIL
        )

        raw_token = user.generate_token(
            token_field="email_verification_token",
            expiry_field="email_verification_expiry",
            expiry_minutes=10
        )

        verify_link = f"{settings.FRONTEND_URL}/verify-email/{raw_token}"

        send_email(
            to_email=user.email,
            subject="Verify your email",
            template_id=settings.SENDGRID_EMAIL_VERIFICATION_TEMPLATE_ID,
            dynamic_data={
                "username": user.username,
                "verification_code": raw_token,
                "verify_link": verify_link
            }
        )

        return user

    # =====================================================
    # Verify Email
    # =====================================================
    @staticmethod
    def verify_email(token):

        token = AuthService._validate_token(token)
        hashed_token = AuthService._hash_token(token)

        user = User.objects.filter(
            email_verification_token=hashed_token,
            email_verification_expiry__gt=timezone.now()
        ).first()

        if not user:
            raise ValidationError("Invalid or expired token")

        user.is_verified = True
        user.email_verification_token = None
        user.email_verification_expiry = None
        user.save(update_fields=[
            "is_verified",
            "email_verification_token",
            "email_verification_expiry"
        ])

        return user

    # =====================================================
    # Login User
    # =====================================================
    @staticmethod
    def login_user(email, password):

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials")
        
        if user.is_blocked:
            raise AuthenticationFailed("Account is blocked")

        if user.login_type == LOGIN_GOOGLE:
            raise AuthenticationFailed("Please login using Google")

        if not user.is_verified:
            raise AuthenticationFailed("Email not verified")

        if not user.is_active:
            raise AuthenticationFailed("Account is disabled")

        return {
            "user": user,
            "requires_2fa": user.is_2fa_enabled
        }

    # =====================================================
    # Forgot Password
    # =====================================================
    @staticmethod
    def forgot_password(email):

        user = get_user_by_email(email)

        if not user:
            return  

        token = user.generate_token(
            "forgot_password_token",
            "forgot_password_expiry",
            15
        )

        reset_link = f"{settings.FRONTEND_URL}/reset-password/{token}"

        send_email(
            to_email=user.email,
            subject="Reset Password",
            template_id=settings.SENDGRID_PASSWORD_RESET_TEMPLATE_ID,
            dynamic_data={
                "username": user.username,
                "reset_link": reset_link
            }
        )

        return token

    # =====================================================
    # Reset Password
    # =====================================================
    @staticmethod
    def reset_password(token, password):

        token = AuthService._validate_token(token)
        hashed = AuthService._hash_token(token)

        user = User.objects.filter(
            forgot_password_token=hashed,
            forgot_password_expiry__gt=timezone.now()
        ).first()

        if not user:
            raise ValidationError("Invalid or expired token")

        user.set_password(password)
        user.forgot_password_token = None
        user.forgot_password_expiry = None
        user.save(update_fields=[
            "password",
            "forgot_password_token",
            "forgot_password_expiry"
        ])

        return user

    # =====================================================
    # Change Password
    # =====================================================
    @staticmethod
    def change_password(user, old_password, new_password):

        if not user.check_password(old_password):
            raise ValidationError("Old password is incorrect")

        user.set_password(new_password)
        user.save(update_fields=["password"])

        return user

    # =====================================================
    # Google Login
    # =====================================================
    @staticmethod
    def google_login(token):

        token = AuthService._validate_token(token)

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            if idinfo["aud"] != settings.GOOGLE_CLIENT_ID:
                raise ValidationError("Invalid audience")

        except ValueError:
            raise ValidationError("Invalid Google token")

        email = idinfo.get("email")
        name = idinfo.get("name") or "user"
        avatar = idinfo.get("picture")

        if not email:
            raise ValidationError("Google account has no email")

        username = f"{name.replace(' ', '').lower()}_{uuid.uuid4().hex[:6]}"

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": username,
                "avatar": avatar,
                "is_verified": True,
                "login_type": LOGIN_GOOGLE
            }
        )

        if not created and user.login_type != LOGIN_GOOGLE:
            user.login_type = LOGIN_GOOGLE
            user.save(update_fields=["login_type"])

        if not user.avatar and avatar:
            user.avatar = avatar
            user.save(update_fields=["avatar"])

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }