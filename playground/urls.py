from django.urls import path
from playground.views import (
    APIPlaygroundListCreateView,
    APIPlaygroundDetailView,
    APIPlaygroundRerunView,
)

urlpatterns = [
    path("", APIPlaygroundListCreateView.as_view(), name="playground-list-create"),
    path("<uuid:pk>/", APIPlaygroundDetailView.as_view(), name="playground-detail"),
    path("<uuid:pk>/rerun/", APIPlaygroundRerunView.as_view(), name="playground-rerun"),
]
