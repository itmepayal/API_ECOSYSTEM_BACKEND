from django.urls import path

from api_catalog.views.category import APICategoryListCreateView
from api_catalog.views.endpoint import APIEndpointListCreateView

app_name = "api_catalog"

urlpatterns = [
    path("categories/", APICategoryListCreateView.as_view(), name="api-categories"),
    # path("endpoints/", APIEndpointListCreateView.as_view(), name="api-endpoints"),
]
