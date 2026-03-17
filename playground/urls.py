from django.urls import path
from playground.views import (
    APIPlaygroundListCreateView,
    APIPlaygroundDetailView,
    APIPlaygroundRerunView,
)

urlpatterns = [
    path("", APIPlaygroundListCreateView.as_view(), name="playground-list-create"),
    path("<int:pk>/", APIPlaygroundDetailView.as_view(), name="playground-detail"),
    path("<int:pk>/rerun/", APIPlaygroundRerunView.as_view(), name="playground-rerun"),
]
