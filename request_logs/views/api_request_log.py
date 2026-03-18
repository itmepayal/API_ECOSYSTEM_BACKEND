from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend

from core.api.base_view import BaseAPIView
from request_logs.models import APIRequestLog
from request_logs.serializers.api_request_log import APIRequestLogSerializer

class APIRequestLogListView(BaseAPIView, ListAPIView):
    queryset = APIRequestLog.objects.select_related("api", "api_key").all()
    serializer_class = APIRequestLogSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ["api", "api_key", "status_code", "method"]
    search_fields = ["path", "user_agent"]
    ordering_fields = ["created_at", "response_time", "status_code"]
    ordering = ["-created_at"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.success_response(
                message="API logs fetched successfully",
                data=serializer.data,
                meta={
                    "count": self.paginator.page.paginator.count,
                    "next": self.paginator.get_next_link(),
                    "previous": self.paginator.get_previous_link(),
                }
            )

        serializer = self.get_serializer(queryset, many=True)

        return self.success_response(
            message="API logs fetched successfully",
            data=serializer.data
        )

class APIRequestLogDetailView(BaseAPIView, RetrieveAPIView):
    queryset = APIRequestLog.objects.select_related("api", "api_key").all()
    serializer_class = APIRequestLogSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return self.success_response(
            message="API log fetched successfully",
            data=serializer.data
        )