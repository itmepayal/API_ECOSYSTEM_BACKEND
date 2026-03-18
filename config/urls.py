from django.contrib import admin
from django.urls import path, include

from rest_framework.permissions import AllowAny

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "api/v1/accounts/",
        include(("accounts.urls", "accounts"), namespace="accounts")
    ),
    
    path(
        "api/v1/api-catalog/",
        include(("api_catalog.urls", "api_catalog"), namespace="api-catalog")
    ),
    
    path(
        "api/v1/playground/",
        include(("playground.urls", "playground"), namespace="playground")
    ),
    
    path(
        "api/v1/request-logs/",
        include(("request_logs.urls", "request_logs"), namespace="request_logs")
    ),
    
    # API Schema
    path(
        "api/v1/schema/",
        SpectacularAPIView.as_view(permission_classes=[AllowAny]),
        name="schema",
    ),

    # Swagger UI
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema", permission_classes=[AllowAny]),
        name="swagger-ui",
    ),

    # ReDoc UI
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema", permission_classes=[AllowAny]),
        name="redoc",
    ),
]