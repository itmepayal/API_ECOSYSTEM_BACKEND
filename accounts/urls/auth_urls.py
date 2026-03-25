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
    GoogleLoginView
)

from accounts.views import (
    TwoFactorSetupView,
    TwoFactorVerifySetupView,
    TwoFactorLoginVerifyView,
    TwoFactorDisableView
)

urlpatterns = [
    # Auth
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("verify-email/", VerifyEmailView.as_view()),
    path("forgot-password/", ForgotPasswordView.as_view()),
    path("reset-password/", ResetPasswordView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("refresh-token/", RefreshTokenView.as_view()),
    path("google/", GoogleLoginView.as_view()),

    # 2FA
    path("2fa/setup/", TwoFactorSetupView.as_view()),
    path("2fa/verify-setup/", TwoFactorVerifySetupView.as_view()),
    path("2fa/login-verify/", TwoFactorLoginVerifyView.as_view()),
    path("2fa/disable/", TwoFactorDisableView.as_view()),
]
