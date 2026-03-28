# =========================================================
# Django REST Framework
# =========================================================
from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# =========================================================
# Core
# =========================================================
from core.api.base_view import BaseAPIView

# =========================================================
# API Catalog
# =========================================================
from api_catalog.serializers import APICategorySerializer
from api_catalog.services import APICategoryService

# =========================================================
# API CATEGORY LIST & CREATE
# =========================================================
class APICategoryListCreateView(BaseAPIView, ListCreateAPIView):

    serializer_class = APICategorySerializer

    # =====================================================
    # FILTERING CONFIG
    # =====================================================
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    # =====================================================
    # QUERYSET
    # =====================================================
    def get_queryset(self):
        """
        Dynamic queryset (fixes stale data issue)
        """
        return APICategoryService.get_queryset()

    # =====================================================
    # LIST API
    # =====================================================
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        payload = APICategoryService.build_list_response(
            response,
            message="API Categories fetched successfully"
        )

        return self.success_response(**payload)

    # =====================================================
    # CREATE API
    # =====================================================
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return self.success_response(
            message="API Category created successfully",
            data=response.data,
            status_code=response.status_code
        )


# =========================================================
# API CATEGORY DETAIL
# =========================================================
class APICategoryDetailView(BaseAPIView, RetrieveUpdateDestroyAPIView):

    serializer_class = APICategorySerializer

    # =====================================================
    # QUERYSET
    # =====================================================
    def get_queryset(self):
        return APICategoryService.get_queryset()

    # =====================================================
    # RETRIEVE API
    # =====================================================
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        return self.success_response(
            message="Category fetched successfully",
            data=response.data
        )

    # =====================================================
    # UPDATE API
    # =====================================================
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        return self.success_response(
            message="Category updated successfully",
            data=response.data
        )

    # =====================================================
    # PARTIAL UPDATE API
    # =====================================================
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)

        return self.success_response(
            message="Category partially updated successfully",
            data=response.data
        )

    # =====================================================
    # DELETE API
    # =====================================================
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return self.success_response(
            message="Category deleted successfully",
            data=None
        )