from core.api.base_view import BaseAPIView
from rest_framework import status
from api_catalog.models.category import APICategory
from api_catalog.serializers.category import APICategorySerializer

class APICategoryListCreateView(BaseAPIView):

    def get(self, request):
        categories = APICategory.objects.all()
        serializer = APICategorySerializer(categories, many=True)
        return self.success_response(
            message="Categories fetched successfully",
            data=serializer.data,
        )

    def post(self, request):
        serializer = APICategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return self.success_response(
                message="Category created successfully",
                data=APICategorySerializer(category).data,
                status_code=status.HTTP_201_CREATED
            )
        return self.error_response(
            message="Category creation failed",
            errors=serializer.errors,
        )
        