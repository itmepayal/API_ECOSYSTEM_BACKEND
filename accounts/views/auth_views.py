from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from core.api.base_view import BaseAPIView
from core.throttles.auth_throttle import AuthThrottle

from accounts.serializers.auth_serializer import (
    RegisterSerializer,
    LoginSerializer,
    VerifyEmailSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    ForgotPasswordSerializer,
    GoogleLoginSerializer
)

from accounts.serializers.user_serializer import UserSerializer
from accounts.services.auth_service import AuthService


# =========================================================
# User Registration
# =========================================================
class RegisterView(BaseAPIView):
    """
    API endpoint for user registration.

    Responsibilities:
    - Validate registration data
    - Create new user account
    - Send email verification token

    Security:
    - Public endpoint
    - Rate limited
    """

    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthService.register_user(**serializer.validated_data)

        return self.success_response(
            message="User registered successfully. Please verify your email.",
            data=UserSerializer(user).data,
            status_code=status.HTTP_201_CREATED
        )


# =========================================================
# User Login
# =========================================================
class LoginView(BaseAPIView):
    """
    API endpoint for user login.

    Responsibilities:
    - Validate login credentials
    - Authenticate user
    - Generate JWT access and refresh tokens
    """

    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = AuthService.login_user(**serializer.validated_data)

        return self.success_response(
            message="Login successful",
            data={
                "user": UserSerializer(result["user"]).data,
                "access_token": result["access"],
                "refresh_token": result["refresh"]
            }
        )

# =========================================================
# Email Verification
# =========================================================
class VerifyEmailView(BaseAPIView):
    """
    Verify user's email using verification token.
    """

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthService.verify_email(
            serializer.validated_data["token"]
        )

        return self.success_response(
            message="Email verified successfully",
            data=UserSerializer(user).data
        )


# =========================================================
# Logout
# =========================================================
class LogoutView(BaseAPIView):
    """
    Logout the authenticated user.

    Note:
    JWT is stateless, so logout usually requires
    refresh token blacklisting.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        return self.success_response(
            message="Logged out successfully"
        )


# =========================================================
# Forgot Password
# =========================================================
class ForgotPasswordView(BaseAPIView):
    """
    Initiate password reset process.
    """

    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    def post(self, request):

        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        AuthService.forgot_password(
            serializer.validated_data["email"]
        )

        return self.success_response(
            message="Password reset email sent"
        )


# =========================================================
# Reset Password
# =========================================================
class ResetPasswordView(BaseAPIView):
    """
    Reset password using reset token.
    """

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        AuthService.reset_password(**serializer.validated_data)

        return self.success_response(
            message="Password reset successful"
        )


# =========================================================
# Change Password
# =========================================================
class ChangePasswordView(BaseAPIView):
    """
    Change password for authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        AuthService.change_password(
            request.user,
            **serializer.validated_data
        )

        return self.success_response(
            message="Password changed successfully"
        )


# =========================================================
# Goggle Login
# =========================================================
class GoogleLoginView(BaseAPIView):
    """
    Authenticate user via Google OAuth
    """

    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    def post(self, request):

        serializer = GoogleLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = AuthService.google_login(
            serializer.validated_data["token"]
        )

        return self.success_response(
            message="Google login successful",
            data={
                "user": UserSerializer(result["user"]).data,
                "access_token": result["access"],
                "refresh_token": result["refresh"]
            }
        )
        