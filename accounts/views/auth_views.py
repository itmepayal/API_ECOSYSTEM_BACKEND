from rest_framework.permissions import AllowAny
from rest_framework import status

from core.api.base_view import BaseAPIView
from core.throttles.auth_throttle import AuthThrottle

from accounts.serializers.auth_serializer import RegisterSerializer
from accounts.services.auth_service import AuthService

class RegisterView(BaseAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthService.register_user(**serializer.validated_data)

        return self.success_response(
            message="User registered successfully. Please verify your email.",
            data={
                "email": user.email,
                "username": user.username
            },
            status_code=status.HTTP_201_CREATED
        )