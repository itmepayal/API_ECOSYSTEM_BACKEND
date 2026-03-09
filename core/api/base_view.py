from rest_framework.views import APIView
from rest_framework import status
from core.responses.api_response import api_response


class BaseAPIView(APIView):

    def success_response(self, message="Success", data=None, status_code=status.HTTP_200_OK):
        return api_response(
            success=True,
            message=message,
            data=data,
            status_code=status_code
        )

    def error_response(self, message="Error", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        return api_response(
            success=False,
            message=message,
            errors=errors,
            status_code=status_code
        )