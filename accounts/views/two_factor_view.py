from rest_framework.permissions import IsAuthenticated, AllowAny

from core.api.base_view import BaseAPIView
from core.throttles.auth_throttle import AuthThrottle

from accounts.services.two_factor_service import TwoFactorService
from accounts.services.auth_service import AuthService


# =========================================================
# 2FA SETUP
# =========================================================
class TwoFactorSetupView(BaseAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthThrottle]

    def post(self, request):

        data = TwoFactorService.setup_2fa(request.user)

        return self.success_response(
            message="2FA setup initiated",
            data=data
        )


# =========================================================
# VERIFY SETUP
# =========================================================
class TwoFactorVerifySetupView(BaseAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthThrottle]

    def post(self, request):

        code = request.data.get("code")

        TwoFactorService.verify_setup(request.user, code)

        return self.success_response(
            message="2FA enabled successfully"
        )


# =========================================================
# VERIFY LOGIN 2FA
# =========================================================
class TwoFactorLoginVerifyView(BaseAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    def post(self, request):

        user_id = request.data.get("user_id")
        code = request.data.get("code")

        if not user_id or not code:
            return self.error_response("user_id and code are required")

        user = TwoFactorService.verify_login_2fa(user_id, code)

        tokens = AuthService.generate_tokens(user)

        return self.success_response(
            message="Login successful",
            data={
                "user": user.id,
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"]
            }
        )


# =========================================================
# DISABLE 2FA
# =========================================================
class TwoFactorDisableView(BaseAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthThrottle]

    def post(self, request):

        code = request.data.get("code")

        TwoFactorService.disable_2fa(request.user, code)

        return self.success_response(
            message="2FA disabled successfully"
        )
        