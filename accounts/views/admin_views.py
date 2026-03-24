from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import User, APIKey
from accounts.serializers import UserSerializer, APIKeySerializer
from core.permission import IsAdminUser

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    # Block a user
    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        user = self.get_object()
        user.is_blocked = True
        user.save(update_fields=["is_blocked"])
        return Response({"status": "user blocked"})

    # Unblock a user
    @action(detail=True, methods=['post'])
    def unblock(self, request, pk=None):
        user = self.get_object()
        user.is_blocked = False
        user.save(update_fields=["is_blocked"])
        return Response({"status": "user unblocked"})

    # List a user's API keys
    @action(detail=True, methods=['get'])
    def api_keys(self, request, pk=None):
        user = self.get_object()
        keys = APIKey.objects.filter(user=user)
        serializer = APIKeySerializer(keys, many=True)
        return Response(serializer.data)

class AdminAPIKeyDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            key = APIKey.objects.get(id=pk)
            key.delete()
            return Response({"status": "API key deleted"}, status=status.HTTP_204_NO_CONTENT)
        except APIKey.DoesNotExist:
            return Response({"error": "API key not found"}, status=status.HTTP_404_NOT_FOUND)
        
class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        total_api_keys = APIKey.objects.count()
        return Response({
            "total_users": total_users,
            "active_users": active_users,
            "total_api_keys": total_api_keys,
        })