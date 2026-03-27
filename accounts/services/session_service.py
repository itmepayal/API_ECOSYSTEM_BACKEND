# =========================================================
# Django
# =========================================================
from django.utils import timezone

# =========================================================
# Rest Framework
# =========================================================
from rest_framework.exceptions import ValidationError

# =========================================================
# Accounts Models
# =========================================================
from accounts.models import UserSession

# =========================================================
# SESSION SERVICE
# =========================================================
class SessionService:

    # =====================================================
    # GET USER ACTIVE SESSIONS
    # =====================================================
    @staticmethod
    def get_user_sessions(user):
        return UserSession.objects.filter(
            user=user,
            is_active=True
        ).order_by("-created_at")

    # =====================================================
    # DELETE SINGLE SESSION
    # =====================================================
    @staticmethod
    def delete_session(user, session_id, current_session_id):
        session = UserSession.objects.filter(
            id=session_id,
            user=user,
            is_active=True
        ).first()

        if not session:
            raise ValidationError("Session not found")

        # Prevent deleting current session
        if str(session.id) == str(current_session_id):
            raise ValidationError("You cannot delete your current session")

        session.is_active = False
        session.last_activity = timezone.now()
        session.save(update_fields=["is_active", "last_activity"])

        return True

    # =====================================================
    # LOGOUT ALL OTHER SESSIONS
    # =====================================================
    @staticmethod
    def logout_all_sessions(user, current_session_id):
        if not current_session_id:
            raise ValidationError("Invalid session context")

        UserSession.objects.filter(
            user=user,
            is_active=True
        ).exclude(
            id=current_session_id
        ).update(
            is_active=False,
            last_activity=timezone.now()
        )

        return True

    # =====================================================
    # LOGOUT CURRENT SESSION
    # =====================================================
    @staticmethod
    def logout_current_session(user, current_session_id):
        if not current_session_id:
            raise ValidationError("Session not found")

        session = UserSession.objects.filter(
            id=current_session_id,
            user=user,
            is_active=True
        ).first()

        if not session:
            raise ValidationError("Session not found")

        session.is_active = False
        session.last_activity = timezone.now()
        session.save(update_fields=["is_active", "last_activity"])

        return True

    # =====================================================
    # CLEANUP EXPIRED SESSIONS (CRON / CELERY)
    # =====================================================
    @staticmethod
    def cleanup_expired_sessions():
        expired_sessions = UserSession.objects.filter(
            expires_at__lt=timezone.now(),
            is_active=True
        )

        expired_sessions.update(
            is_active=False,
            last_activity=timezone.now()
        )

        return expired_sessions.count()
    