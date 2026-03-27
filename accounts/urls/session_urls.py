from django.urls import path

from accounts.views import (
    UserSessionListView,
    UserSessionDeleteView,
    LogoutAllSessionsView,
    LogoutCurrentSessionView,
)

urlpatterns = [
    path("", UserSessionListView.as_view()),
    path("<uuid:id>/", UserSessionDeleteView.as_view()),
    path("logout-all/", LogoutAllSessionsView.as_view()),
    path("logout-current/", LogoutCurrentSessionView.as_view()),
]
