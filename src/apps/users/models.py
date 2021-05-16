from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .user_managers import ApartmentServiceUserManager


class ApartmentServiceUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('0', 'Male'),
        ('1', 'Female')
    )

    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False
    )
    first_name = models.CharField(
        _('first name'),
        max_length=30
    )
    last_name = models.CharField(
        _('last name'),
        max_length=50
    )
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES
    )
    born = models.DateField(
        null=True,
        blank=True
    )
    country = models.CharField(
        max_length=100
    )
    state = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=100
    )
    passport = models.FileField(
        upload_to='media/passport_scans/',
        null=True,
        blank=True
    )

    is_owner = models.BooleanField(
        _('property owner status'),
        default=False
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False
    )
    is_admin = models.BooleanField(
        _('admin status'),
        default=False
    )
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
    )
    date_joined = models.DateField(
        _('date joined'),
        auto_now_add=True
    )

    objects = ApartmentServiceUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'password', 'first_name',
        'last_name', 'gender',
        'country', 'city'
    ]
