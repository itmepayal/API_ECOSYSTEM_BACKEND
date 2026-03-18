import uuid
from rest_framework.views import exception_handler
from rest_framework import status
import traceback

from core.responses.api_response import api_response

def custom_exception_handler(exc, context):
    traceback.print_exc() 

    if isinstance(exc, (ValueError, TypeError)) and "uuid" in str(exc).lower():
        return api_response(
            success=False,
            message="Invalid UUID format",
            errors=str(exc),
            status_code=status.HTTP_400_BAD_REQUEST
        )

    response = exception_handler(exc, context)

    if response is not None:
        return api_response(
            success=False,
            message="Request failed",
            errors=response.data,
            status_code=response.status_code
        )

    return api_response(
        success=False,
        message="Internal server error",
        errors=str(exc),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )