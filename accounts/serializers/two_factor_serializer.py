# =========================================================
# Django REST Framework
# =========================================================
from rest_framework import serializers

# =========================================================
# TWOFACTOR SERIALIZER
# =========================================================
class TwoFactorLoginVerifySerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    code = serializers.CharField(max_length=6)
    
class TwoFactorVerifySetupSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    