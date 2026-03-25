# =========================================================
# Rest Framework
# =========================================================
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveUpdateDestroyAPIView

# =========================================================
# Django
# =========================================================
from django.contrib.auth import logout

# =========================================================
# Serializers
# =========================================================
from accounts.serializers import (
    UserSerializer,
    UpdateAvatarSerializer
)

# =========================================================
# Services
# =========================================================
from accounts.services import MeService

# =========================================================
# Core
# =========================================================
from core.api import BaseAPIView

# =========================================================
# User Profile (Me)
# =========================================================
class MeView(BaseAPIView, RetrieveUpdateDestroyAPIView):
    """API endpoint for authenticated user's profile:"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # =========================
    # Get validated current user
    # =========================
    def get_object(self):
        return MeService.validate_user(self.request.user)

    # =========================
    # Retrieve profile
    # =========================
    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request, *args, **kwargs)

        return self.success_response(
            message="User profile fetched successfully",
            data=res.data
        )

    # =========================
    # Partial update (PATCH)
    # =========================
    def partial_update(self, request, *args, **kwargs):
        res = super().partial_update(request, *args, **kwargs)

        return self.success_response(
            message="Profile updated successfully",
            data=res.data
        )

    # =========================
    # Full update (PUT)
    # =========================
    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)

        return self.success_response(
            message="Profile updated successfully",
            data=res.data
        )

    # =========================
    # Delete account
    # =========================
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        # Delete account via service
        MeService.delete_account(user)

        # Logout user
        logout(request)

        return self.success_response(
            message="Account deleted successfully",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )


# =========================================================
# Avatar Management
# =========================================================
class UpdateAvatarView(BaseAPIView, generics.GenericAPIView):
    """API endpoint to update user avatar"""
    serializer_class = UpdateAvatarSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    # =========================
    # Update avatar
    # =========================
    def patch(self, request, *args, **kwargs):
        # Step 1: Validate input
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Step 2: Update avatar via service
        avatar_url = MeService.update_avatar(
            user=request.user,
            file=serializer.validated_data["avatar"]
        )

        # Step 3: Return response
        return self.success_response(
            message="Avatar updated successfully",
            data={
                "avatar": avatar_url
            },
            status_code=status.HTTP_200_OK
        )