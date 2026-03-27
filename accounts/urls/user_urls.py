from django.urls import path

from accounts.views import (
    MeView,
    UpdateAvatarView
)

urlpatterns = [
    path("me/", MeView.as_view()),
    path("me/avatar/", UpdateAvatarView.as_view()),
]