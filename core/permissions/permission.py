from rest_framework.permissions import BasePermission
from core.constants import ROLE_ADMIN  

class IsAdminUserCustom(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and not user.is_blocked
            and (
                (user.is_staff and user.is_superuser)  
                or user.role == ROLE_ADMIN    
            )
        )