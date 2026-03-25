from rest_framework.views import APIView
from core.mixins.api_response_mixin import APIResponseMixin

class BaseAPIView(APIResponseMixin, APIView):
    pass
