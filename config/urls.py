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

    # =============================
    # AUTH
    # =============================
    path(
        "api/v1/accounts/",
        include(("accounts.urls.auth_urls", "accounts"), namespace="accounts")
    ),

    # =============================
    # USERS
    # =============================
    path(
        "api/v1/users/",
        include(("accounts.urls.user_urls", "users"), namespace="users")
    ),

    # =============================
    # API KEYS
    # =============================
    path(
        "api/v1/api-keys/",
        include(("accounts.urls.apikey_urls", "api_keys"), namespace="api_keys")
    ),

    # =============================
    # SESSIONS
    # =============================
    path(
        "api/v1/sessions/",
        include(("accounts.urls.session_urls", "sessions"), namespace="sessions")
    ),

    # =============================
    # ADMIN APIs
    # =============================
    path(
        "api/v1/admin/",
        include(("accounts.urls.admin_urls", "admin_api"), namespace="admin_api")
    ),

    # =============================
    # OTHER MODULES
    # =============================
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

    # =============================
    # API DOCUMENTATION
    # =============================
    path(
        "api/v1/schema/",
        SpectacularAPIView.as_view(permission_classes=[AllowAny]),
        name="schema",
    ),

    path(
        "swagger/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
            permission_classes=[AllowAny]
        ),
        name="swagger-ui",
    ),

    path(
        "redoc/",
        SpectacularRedocView.as_view(
            url_name="schema",
            permission_classes=[AllowAny]
        ),
        name="redoc",
    ),
]