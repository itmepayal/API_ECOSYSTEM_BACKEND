from rest_framework import serializers
from accounts.models import User
from accounts.selectors.user_selector import get_user_by_email

# =========================================================
# Register Serializer
# =========================================================
class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration.

    Validates:
    - Email format and uniqueness
    - Username uniqueness
    - Password minimum length
    """

    # ---------------------------------
    # USER INPUT FIELDS
    # ---------------------------------

    # User email address
    email = serializers.EmailField()

    # Unique username
    username = serializers.CharField(max_length=150)

    # Password must be at least 8 characters
    password = serializers.CharField(
        min_length=8,
        write_only=True
    )


    # ---------------------------------
    # EMAIL VALIDATION
    # ---------------------------------
    def validate_email(self, value):
        """
        Ensure email is unique in the system.
        """

        if get_user_by_email(value):
            raise serializers.ValidationError(
                "Email already exists"
            )

        return value


    # ---------------------------------
    # USERNAME VALIDATION
    # ---------------------------------
    def validate_username(self, value):
        """
        Ensure username is not already taken.
        """

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already taken"
            )

        return value


# =========================================================
# Login Serializer
# =========================================================
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Validates:
    - Email format
    - Password presence

    Authentication is handled in the service layer.
    """

    email = serializers.EmailField()
    password = serializers.CharField()


# =========================================================
# Email Verification Serializer
# =========================================================
class VerifyEmailSerializer(serializers.Serializer):
    """
    Serializer used to verify a user's email address.

    The verification token is generated during registration
    and sent via email.
    """

    token = serializers.CharField()


# =========================================================
# Resend Verification Email Serializer
# =========================================================
class ResendVerificationSerializer(serializers.Serializer):
    """
    Serializer used when a user requests a new
    email verification link.
    """

    email = serializers.EmailField()


# =========================================================
# Forgot Password Serializer
# =========================================================
class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer used to initiate password reset.

    User submits their email address to receive
    a password reset link.
    """

    email = serializers.EmailField()


# =========================================================
# Reset Password Serializer
# =========================================================
class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer used to reset a user's password
    using a valid reset token.
    """

    # Password reset token
    token = serializers.CharField()

    # New password (minimum security requirement)
    password = serializers.CharField(
        min_length=8
    )


# =========================================================
# Change Password Serializer
# =========================================================
class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer used when an authenticated user
    wants to change their password.

    Requires:
    - Old password verification
    - New password validation
    """

    # Current password
    old_password = serializers.CharField()

    # New password with minimum length requirement
    new_password = serializers.CharField(
        min_length=8
    )

# =========================================================
# Google Login Serializer
# =========================================================
class GoogleLoginSerializer(serializers.Serializer):
    """
    Serializer for Google login
    """
    token = serializers.CharField(required=True)