import hashlib
from django.utils import timezone
from accounts.models import UserSession

def create_user_session(request, user):
    raw_token, token_hash = UserSession.generate_session_token()

    session = UserSession.objects.create(
        user=user,
        token_hash=token_hash,
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        expires_at=timezone.now() 
    )

    session.set_expiry(days=7)
    session.save(update_fields=["expires_at"])

    return raw_token, session

def validate_session(request):
    raw_token = request.headers.get("X-Session-Token")

    if not raw_token:
        return None

    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    return UserSession.objects.filter(
        token_hash=token_hash,
        expires_at__gt=timezone.now()
    ).first()


def logout_user_session(request):
    """
    Logout current session using X-Session-Token
    """
    raw_token = request.headers.get("X-Session-Token")

    if not raw_token:
        return False

    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    deleted, _ = UserSession.objects.filter(
        user=request.user,
        token_hash=token_hash
    ).soft_delete()

    return deleted > 0
    
