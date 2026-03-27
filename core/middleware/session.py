import hashlib
from django.utils import timezone
from accounts.models import UserSession

class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session_id = None

        token = request.headers.get("X-Session-Token")

        if token:
            token_hash = hashlib.sha256(token.encode()).hexdigest()

            session = UserSession.objects.filter(
                token_hash=token_hash,
                is_active=True
            ).first()

            if session and session.expires_at < timezone.now():
                session.is_active = False
                session.save(update_fields=["is_active"])
                session = None

            if session:
                request.session_id = session.id

                session.last_activity = timezone.now()
                session.save(update_fields=["last_activity"])

        return self.get_response(request)
    