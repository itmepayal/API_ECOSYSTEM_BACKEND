# =========================================================
# AUTH VIEWS
# =========================================================
from .auth_views import (
    RegisterView,
    LoginView,
    LogoutView,
    VerifyEmailView,
    RefreshTokenView,
    ForgotPasswordView,
    ResetPasswordView,
    ChangePasswordView,
    GoogleLoginView,
)

# =========================================================
# USER (ME)
# =========================================================
from .user_views import (
    MeView,
    UpdateAvatarView,
)

# =========================================================
# API KEY VIEWS
# =========================================================
from .api_key_views import (
    APIKeyListCreateView,
    APIKeyDetailView,
    AdminAPIKeyListView,
    AdminAPIKeyUpdateView,
    AdminAPIKeyDeleteView,
)

# =========================================================
# SESSION VIEWS (USER)
# =========================================================
from .session_views import (
    UserSessionListView,
    UserSessionDeleteView,
    LogoutAllSessionsView,
    LogoutCurrentSessionView,
)

# =========================================================
# TWO FACTOR AUTH
# =========================================================
from .two_factor_views import (
    TwoFactorLoginVerifyView,
    TwoFactorSetupView,
    TwoFactorVerifySetupView,
    TwoFactorDisableView
)
