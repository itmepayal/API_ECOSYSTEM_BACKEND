from rest_framework.throttling import ScopedRateThrottle

# =========================================================
# BASE AUTH THROTTLE
# =========================================================
class AuthThrottle(ScopedRateThrottle):
    scope = "auth"

# =========================================================
# LOGIN THROTTLE (STRICT)
# =========================================================
class LoginThrottle(ScopedRateThrottle):
    scope = "login"

# =========================================================
# REGISTER THROTTLE
# =========================================================
class RegisterThrottle(ScopedRateThrottle):
    scope = "register"

# =========================================================
# RESEND VERIFICATION (ANTI-SPAM)
# =========================================================
class ResendVerificationThrottle(ScopedRateThrottle):
    scope = "resend"

# =========================================================
# FORGOT PASSWORD (ANTI-ABUSE)
# =========================================================
class ForgotPasswordThrottle(ScopedRateThrottle):
    scope = "forgot_password"

# =========================================================
# TWO FACTOR AUTH (CRITICAL SECURITY)
# =========================================================
class TwoFactorThrottle(ScopedRateThrottle):
    scope = "two_factor"
    