# =========================================================
# Django REST Framework
# =========================================================
from rest_framework import generics, permissions

# =========================================================
# Serializers
# =========================================================
from accounts.serializers import (
    UserSessionSerializer,
    DeleteSessionSerializer,
    LogoutAllSessionsSerializer,
    LogoutCurrentSessionSerializer
)

# =========================================================
# Services
# =========================================================
from accounts.services.session_service import SessionService

# =========================================================
# Core
# =========================================================
from core.api import BaseAPIView


# =========================================================
# LIST USER SESSIONS
# =========================================================
class UserSessionListView(generics.ListAPIView):
    serializer_class = UserSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SessionService.get_user_sessions(self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}

# =========================================================
# DELETE SINGLE SESSION
# =========================================================
class UserSessionDeleteView(BaseAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeleteSessionSerializer
    
    def delete(self, request, id):
        try:
            SessionService.delete_session(
                user=request.user,
                session_id=id,
                current_session_id=getattr(request, "session_id", None)
            )
        except Exception as e:
            return self.error_response(message=str(e))

        return self.success_response(message="Session logged out successfully")


# =========================================================
# LOGOUT ALL OTHER DEVICES
# =========================================================
class LogoutAllSessionsView(BaseAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutAllSessionsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            SessionService.logout_all_sessions(
                user=request.user,
                current_session_id=getattr(request, "session_id", None)
            )
        except Exception as e:
            return self.error_response(message=str(e))

        return self.success_response(
            message="Logged out from all other devices"
        )
        
# =========================================================
# LOGOUT CURRENT SESSION
# =========================================================
class LogoutCurrentSessionView(BaseAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutCurrentSessionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            SessionService.logout_current_session(
                user=request.user,
                current_session_id=getattr(request, "session_id", None)
            )
        except Exception as e:
            return self.error_response(message=str(e))

        return self.success_response(
            message="Logged out from current device"
        )
        