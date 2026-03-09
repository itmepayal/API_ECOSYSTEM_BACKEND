from rest_framework import serializers
from accounts.models import User
from accounts.selectors.user_selector import get_user_by_email

class RegisterSerializer(serializers.Serializer):

    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=8, write_only=True)

    def validate_email(self, value):
        if get_user_by_email(value):
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken")
        return value