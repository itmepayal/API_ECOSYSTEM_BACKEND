from accounts.models.session import UserSession

def get_active_sessions():
    return UserSession.objects.filter(is_active=True)

def get_active_session_by_id(session_id):
    try:
        return UserSession.objects.get(id=session_id, is_active=True)
    except UserSession.DoesNotExist:
        return None