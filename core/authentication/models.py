from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from helper.models import TimestampWithUid


class User(AbstractBaseUser, TimestampWithUid, PermissionsMixin):
    id = TimestampWithUid.uid
    email = models.EmailField(("email address"), unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "username"
    AUTH_FIELD_NAME = "email"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
