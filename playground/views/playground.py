from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from core.api.base_view import BaseAPIView
from playground.models import APIPlayground
from playground.serializers import APIPlaygroundSerializer

class APIPlaygroundListCreateView(BaseAPIView, ListCreateAPIView):
    queryset = APIPlayground.objects.select_related("api", "tested_by").all()
    serializer_class = APIPlaygroundSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["method", "status", "api", "tested_by"]
    search_fields = ["endpoint_url", "error"]
    ordering_fields = ["created_at", "response_time", "status_code"]
    ordering = ["-created_at"]

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
            message="API Playground history fetched successfully",
            data=data,
            meta=meta
        )

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)

        return self.success_response(
            message="API executed successfully",
            data=res.data,
            status_code=res.status_code
        )


class APIPlaygroundDetailView(BaseAPIView, RetrieveDestroyAPIView):
    queryset = APIPlayground.objects.select_related("api", "tested_by").all()
    serializer_class = APIPlaygroundSerializer

    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request, *args, **kwargs)

        return self.success_response(
            message="API Playground detail fetched successfully",
            data=res.data
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return self.success_response(
            message="API Playground record deleted successfully",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )


class APIPlaygroundRerunView(BaseAPIView, APIView):

    def post(self, request, pk):
        try:
            instance = APIPlayground.objects.get(pk=pk)
        except APIPlayground.DoesNotExist:
            return self.error_response(
                message="Record not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = APIPlaygroundSerializer(
            data={
                "api": instance.api.id,
                "method": instance.method,
                "endpoint_url": instance.endpoint_url,
                "request_body": instance.request_body,
                "query_params": instance.query_params,
                "request_headers": instance.request_headers,
            },
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return self.success_response(
            message="API re-executed successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )