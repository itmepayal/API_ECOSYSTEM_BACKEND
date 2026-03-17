from rest_framework import serializers
from api_catalog.models.endpoint import APIEndpoint

class APIEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIEndpoint
        fields = "__all__"
        