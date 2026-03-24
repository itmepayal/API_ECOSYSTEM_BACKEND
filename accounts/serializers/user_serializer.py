from rest_framework import serializers
from accounts.models.user import User
from core.utils.validators import validate_image
from core.services.cloudinary_service import CloudinaryService
import uuid

# =========================================================
# User Serializer
# =========================================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "avatar",
            "role",
            "is_verified",
            "created_at",
        )
        read_only_fields = fields

# =====================================================
# Update Avatar
# =====================================================
class UpdateAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ["avatar"]
