from django.shortcuts import get_object_or_404
from accounts.models import APIKey


class APIKeySelector:

    @staticmethod
    def get_api_keys(user=None):
        qs = APIKey.objects.only(
            "id",
            "user_id",
            "name",
            "prefix",
            "usage_limit",
            "usage_count",
            "expires_at",
            "created_at",
        )

        if user and not user.is_staff:
            qs = qs.filter(user=user)

        return qs

    @staticmethod
    def get_api_key_by_id(api_key_id, user=None):
        qs = APIKeySelector.get_api_keys(user)
        return get_object_or_404(qs, id=api_key_id)
    