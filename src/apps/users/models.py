from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager
from .validators import NameValidator


class User(AbstractBaseUser, PermissionsMixin):
    class GenderChoices(models.IntegerChoices):
        FEMALE = 1, _('Female')
        MALE = 2, _('Male')
        OTHER = 3, _('Other')

    email = models.EmailField(unique=True, max_length=255, blank=False)
    first_name = models.CharField(validators=[NameValidator], max_length=50)
    last_name = models.CharField(validators=[NameValidator], max_length=50)
    gender = models.IntegerField(choices=GenderChoices.choices)
    born_at = models.DateField(null=True, blank=True)
    country = models.ForeignKey(
        'apartments.Country', on_delete=models.PROTECT, null=True, blank=True
    )
    city = models.ForeignKey(
        'apartments.City', on_delete=models.PROTECT, null=True, blank=True
    )
    passport = models.FileField(
        upload_to='users/passport_scans/', null=True, blank=True
    )
    is_owner = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'password', 'first_name',
        'last_name', 'gender',
    ]
