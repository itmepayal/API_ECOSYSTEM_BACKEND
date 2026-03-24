from rest_framework import serializers
from accounts.models import User
from accounts.selectors.user_selector import get_user_by_email

# =========================================================
# Register Serializer
# =========================================================
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(
        min_length=8,
        write_only=True
    )
    
    def validate_email(self, value):
        if get_user_by_email(value):
            raise serializers.ValidationError(
                "Email already exists"
            )

        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already taken"
            )

        return value


# =========================================================
# Login Serializer
# =========================================================
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


# =========================================================
# Email Verification Serializer
# =========================================================
class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()

# =========================================================
# Resend Verification Email Serializer
# =========================================================
class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

# =========================================================
# Forgot Password Serializer
# =========================================================
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


# =========================================================
# Reset Password Serializer
# =========================================================
class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(
        min_length=8
    )

# =========================================================
# Change Password Serializer
# =========================================================
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(
        min_length=8
    )

# =========================================================
# Google Login Serializer
# =========================================================
class GoogleLoginSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
