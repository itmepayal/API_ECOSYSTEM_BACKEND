from django.db.models import F
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from accounts.models import APIKey


class APIKeyService:
    MAX_KEYS_PER_USER = 5

    # =====================================================
    # CREATE
    # =====================================================
    @staticmethod
    @transaction.atomic
    def create_api_key(user, validated_data):
        current_count = (
            APIKey.objects.select_for_update()
            .filter(user=user)
            .count()
        )

        if current_count >= APIKeyService.MAX_KEYS_PER_USER:
            raise ValidationError("API key limit reached")

        raw_key, key_hash, prefix = APIKey.generate_key()

        instance = APIKey.objects.create(
            user=user,
            key_hash=key_hash,
            prefix=prefix,
            **validated_data
        )

        return instance, raw_key

    # =====================================================
    # UPDATE
    # =====================================================
    @staticmethod
    @transaction.atomic
    def update_api_key(instance, validated_data):
        # 🔒 prevent sensitive updates
        restricted_fields = {"key", "key_hash", "usage_count"}

        for field in restricted_fields:
            if field in validated_data:
                raise ValidationError(f"{field} cannot be updated")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if validated_data:
            instance.save(update_fields=list(validated_data.keys()))

        return instance

    # =====================================================
    # DELETE
    # =====================================================
    @staticmethod
    @transaction.atomic
    def delete_api_key(instance):
        instance.delete()

    # =====================================================
    # ACTIVATE / DEACTIVATE
    # =====================================================
    @staticmethod
    @transaction.atomic
    def set_active_status(instance, is_active: bool):
        instance.is_active = is_active
        instance.save(update_fields=["is_active"])
        return instance

    # =====================================================
    # VALIDATION
    # =====================================================
    @staticmethod
    def is_expired(api_key):
        return api_key.expires_at and api_key.expires_at <= timezone.now()

    @staticmethod
    def validate_key_usage(api_key):
        if not api_key:
            raise ValidationError("Invalid API Key")

        if not api_key.is_active:
            raise ValidationError("API Key is disabled")

        if APIKeyService.is_expired(api_key):
            raise ValidationError("API Key expired")

        if api_key.usage_count >= api_key.usage_limit:
            raise ValidationError("API usage limit exceeded")

    # =====================================================
    # VERIFY ONLY
    # =====================================================
    @staticmethod
    def verify_key(raw_key: str):
        if not raw_key:
            raise ValidationError("API key is required")

        api_key = APIKey.verify_key(raw_key)

        APIKeyService.validate_key_usage(api_key)

        return api_key

    # =====================================================
    # VERIFY + USE
    # =====================================================
    @staticmethod
    @transaction.atomic
    def verify_and_use_key(raw_key: str):
        if not raw_key:
            raise ValidationError("API key is required")

        api_key = APIKey.verify_key(raw_key)

        APIKeyService.validate_key_usage(api_key)

        APIKey.objects.filter(id=api_key.id).update(
            usage_count=F("usage_count") + 1
        )

        api_key.refresh_from_db()

        return api_key

    # =====================================================
    # SELECTORS
    # =====================================================
    @staticmethod
    def get_user_api_keys(user):
        return APIKey.objects.filter(user=user).order_by("-created_at")

    @staticmethod
    def get_api_key_by_id(user, key_id):
        try:
            return APIKey.objects.get(id=key_id, user=user)
        except APIKey.DoesNotExist:
            raise ValidationError("API Key not found")