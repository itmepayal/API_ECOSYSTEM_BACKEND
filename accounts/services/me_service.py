# =========================================================
# Rest Framework
# =========================================================
from rest_framework.exceptions import PermissionDenied

# =========================================================
# ME SERVICE
# =========================================================
class MeService:
    # =====================================================
    # INTERNAL HELPERS
    # =====================================================
    @staticmethod
    def validate_user(user):
        if not user:
            raise PermissionDenied("User not found")

        if not user.is_active:
            raise PermissionDenied("Account is deactivated")

        if getattr(user, "is_blocked", False):
            raise PermissionDenied("Account is blocked")

        return user

    # =====================================================
    # DELETE ACCOUNT (SOFT DELETE)
    # =====================================================
    @staticmethod
    def delete_account(user):
        user = MeService.validate_user(user)
        user.soft_delete()

        return True
    
    