from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.contrib.auth import logout

from core.api.base_view import BaseAPIView
from accounts.serializers.user_serializer import UserSerializer, UpdateAvatarSerializer
from accounts.services.me_service import MeService
from core.services import cloudinary_service

class MeView(BaseAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # =========================
    # Always return validated user
    # =========================
    def get_object(self):
        user = self.request.user
        return MeService.validate_user(user)

    # =========================
    # GET → Get current user
    # =========================
    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request, *args, **kwargs)

        return self.success_response(
            message="User profile fetched successfully",
            data=res.data
        )

    # =========================
    # PATCH → Update profile
    # =========================
    def partial_update(self, request, *args, **kwargs):
        res = super().partial_update(request, *args, **kwargs)

        return self.success_response(
            message="Profile updated successfully",
            data=res.data
        )

    # =========================
    # PUT → Full update
    # =========================
    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)

        return self.success_response(
            message="Profile fully updated successfully",
            data=res.data
        )

    # =========================
    # DELETE → Soft delete account
    # =========================
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        MeService.delete_account(user)

        logout(request)

        return self.success_response(
            message="Account deleted successfully",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )
        
class UpdateAvatarView(generics.GenericAPIView):
    serializer_class = UpdateAvatarSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["avatar"]
        user = request.user

        try:
            avatar_data = CloudinaryService.upload_image(file, folder="avatars")
            avatar_url = avatar_data["url"]

            user.avatar = avatar_url
            user.save(update_fields=["avatar"])

            return Response({
                "success": True,
                "message": "Avatar updated successfully",
                "data": {"avatar": avatar_url}
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Error uploading avatar"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            