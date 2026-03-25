import json
from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from core.api.base_view import BaseAPIView
from playground.models import APIPlayground
from playground.serializers import APIPlaygroundSerializer


# =========================================================
# LIST + CREATE
# =========================================================
class APIPlaygroundListCreateView(BaseAPIView, ListCreateAPIView):
    serializer_class = APIPlaygroundSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["method", "status", "api"]
    search_fields = ["endpoint_url", "error"]
    ordering_fields = ["created_at", "response_time", "status_code"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        qs = APIPlayground.objects.select_related("api", "tested_by")

        # Admin can see all
        if user.is_staff:
            return qs.all()

        # User sees only own
        return qs.filter(tested_by=user)

    def perform_create(self, serializer):
        serializer.save(tested_by=self.request.user)

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


# =========================================================
# DETAIL + DELETE
# =========================================================
class APIPlaygroundDetailView(BaseAPIView, RetrieveDestroyAPIView):
    serializer_class = APIPlaygroundSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = APIPlayground.objects.select_related("api", "tested_by")

        if user.is_staff:
            return qs.all()

        return qs.filter(tested_by=user)

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


# =========================================================
# RERUN API
# =========================================================
class APIPlaygroundRerunView(BaseAPIView, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user

        # Secure fetch
        instance = APIPlayground.objects.filter(pk=pk)

        if not user.is_staff:
            instance = instance.filter(tested_by=user)

        instance = instance.first()

        if not instance:
            return self.error_response(
                message="Record not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        def safe_parse(value):
            if not value:
                return None
            try:
                return json.loads(value) if isinstance(value, str) else value
            except json.JSONDecodeError:
                return None

        serializer = APIPlaygroundSerializer(
            data={
                "api": instance.api.id if instance.api else None,
                "method": instance.method,
                "endpoint_url": instance.endpoint_url,
                "request_body": safe_parse(instance.request_body),
                "query_params": safe_parse(instance.query_params),
                "request_headers": safe_parse(instance.request_headers),
            },
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save(tested_by=request.user)

        return self.success_response(
            message="API re-executed successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )
        