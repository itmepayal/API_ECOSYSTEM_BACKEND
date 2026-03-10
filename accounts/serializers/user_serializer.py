from rest_framework import serializers
from accounts.models import User

# =========================================================
# User Serializer
# =========================================================
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer used to return user profile data.

    Purpose:
    - Serialize user information for API responses
    - Ensure sensitive fields are not exposed
    - Provide a consistent representation of user data

    This serializer is primarily used in:
    - Authentication responses
    - User profile endpoints
    """
    # ---------------------------------
    # SERIALIZER META CONFIGURATION
    # ---------------------------------
    class Meta:
        """
        Defines model mapping and exposed fields.
        """

        # Associate serializer with User model
        model = User

        # Fields that will be included in API responses
        fields = (
            "id",          
            "email",        
            "username",     
            "avatar",   
            "role",       
            "is_verified",
            "created_at", 
        )

        # ---------------------------------
        # READ ONLY FIELDS
        # ---------------------------------
        read_only_fields = (
            "id",
            "email",
            "username",
            "avatar",
            "role",
            "is_verified",
            "created_at",
        )