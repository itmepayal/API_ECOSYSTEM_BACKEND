# =========================================================
# Django REST Framework
# =========================================================
from rest_framework import serializers

# =========================================================
# Accounts Models
# =========================================================
from accounts.models import User

# =========================================================
# Core Utilities
# =========================================================
from core.utils import validate_image
from core.services import CloudinaryService

# =========================================================
# USER SERIALIZER
# =========================================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "avatar",
            "role",
            "is_verified",
            "created_at"
        ]
        read_only_fields = [
            "id",
            "email",
            "role",
            "is_verified",
            "created_at"
        ]


# =========================================================
# UPDATE AVATAR SERIALIZER
# =========================================================
class UpdateAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ["avatar"]

    # -------------------------
    # Validate Avatar
    # -------------------------
    def validate_avatar(self, value):
        validate_image(value)
        return value
    