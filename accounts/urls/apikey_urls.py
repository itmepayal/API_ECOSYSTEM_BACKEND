from django.urls import path
from accounts.views import (
    APIKeyListCreateView,
    APIKeyDetailView,
    AdminAPIKeyListView,
    AdminAPIKeyUpdateView,
    AdminAPIKeyDeleteView,
)

urlpatterns = [
    # USER
    path("", APIKeyListCreateView.as_view()),
    path("<uuid:id>/", APIKeyDetailView.as_view()),

    # ADMIN
    path("admin/", AdminAPIKeyListView.as_view()),
    path("admin/<uuid:id>/", AdminAPIKeyUpdateView.as_view()),
    path("admin/<uuid:id>/delete/", AdminAPIKeyDeleteView.as_view()),
]
