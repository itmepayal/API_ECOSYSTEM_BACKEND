from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend

from core.api.base_view import BaseAPIView
from api_catalog.models.endpoint import APIEndpoint
from api_catalog.serializers.endpoint import APIEndpointSerializer

class APIEndpointListCreateView(BaseAPIView, ListCreateAPIView):
    queryset = APIEndpoint.objects.select_related("category").all()
    serializer_class = APIEndpointSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name", "method", "is_public", "category"]
    search_fields = ["name", "description", "endpoint"]
    ordering_fields = ["name", "created_at", "rate_limit"]
    ordering = ["name"]

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)

        if isinstance(res.data, dict):
            data = res.data.get("results", [])
            meta = {
                "count": res.data.get("count"),
                "next": res.data.get("next"),
                "previous": res.data.get("previous"),
            }
        else:
            data = res.data
            meta = None

        return self.success_response(
            message="API Endpoints fetched successfully",
            data=data,
            meta=meta
        )

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)

        return self.success_response(
            message="API Endpoint created successfully",
            data=res.data,
            status_code=res.status_code
        )


class APIEndpointDetailView(BaseAPIView, RetrieveUpdateDestroyAPIView):
    queryset = APIEndpoint.objects.select_related("category").all()
    serializer_class = APIEndpointSerializer

    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request, *args, **kwargs)

        return self.success_response(
            message="API Endpoint fetched successfully",
            data=res.data
        )

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)

        return self.success_response(
            message="API Endpoint updated successfully",
            data=res.data
        )

    def partial_update(self, request, *args, **kwargs):
        res = super().partial_update(request, *args, **kwargs)

        return self.success_response(
            message="API Endpoint partially updated successfully",
            data=res.data
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return self.success_response(
            message="API Endpoint deleted successfully",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )