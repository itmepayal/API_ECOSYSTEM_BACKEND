from rest_framework.exceptions import NotFound

from accounts.selectors.session_selector import (
    get_active_sessions,
    get_active_session_by_id
)

class AdminSessionService:
    @staticmethod
    def list_active_sessions():
        return get_active_sessions()

    @staticmethod
    def deactivate_session(session_id):
        session = get_active_session_by_id(session_id)

        if not session:
            raise NotFound("Active session not found.")

        session.soft_delete()

        return session