# =========================================================
# Rest Framework
# =========================================================
from rest_framework.exceptions import PermissionDenied, ValidationError

# =========================================================
# Core Services
# =========================================================
from core.services import CloudinaryService

# =========================================================
# ME SERVICE
# =========================================================
class MeService:

    # =====================================================
    # VALIDATE USER
    # =====================================================
    @staticmethod
    def validate_user(user):
        """Ensures the user is valid, active, and not blocked."""
        if not user:
            raise PermissionDenied("User not found")

        if not user.is_active:
            raise PermissionDenied("Account is deactivated")

        if getattr(user, "is_blocked", False):
            raise PermissionDenied("Account is blocked")

        return user

    # =====================================================
    # DELETE ACCOUNT
    # =====================================================
    @staticmethod
    def delete_account(user):
        """Soft deletes the user account."""
        user = MeService.validate_user(user)

        if hasattr(user, "soft_delete"):
            user.soft_delete()
        else:
            user.is_active = False
            user.save(update_fields=["is_active"])

        return True

    # =====================================================
    # UPDATE AVATAR
    # =====================================================
    @staticmethod
    def update_avatar(user, file):
        """Uploads and updates user avatar."""
        user = MeService.validate_user(user)

        if not file:
            raise ValidationError("Avatar file is required")

        try:
            upload_result = CloudinaryService.upload_image(
                file=file,
                folder="avatars"
            )

            avatar_url = upload_result.get("url")

            if not avatar_url:
                raise ValidationError("Avatar upload failed")

            user.avatar = avatar_url
            user.save(update_fields=["avatar"])

            return avatar_url

        except Exception:
            raise ValidationError("Error uploading avatar")
        