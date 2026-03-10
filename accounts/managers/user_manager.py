from django.contrib.auth.models import BaseUserManager
from core.constants import ROLE_ADMIN, ROLE_USER

# =========================================================
# Custom User Manager
# =========================================================
class UserManager(BaseUserManager):
    """
    Custom manager for the User model.

    Responsibilities:
    - Handle user creation
    - Handle superuser creation
    - Normalize email addresses
    - Ensure proper permission flags

    This manager is required when using a custom user model
    based on AbstractBaseUser.
    """

    # -----------------------------------------------------
    # INTERNAL USER CREATION METHOD
    # -----------------------------------------------------
    def _create_user(self, email, username, password=None, **extra_fields):
        """
        Internal method used by both create_user and create_superuser.

        Responsibilities:
        - Validate required fields
        - Normalize email
        - Hash password
        - Save user to database
        """

        # Validate required fields
        if not email:
            raise ValueError("Email must be provided")

        if not username:
            raise ValueError("Username must be provided")

        # Normalize email address (lowercase domain etc.)
        email = self.normalize_email(email)

        # Create user instance
        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )

        # Hash and set password securely
        user.set_password(password)

        # Save user to database
        user.save(using=self._db)

        return user


    # -----------------------------------------------------
    # CREATE NORMAL USER
    # -----------------------------------------------------
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and return a regular user.

        Default permissions:
        - role = ROLE_USER
        - is_staff = False
        - is_superuser = False
        """

        # Set default values for normal users
        extra_fields.setdefault("role", ROLE_USER)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(
            email,
            username,
            password,
            **extra_fields
        )


    # -----------------------------------------------------
    # CREATE SUPERUSER
    # -----------------------------------------------------
    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and return a superuser (admin).

        Default permissions:
        - role = ROLE_ADMIN
        - is_staff = True
        - is_superuser = True
        - is_verified = True
        """

        # Set default admin permissions
        extra_fields.setdefault("role", ROLE_ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        # Validate admin permissions
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(
            email,
            username,
            password,
            **extra_fields
        )
    