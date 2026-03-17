from rest_framework import serializers
from api_catalog.models.category import APICategory

class APICategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = APICategory
        fields = "__all__"
        