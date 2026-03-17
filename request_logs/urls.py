from django.urls import path
from request_logs.views.api_request_log import (
    APIRequestLogListView,
    APIRequestLogDetailView,
)

urlpatterns = [
    path("logs/", APIRequestLogListView.as_view(), name="api-logs"),
    path("logs/<int:pk>/", APIRequestLogDetailView.as_view(), name="api-log-detail"),
]