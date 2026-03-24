from rest_framework import generics, permissions, status
from rest_framework.response import Response
from accounts.models.session import UserSession
from accounts.serializers.session_serializer import UserSessionSerializer

# ----------------------------
# Users manage their sessions
# ----------------------------
class UserSessionView(generics.ListAPIView):
    serializer_class = UserSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSession.objects.filter(user=self.request.user, is_active=True)


class UserSessionDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return UserSession.objects.filter(user=self.request.user, is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()