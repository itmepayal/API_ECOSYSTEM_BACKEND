from django.contrib.auth.models import BaseUserManager
from core.constants import ROLE_ADMIN, ROLE_USER

class UserManager(BaseUserManager):
    def _create_user(self, email, username, password=None, **extra_fields):

        if not email:
            raise ValueError("Email must be provided")

        if not username:
            raise ValueError("Username must be provided")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, username, password=None, **extra_fields):

        extra_fields.setdefault("role", ROLE_USER)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):

        extra_fields.setdefault("role", ROLE_ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
    
        return self._create_user(email, username, password, **extra_fields)
    