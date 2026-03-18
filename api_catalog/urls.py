from django.urls import path
from api_catalog.views.category import (
    APICategoryListCreateView,
    APICategoryDetailView
)
from api_catalog.views.endpoint import (
    APIEndpointListCreateView, 
    APIEndpointDetailView
)

app_name = "api_catalog"

urlpatterns = [
    path("categories/", APICategoryListCreateView.as_view(), name="api-categories"),
    path("categories/<uuid:pk>/", APICategoryDetailView.as_view(), name="api-category-detail"),
    path("endpoint", APIEndpointListCreateView.as_view(), name="api-endpoints"),
    path("endpoints/<uuid:pk>/", APIEndpointDetailView.as_view(), name="api-endpoint-detail"),
]