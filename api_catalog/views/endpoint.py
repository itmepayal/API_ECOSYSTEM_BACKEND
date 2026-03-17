from rest_framework import status
from core.api.base_view import BaseAPIView
from api_catalog.models import APICategory
from api_catalog.serializers import APICategorySerializer
from django.shortcuts import get_object_or_404

class APICategoryListCreateView(BaseAPIView):
    def get(self, request, *args, **kwargs):
        categories = APICategory.objects.all()
        serializer = APICategorySerializer(categories, many=True)
        return self.success_response(
            message="API Categories fetched successfully",
            data=serializer.data,
        )

    def post(self, request, *args, **kwargs):
        serializer = APICategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return self.success_response(
                message="API Category created successfully",
                data=APICategorySerializer(category).data,
                status_code=status.HTTP_201_CREATED,
            )
        return self.error_response(
            message="API Category creation failed",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

class APICategoryDetailView(BaseAPIView):

    def get_object(self, pk):
        return get_object_or_404(APICategory, pk=pk)

    def get(self, request, pk, *args, **kwargs):
        category = self.get_object(pk)
        serializer = APICategorySerializer(category)
        return self.success_response(
            message="Category fetched successfully",
            data=serializer.data,
        )

    def put(self, request, pk, *args, **kwargs):
        category = self.get_object(pk)
        serializer = APICategorySerializer(category, data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return self.success_response(
                message="Category updated successfully",
                data=APICategorySerializer(category).data,
            )
        return self.error_response(
            message="Category update failed",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, pk, *args, **kwargs):
        category = self.get_object(pk)
        serializer = APICategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            category = serializer.save()
            return self.success_response(
                message="Category partially updated successfully",
                data=APICategorySerializer(category).data,
            )
        return self.error_response(
            message="Partial update failed",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk, *args, **kwargs):
        category = self.get_object(pk)
        category.delete()
        return self.success_response(
            message="Category deleted successfully",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT,
        )