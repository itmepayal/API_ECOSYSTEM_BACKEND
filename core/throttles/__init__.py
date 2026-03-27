# =========================================================
# AUTH THROTTLES
# =========================================================
from .auth_throttle import (
    AuthThrottle,
    LoginThrottle,
    RegisterThrottle,
    ResendVerificationThrottle,
    ForgotPasswordThrottle,
    TwoFactorThrottle,
)

__all__ = [
    "AuthThrottle",
    "LoginThrottle",
    "RegisterThrottle",
    "ResendVerificationThrottle",
    "ForgotPasswordThrottle",
    "TwoFactorThrottle",
]