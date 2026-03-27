from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from accounts.serializers import APIKeySerializer
from accounts.services.api_key_service import APIKeyService
from accounts.selectors.api_key_selector import APIKeySelector
from core.api import BaseAPIView


# =========================================================
# LIST + CREATE
# =========================================================
class APIKeyListCreateView(BaseAPIView, ListCreateAPIView):
    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["usage_limit", "is_active"]
    ordering_fields = ["created_at", "usage_limit"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return APIKeySelector.get_api_keys(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance, raw_key = APIKeyService.create_api_key(
            user=request.user,
            validated_data=serializer.validated_data
        )

        return self.success_response(
            message="API Key created successfully",
            data={
                **self.get_serializer(instance).data,
                "api_key": raw_key,  # only shown once
            }
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return self.success_response(
            message="API Keys fetched successfully",
            data=serializer.data,
            meta={"count": queryset.count()},
        )


# =========================================================
# DETAIL / UPDATE / DELETE
# =========================================================
class APIKeyDetailView(BaseAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return APIKeySelector.get_api_keys(self.request.user)

    # ✅ CLEAN UPDATE FLOW
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)

        # Use service layer
        APIKeyService.update_api_key(
            instance=instance,
            validated_data=serializer.validated_data
        )

        # Ensure fresh data
        instance.refresh_from_db()

        return self.success_response(
            message="API Key updated successfully",
            data=self.get_serializer(instance).data,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        APIKeyService.delete_api_key(instance)

        return self.success_response(
            message="API Key deleted successfully"
        )

# =========================================================
# VERIFY API KEY
# =========================================================
class VerifyAPIKeyView(BaseAPIView, APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        raw_key = request.data.get("api_key")

        if not raw_key:
            return self.error_response(
                message="API key is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            api_key = APIKeyService.verify_and_use_key(raw_key)
        except ValidationError as e:
            return self.error_response(
                message="Invalid API key",
                errors=e.detail,
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        return self.success_response(
            message="API key is valid",
            data={
                "user_id": api_key.user.id,
                "email": api_key.user.email,
                "prefix": api_key.prefix,
                "usage_count": api_key.usage_count,
            }
        )
        