# =========================================================
# Rest Framework
# =========================================================
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
)

# =========================================================
# Third Party
# =========================================================
from django_filters.rest_framework import DjangoFilterBackend

# =========================================================
# Models
# =========================================================
from accounts.models import APIKey

# =========================================================
# Serializers
# =========================================================
from accounts.serializers import APIKeySerializer

# =========================================================
# Core
# =========================================================
from core.api import BaseAPIView
from core.permissions import IsAdminUserCustom

# =========================================================
# USER: LIST & CREATE
# =========================================================
class APIKeyListCreateView(ListCreateAPIView, BaseAPIView):
    """
    USER:
    - List own API keys
    - Create API key
    """

    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = ["usage_limit"]
    ordering_fields = ["created_at", "usage_limit"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return APIKey.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        data, meta = self._format_response(res)

        return self.success_response(
            message="Your API Keys fetched successfully",
            data=data,
            meta=meta,
        )

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)

        return self.success_response(
            message="API Key created successfully",
            data=res.data,
            status_code=res.status_code,
        )

    def _format_response(self, res):
        if isinstance(res.data, dict):
            return (
                res.data.get("results", []),
                {
                    "count": res.data.get("count"),
                    "next": res.data.get("next"),
                    "previous": res.data.get("previous"),
                },
            )
        return res.data, None


# =========================================================
# USER: RETRIEVE / UPDATE / DELETE
# =========================================================
class APIKeyDetailView(RetrieveUpdateDestroyAPIView, BaseAPIView):
    """
    USER:
    - Retrieve own API key
    - Update
    - Delete
    """

    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return APIKey.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request, *args, **kwargs)

        return self.success_response(
            message="API Key fetched successfully",
            data=res.data,
        )

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)

        return self.success_response(
            message="API Key updated successfully",
            data=res.data,
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return self.success_response(
            message="API Key deleted successfully"
        )


# =========================================================
# ADMIN: LIST ALL KEYS
# =========================================================
class AdminAPIKeyListView(ListAPIView, BaseAPIView):
    """
    ADMIN:
    - View all API keys
    """

    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["usage_limit", "user"]
    search_fields = ["user__email"]  # ❗ secure
    ordering_fields = ["created_at", "usage_limit"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return APIKey.objects.select_related("user").all()

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        data, meta = self._format_response(res)

        return self.success_response(
            message="All API Keys fetched (Admin)",
            data=data,
            meta=meta,
        )

    def _format_response(self, res):
        if isinstance(res.data, dict):
            return (
                res.data.get("results", []),
                {
                    "count": res.data.get("count"),
                    "next": res.data.get("next"),
                    "previous": res.data.get("previous"),
                },
            )
        return res.data, None


# =========================================================
# ADMIN: UPDATE KEY
# =========================================================
class AdminAPIKeyUpdateView(RetrieveUpdateAPIView, BaseAPIView):
    """
    ADMIN:
    - Update API key
    - Revoke key
    """

    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]
    queryset = APIKey.objects.all()
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)

        return self.success_response(
            message="API Key updated successfully",
            data=res.data,
        )


# =========================================================
# ADMIN: DELETE KEY
# =========================================================
class AdminAPIKeyDeleteView(DestroyAPIView, BaseAPIView):
    """
    ADMIN:
    - Delete any API key
    """

    permission_classes = [IsAuthenticated, IsAdminUserCustom]
    queryset = APIKey.objects.all()
    lookup_field = "id"

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return self.success_response(
            message="API Key deleted successfully"
        )