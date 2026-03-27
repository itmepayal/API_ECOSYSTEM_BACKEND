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
    LogoutSerializer,
    RefreshTokenSerializer,
    VerifyEmailSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    ForgotPasswordSerializer,
    GoogleLoginSerializer,
    ResendVerificationSerializer,
)

# =========================================================
# Services
# =========================================================
from accounts.services import AuthService

# =========================================================
# Utils
# =========================================================
from accounts.utils import logout_user_session, create_user_session

# =========================================================
# Core
# =========================================================
from core.api import BaseAPIView
from core.throttles import (
    AuthThrottle,
    LoginThrottle,
    RegisterThrottle,
    ResendVerificationThrottle,
    ForgotPasswordThrottle,
    TwoFactorThrottle,
)

# =========================================================
# USER REGISTRATION
# =========================================================
class RegisterView(BaseAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [RegisterThrottle]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = AuthService.register_user(**serializer.validated_data)
        except Exception as e:
            return self.error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        return self.success_response(
            message="User registered successfully. Please verify your email.",
            data=UserSerializer(user).data,
            status_code=status.HTTP_201_CREATED
        )


# =========================================================
# USER LOGIN
# =========================================================
class LoginView(BaseAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [LoginThrottle]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = AuthService.login_user(**serializer.validated_data)
            user = result["user"]
        except Exception as e:
            return self.error_response(message=str(e))

        if result["requires_2fa"]:
            return self.success_response(
                message="2FA required",
                data={
                    "requires_2fa": True,
                    "user_id": user.id
                }
            )

        session_token, _ = create_user_session(request, user)

        tokens = AuthService.generate_tokens(user)

        return self.success_response(
            message="Login successful",
            data={
                "user": UserSerializer(user).data,
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"],
                "session_token": session_token
            }
        )

# =========================================================
# VERIFY EMAIL
# =========================================================
class VerifyEmailView(BaseAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = AuthService.verify_email(serializer.validated_data["token"])
        except Exception as e:
            return self.error_response(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)

        return self.success_response(
            message="Email verified successfully",
            data=UserSerializer(user).data
        )

# =========================================================
# RESEND EMAIL VERIFICATION
# =========================================================
class ResendVerificationView(BaseAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [ResendVerificationThrottle]
    serializer_class = ResendVerificationSerializer

    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            AuthService.resend_verification(email)
        except Exception as e:
            return self.error_response(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)

        return self.success_response(
            message="If your email exists, a verification link has been sent",
            data={"email": email}
        )

# =========================================================
# LOGOUT
# =========================================================
class LogoutView(BaseAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthThrottle]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.validated_data["token"].blacklist()
            logout_user_session(request)

        except Exception as e:
            return self.error_response(message=str(e))

        return self.success_response(message="Logged out successfully")
    
# =========================================================
# FORGOT PASSWORD
# =========================================================
class ForgotPasswordView(BaseAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [ForgotPasswordThrottle]
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            AuthService.forgot_password(email)
        except Exception as e:
            return self.error_response(message=str(e))

        return self.success_response(
            message="Password reset email sent",
            data={"email": email}
        )


# =========================================================
# RESET PASSWORD
# =========================================================
class ResetPasswordView(BaseAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            AuthService.reset_password(**serializer.validated_data)
        except Exception as e:
            return self.error_response(message=str(e))

        return self.success_response(message="Password reset successful")


# =========================================================
# CHANGE PASSWORD
# =========================================================
class ChangePasswordView(BaseAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthThrottle]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            AuthService.change_password(request.user, **serializer.validated_data)
        except Exception as e:
            return self.error_response(message=str(e))

        return self.success_response(message="Password changed successfully")


# =========================================================
# GOOGLE LOGIN
# =========================================================
class GoogleLoginView(BaseAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]
    serializer_class = GoogleLoginSerializer

    def post(self, request):
        serializer = GoogleLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = AuthService.google_login(serializer.validated_data["token"])
            user = result["user"]
        except Exception as e:
            return self.error_response(message=str(e))

        session_token, _ = create_user_session(request, user)

        tokens = AuthService.generate_tokens(user)

        return self.success_response(
            message="Google login successful",
            data={
                "user": UserSerializer(user).data,
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"],
                "session_token": session_token
            }
        )

# =========================================================
# REFRESH TOKEN
# =========================================================
class RefreshTokenView(BaseAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            tokens = AuthService.refresh_tokens(
                serializer.validated_data["token"]
            )
        except Exception as e:
            return self.error_response(message=str(e))

        return self.success_response(
            message="Token refreshed successfully",
            data={
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"]
            }
        )