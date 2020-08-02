from django.db import models

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .manager import AppUserManager
from django.core.exceptions import ValidationError
import uuid
from django.utils import timezone
from datetime import datetime
from django.db import IntegrityError
from django.conf import settings
import uuid
import base64
import os


class BaseTimeStampModel(models.Model):
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

def generate_id():
    r_id = base64.b64encode(os.urandom(6)).decode('ascii')
    return r_id


def usermanagerprofile(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return '{0}_manager_profile_pic/{1}'.format(instance.username, filename)


class User(AbstractBaseUser, PermissionsMixin):
    KARYAWAN = 'karyawan'
    ADMIN = 'ADMIN'
    STAFF = 'STAFF'
    ROLE = (
        (KARYAWAN,'karyawan'),
        (ADMIN,'ADMIN'),
        (STAFF,'STAFF')
        )
    uid = models.CharField(max_length=255, primary_key=True,
                           editable=False, default=generate_id())
    email = models.EmailField(('email address'), unique=True,null=True,blank=True)
    username = models.CharField(
        max_length=255, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    alamat = models.TextField(blank=True, null=True)
    nama = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to=usermanagerprofile, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=20,choices=ROLE, default=KARYAWAN)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nama']

    objects = AppUserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user_core'
