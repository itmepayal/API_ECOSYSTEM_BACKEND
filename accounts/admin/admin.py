from django.contrib import admin
from accounts.models import User


# =========================================================
# User Admin Configuration
# =========================================================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin configuration for the User model.

    This configuration customizes how users are displayed
    and managed inside the Django admin panel.

    Features:
    - Custom list display for user overview
    - Search functionality
    - Filtering options
    - Organized fieldsets for better admin UI
    """

    # -----------------------------------------------------
    # LIST DISPLAY
    # -----------------------------------------------------
    # Fields shown in the admin list view
    list_display = (
        "email",        
        "username",   
        "role",        
        "is_verified",
        "is_staff",    
        "is_active",
        "created_at",  
    )


    # -----------------------------------------------------
    # SEARCH CONFIGURATION
    # -----------------------------------------------------
    # Enables search functionality in admin panel
    search_fields = (
        "email",
        "username",
    )


    # -----------------------------------------------------
    # FILTER CONFIGURATION
    # -----------------------------------------------------
    # Sidebar filters for quick filtering
    list_filter = (
        "role",
        "is_verified",
        "is_staff",
        "is_active",
    )


    # -----------------------------------------------------
    # DEFAULT ORDERING
    # -----------------------------------------------------
    # Sort users by newest accounts first
    ordering = ("-created_at",)


    # -----------------------------------------------------
    # READ ONLY FIELDS
    # -----------------------------------------------------
    # Prevent modification of these fields in admin
    readonly_fields = (
        "created_at",
    )


    # -----------------------------------------------------
    # FIELD ORGANIZATION
    # -----------------------------------------------------
    # Groups fields into sections for better admin UI
    fieldsets = (

        # Basic user information
        ("Basic Info", {
            "fields": (
                "email",
                "username",
                "avatar"
            )
        }),

        # Role management
        ("Role", {
            "fields": ("role",)
        }),

        # Account status flags
        ("Account Status", {
            "fields": (
                "is_verified",
                "is_active",
                "is_staff"
            )
        }),

        # Security related fields
        ("Security", {
            "fields": (
                "refresh_token_hash",
                "refresh_token_expiry",
                "forgot_password_token",
                "forgot_password_expiry",
                "email_verification_token",
                "email_verification_expiry",
            )
        }),

        # Two factor authentication configuration
        ("Two Factor Authentication", {
            "fields": (
                "is_2fa_enabled",
                "totp_secret"
            )
        }),

        # Metadata information
        ("Metadata", {
            "fields": ("created_at",)
        }),
    )