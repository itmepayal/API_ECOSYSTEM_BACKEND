from django.urls import path

from accounts.views import (
    RegisterView,
    LoginView,
    VerifyEmailView,
    ForgotPasswordView,
    ResetPasswordView,
    ChangePasswordView,
    LogoutView,
    RefreshTokenView,
    GoogleLoginView,
    ResendVerificationView,
    TwoFactorSetupView,
    TwoFactorVerifySetupView,
    TwoFactorLoginVerifyView,
    TwoFactorDisableView
)

urlpatterns = [
    # =========================
    # AUTH
    # =========================
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("resend-verification/", ResendVerificationView.as_view(), name="resend-verification"),

    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),

    path("refresh-token/", RefreshTokenView.as_view(), name="refresh-token"),
    path("google/", GoogleLoginView.as_view(), name="google-login"),

    # =========================
    # TWO FACTOR AUTH (2FA)
    # =========================
    path("2fa/setup/", TwoFactorSetupView.as_view(), name="2fa-setup"),
    path("2fa/verify-setup/", TwoFactorVerifySetupView.as_view(), name="2fa-verify-setup"),
    path("2fa/login-verify/", TwoFactorLoginVerifyView.as_view(), name="2fa-login-verify"),
    path("2fa/disable/", TwoFactorDisableView.as_view(), name="2fa-disable"),
]
