# =========================================================
# Django REST Framework
# =========================================================
from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend

# =========================================================
# Core
# =========================================================
from core.api.base_view import BaseAPIView

# =========================================================
# API Catalog
# =========================================================
from api_catalog.serializers.endpoint import APIEndpointSerializer
from api_catalog.services import APIEndpointService

# =========================================================
# API ENDPOINT LIST & CREATE
# =========================================================
class APIEndpointListCreateView(BaseAPIView, ListCreateAPIView):

    serializer_class = APIEndpointSerializer

    # =====================================================
    # FILTERING CONFIG
    # =====================================================
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name", "method", "is_public", "category"]
    search_fields = ["name", "description", "endpoint"]
    ordering_fields = ["name", "created_at", "rate_limit"]
    ordering = ["name"]

    # =====================================================
    # QUERYSET
    # =====================================================
    def get_queryset(self):
        return APIEndpointService.get_queryset()

    # =====================================================
    # LIST API
    # =====================================================
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        payload = APIEndpointService.build_list_response(
            response,
            message="API Endpoints fetched successfully"
        )

        return self.success_response(**payload)

    # =====================================================
    # CREATE API
    # =====================================================
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return self.success_response(
            message="API Endpoint created successfully",
            data=response.data,
            status_code=response.status_code
        )


# =========================================================
# API ENDPOINT DETAIL
# =========================================================
class APIEndpointDetailView(BaseAPIView, RetrieveUpdateDestroyAPIView):

    serializer_class = APIEndpointSerializer

    # =====================================================
    # QUERYSET
    # =====================================================
    def get_queryset(self):
        return APIEndpointService.get_queryset()

    # =====================================================
    # RETRIEVE API
    # =====================================================
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        return self.success_response(
            message="API Endpoint fetched successfully",
            data=response.data
        )

    # =====================================================
    # UPDATE API
    # =====================================================
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        return self.success_response(
            message="API Endpoint updated successfully",
            data=response.data
        )

    # =====================================================
    # PARTIAL UPDATE API
    # =====================================================
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # =====================================================
    # DELETE API
    # =====================================================
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return self.success_response(
            message="API Endpoint deleted successfully",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )
        