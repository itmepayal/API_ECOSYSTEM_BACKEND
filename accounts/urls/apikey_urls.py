from django.urls import path
from accounts.views import (
    APIKeyListCreateView,
    APIKeyDetailView,
    VerifyAPIKeyView
)

from django.urls import path
from accounts.views import (
    APIKeyListCreateView,
    APIKeyDetailView,
    VerifyAPIKeyView
)

urlpatterns = [
    path("", APIKeyListCreateView.as_view()),
    path("<uuid:id>/", APIKeyDetailView.as_view()),
    path("verify/", VerifyAPIKeyView.as_view(), name="api-key-verify"),
]
