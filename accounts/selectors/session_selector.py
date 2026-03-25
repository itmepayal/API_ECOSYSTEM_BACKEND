# =========================================================
# Django
# =========================================================
from django.utils import timezone

# =========================================================
# Accounts Models
# =========================================================
from accounts.models import UserSession

# =========================================================
# GET ACTIVE SESSIONS
# =========================================================
def get_active_sessions(user=None):
    qs = UserSession.objects.filter(expires_at__gt=timezone.now())
    return qs.filter(user=user) if user else qs

# =========================================================
# GET ACTIVE SESSION BY ID
# =========================================================
def get_active_session_by_id(session_id, user=None):
    qs = UserSession.objects.filter(
        id=session_id,
        expires_at__gt=timezone.now()
    )
    return qs.filter(user=user).first() if user else qs.first()
