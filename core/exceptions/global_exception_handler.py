from rest_framework.views import exception_handler
from rest_framework import status

from core.responses.api_response import api_response


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        return api_response(
            success=False,
            message="Something went wrong",
            errors=response.data,
            status_code=response.status_code
        )

    return api_response(
        success=False,
        message="Internal server error",
        errors=str(exc),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )