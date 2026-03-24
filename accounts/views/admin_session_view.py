from rest_framework.permissions import IsAdminUser
from rest_framework import status

from core.api.base_view import BaseAPIView

from accounts.serializers import UserSessionSerializer
from accounts.services import AdminSessionService

# =========================================================
# Admin: List All Active Sessions
# =========================================================
class AdminSessionView(BaseAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Fetch sessions via service layer
        sessions = AdminSessionService.list_active_sessions()

        # Serialize response data
        serializer = UserSessionSerializer(sessions, many=True)

        # Return standardized success response
        return self.success_response(
            message="Sessions fetched successfully",
            data=serializer.data
        )


# =========================================================
# Admin: Deactivate User Session
# =========================================================
class AdminSessionDestroyView(BaseAPIView):
    """
    API endpoint to deactivate (soft delete) a user session (Admin only).

    Responsibilities:
    - Deactivate a specific session
    - Prevent further usage of that session

    Access Control:
    - Only accessible by admin users

    Behavior:
    - Performs soft delete (is_active = False)
    - Does NOT permanently remove the record

    Use Cases:
    - Force logout user from device
    - Handle compromised accounts
    - Admin security actions
    """

    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        """
        Handle DELETE request to deactivate a session.

        Args:
            id (UUID): Session ID to deactivate
        """

        # Call service layer to deactivate session
        AdminSessionService.deactivate_session(id)

        # Return standardized response
        return self.success_response(
            message="Session deactivated successfully",
            status_code=status.HTTP_204_NO_CONTENT
        )