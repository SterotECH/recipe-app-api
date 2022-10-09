"""
Database model for Core
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for User"""

    def create_user(self, email, password, **extra_fields):
        """Create save and return new User"""
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        if not password:
            raise ValueError("User must have a password")
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create Superuser"""
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User models in the system"""

    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
