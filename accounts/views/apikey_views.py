from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from core.api.base_view import BaseAPIView
from accounts.models import APIKey
from accounts.serializers.apikey_serializer import APIKeySerializer

class APIKeyListCreateView(BaseAPIView, ListCreateAPIView):
    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["usage_limit"]
    ordering_fields = ["created_at", "usage_limit"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return APIKey.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)

        if isinstance(res.data, dict):
            data = res.data.get("results", [])
            meta = {
                "count": res.data.get("count"),
                "next": res.data.get("next"),
                "previous": res.data.get("previous"),
            }
        else:
            data = res.data
            meta = None

        return self.success_response(
            message="API Keys fetched successfully",
            data=data,
            meta=meta
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)

        return self.success_response(
            message="API Key created successfully",
            data=res.data,
            status_code=res.status_code
        )
        
class APIKeyDetailView(BaseAPIView, RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, delete API key
    """

    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return APIKey.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request, *args, **kwargs)

        return self.success_response(
            message="API Key fetched successfully",
            data=res.data
        )

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)

        return self.success_response(
            message="API Key updated successfully",
            data=res.data
        )

    def partial_update(self, request, *args, **kwargs):
        res = super().partial_update(request, *args, **kwargs)

        return self.success_response(
            message="API Key partially updated successfully",
            data=res.data
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return self.success_response(
            message="API Key deleted successfully",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )
        