from django.urls import path

from accounts.views.apikey_views import (
    APIKeyListCreateView,
    APIKeyDetailView
)

urlpatterns = [
    path("", APIKeyListCreateView.as_view()),            
    path("<uuid:pk>/", APIKeyDetailView.as_view()),      
]