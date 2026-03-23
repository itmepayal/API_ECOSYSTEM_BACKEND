from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

# Auth Views
from accounts.views.auth_views import (
    RegisterView,
    LoginView,
    VerifyEmailView,
    ForgotPasswordView,
    ResetPasswordView,
    ChangePasswordView,
    LogoutView,
    GoogleLoginView
)

# 2FA Views
from accounts.views.two_factor_view import (
    TwoFactorSetupView,
    TwoFactorVerifySetupView,
    TwoFactorLoginVerifyView,
    TwoFactorDisableView
)

# API Key Views
from accounts.views.apikey_views import (
    APIKeyListCreateView,
    APIKeyDetailView
)


urlpatterns = [
    # =========================================================
    # AUTH
    # =========================================================
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("verify-email/", VerifyEmailView.as_view(), name="verify_email"),

    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),

    path("refresh-token/", TokenRefreshView.as_view(), name="refresh_token"),
    path("google/", GoogleLoginView.as_view(), name="google_login"),

    # =========================================================
    # TWO FACTOR AUTH (2FA)
    # =========================================================
    path("2fa/setup/", TwoFactorSetupView.as_view(), name="2fa_setup"),
    path("2fa/verify-setup/", TwoFactorVerifySetupView.as_view(), name="2fa_verify_setup"),
    path("2fa/login-verify/", TwoFactorLoginVerifyView.as_view(), name="2fa_login_verify"),
    path("2fa/disable/", TwoFactorDisableView.as_view(), name="2fa_disable"),

    # =========================================================
    # API KEYS
    # =========================================================
    path("api-keys/", APIKeyListCreateView.as_view(), name="api_keys"),
    path("api-keys/<uuid:pk>/", APIKeyDetailView.as_view(), name="api_key_detail"),
]
