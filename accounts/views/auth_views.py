# =========================================================
# Rest Framework
# =========================================================
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

# =========================================================
# Serializers
# =========================================================
from accounts.serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    VerifyEmailSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    ForgotPasswordSerializer,
    GoogleLoginSerializer
)

# =========================================================
# Services
# =========================================================
from accounts.services import AuthService

# =========================================================
# Core
# =========================================================
from core.api import BaseAPIView
from core.throttles import AuthThrottle

# =========================================================
# User Registration
# =========================================================
class RegisterView(BaseAPIView):
    """API endpoint for user registration."""
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    def post(self, request):
        # Step 1: Validate input data
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Step 2: Create user via service layer
        user = AuthService.register_user(**serializer.validated_data)

        # Step 3: Return success response
        return self.success_response(
            message="User registered successfully. Please verify your email.",
            data=UserSerializer(user).data,
            status_code=status.HTTP_201_CREATED
        )


# =========================================================
# User Login
# =========================================================
class LoginView(BaseAPIView):
    """API endpoint for user login."""
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    def post(self, request):
        # Step 1: Validate input data
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Step 2: Authenticate user via service
        result = AuthService.login_user(**serializer.validated_data)
        user = result["user"]
        
        # Step 3: Handle 2FA requirement
        if result["requires_2fa"]:
            return self.success_response(
                message="2FA required",
                data={
                    "requires_2fa": True,
                    "user_id": user.id
                }
            )
        
        # Step 4: Generate JWT tokens
        tokens = AuthService.generate_tokens(user)

        # Step 5: Return success response
        return self.success_response(
            message="Login successful",
            data={
                "user": UserSerializer(user).data,
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"]
            }
        )


# =========================================================
# Email Verification
# =========================================================
class VerifyEmailView(BaseAPIView):
    """API endpoint to verify user's email."""
    permission_classes = [AllowAny]

    def post(self, request):
        # Step 1: Validate input data
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Step 2: Verify email via service
        user = AuthService.verify_email(
            serializer.validated_data["token"]
        )

        # Step 3: Return success response
        return self.success_response(
            message="Email verified successfully",
            data=UserSerializer(user).data
        )


# =========================================================
# Logout
# =========================================================
class LogoutView(BaseAPIView):
    """API endpoint for user logout."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Step 1: Return success response
        return self.success_response(
            message="Logged out successfully"
        )


# =========================================================
# Forgot Password
# =========================================================
class ForgotPasswordView(BaseAPIView):
    """API endpoint to initiate password reset."""
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    def post(self, request):
        # Step 1: Validate input data
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Step 2: Trigger reset email
        AuthService.forgot_password(
            serializer.validated_data["email"]
        )

        # Step 3: Return success response
        return self.success_response(
            message="Password reset email sent"
        )


# =========================================================
# Reset Password
# =========================================================
class ResetPasswordView(BaseAPIView):
    """API endpoint to reset password."""
    permission_classes = [AllowAny]

    def post(self, request):
        # Step 1: Validate input data
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Step 2: Reset password via service
        AuthService.reset_password(**serializer.validated_data)
        
        # Step 3: Return success response
        return self.success_response(
            message="Password reset successful"
        )


# =========================================================
# Change Password
# =========================================================
class ChangePasswordView(BaseAPIView):
    """API endpoint to change password."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Step 1: Validate input data
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Step 2: Change password via service
        AuthService.change_password(
            request.user,
            **serializer.validated_data
        )

        # Step 3: Return success response
        return self.success_response(
            message="Password changed successfully"
        )


# =========================================================
# Google Login
# =========================================================
class GoogleLoginView(BaseAPIView):
    """API endpoint for Google OAuth login."""
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    def post(self, request):
        # Step 1: Validate input data
        serializer = GoogleLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Step 2: Authenticate via Google service
        result = AuthService.google_login(
            serializer.validated_data["token"]
        )

        # Step 3: Return success response
        return self.success_response(
            message="Google login successful",
            data={
                "user": UserSerializer(result["user"]).data,
                "access_token": result["access"],
                "refresh_token": result["refresh"]
            }
        )