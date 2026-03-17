from rest_framework import status
from core.responses.api_response import api_response

class APIResponseMixin:

    def success_response(self, message="Success", data=None, meta=None, status_code=status.HTTP_200_OK):
        return api_response(
            success=True,
            message=message,
            data=data,
            meta=meta,
            status_code=status_code
        )

    def error_response(self, message="Error", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        return api_response(
            success=False,
            message=message,
            errors=errors,
            status_code=status_code
        )

    def validation_error(self, errors, message="Validation failed"):
        return self.error_response(
            message=message,
            errors=errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    def server_error(self, message="Internal Server Error"):
        return self.error_response(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )