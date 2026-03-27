# =========================================================
# Django REST Framework
# =========================================================
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

# =========================================================
# Accounts Models & Selectors
# =========================================================
from accounts.models import User
from accounts.selectors import get_user_by_email

# =========================================================
# REGISTER SERIALIZER
# =========================================================
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=8, write_only=True)

    # -------------------------
    # Validate Email
    # -------------------------
    def validate_email(self, value):
        if get_user_by_email(value):
            raise serializers.ValidationError("Email already exists")
        return value

    # -------------------------
    # Validate Username
    # -------------------------
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken")
        return value

# =========================================================
# LOGIN SERIALIZER
# =========================================================
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

# =========================================================
# VERIFY EMAIL SERIALIZER
# =========================================================
class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()

# =========================================================
# RESEND VERIFICATION SERIALIZER
# =========================================================
class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

# =========================================================
# FORGOT PASSWORD SERIALIZER
# =========================================================
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

# =========================================================
# RESET PASSWORD SERIALIZER
# =========================================================
class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=8)

# =========================================================
# CHANGE PASSWORD SERIALIZER
# =========================================================
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

# =========================================================
# GOOGLE LOGIN SERIALIZER
# =========================================================
class GoogleLoginSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

# =========================================================
# LOGOUT SERIALIZER
# =========================================================
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
    
    def validate(self, attrs):
        try:
            attrs["token"] = RefreshToken(attrs["refresh_token"])
        except Exception:
            raise ValidationError("Invalid refresh token")
        return attrs

# =========================================================
# REFRESH TOKEN SERIALIZER
# =========================================================
class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
    
    def validate(self, attrs):
        try:
            attrs["token"] = RefreshToken(attrs["refresh_token"])
        except Exception:
            raise ValidationError("Invalid refresh token")
        return attrs
        
