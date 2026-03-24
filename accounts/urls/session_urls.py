from django.urls import path

from accounts.views.user_session_views import (
    UserSessionView,
    UserSessionDestroyView
)

urlpatterns = [
    path("", UserSessionView.as_view()),                 
    path("<uuid:id>/", UserSessionDestroyView.as_view()),
]