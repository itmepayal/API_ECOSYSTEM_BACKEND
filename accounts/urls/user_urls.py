from django.urls import path

from accounts.views.me_view import (
    MeView,
    UpdateAvatarView
)

urlpatterns = [
    path("me/", MeView.as_view()),
    path("me/avatar/", UpdateAvatarView.as_view()),
]