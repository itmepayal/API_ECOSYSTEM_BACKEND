from django.urls import path

from accounts.views.admin_session_view import (
    AdminSessionView,
    AdminSessionDestroyView
)

urlpatterns = [
    path("sessions/", AdminSessionView.as_view()),
    path("sessions/<uuid:id>/", AdminSessionDestroyView.as_view()),
]