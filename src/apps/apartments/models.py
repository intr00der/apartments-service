from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import User
from .fields import ChoiceArrayField


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, related_name='cities', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Apartment(models.Model):
    class Amount(models.IntegerChoices):
        ONE = 1, _('one')
        TWO = 2, _('two')
        THREE = 3, _('three')
        FOUR = 4, _('four')
        MORE_THAN_FOUR = 5, _('more')

    class ConvenienceItems(models.TextChoices):
        WIFI = 'WIFI', _('Wi-Fi')
        CONDITIONER = 'COND', _('Conditioner')
        WASHING_MACHINE = 'WSHM', _('Washing machine')
        DISHWASHER = 'DSHW', _('Dishwasher')
        HAIRDRYER = 'HRDR', _('Hairdryer')
        MINIBAR = 'MNBR', _('Minibar')
        LANDLINE_PHONE = 'LLPH', _('Landline phone')
        CLEAN_LINEN = 'CLLN', _('Clean linen')

    owner = models.ForeignKey(
        User, related_name='apartments', on_delete=models.CASCADE
    )
    country = models.ForeignKey(
        Country, related_name='apartments', on_delete=models.PROTECT
    )
    city = models.ForeignKey(
        City, related_name='apartments', on_delete=models.PROTECT
    )
    description = models.TextField()
    room_amount = models.IntegerField(choices=Amount.choices)
    bedroom_amount = models.IntegerField(choices=Amount.choices)
    daily_rate = models.DecimalField(max_digits=9, decimal_places=2)
    registry_ordering = models.FileField(upload_to='apartments/registry_scans/')
    convenience_items = ChoiceArrayField(
        models.CharField(max_length=50, choices=ConvenienceItems.choices)
    )
    is_verified = models.BooleanField(default=False)


class ApartmentPhoto(models.Model):
    apartment = models.ForeignKey(
        Apartment, related_name='photos', on_delete=models.CASCADE
    )
    photo = models.ImageField(upload_to='apartments/images/')
    position = models.IntegerField(null=True, blank=True)


class Reservation(models.Model):
    user = models.ForeignKey(
        User, related_name='reservations', on_delete=models.PROTECT
    )
    apartment = models.ForeignKey(
        Apartment, related_name='reservations', on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()


class Review(models.Model):
    user = models.ForeignKey(
        User, related_name='reviews', on_delete=models.CASCADE)
    apartment = models.ForeignKey(
        Apartment, related_name='reviews', on_delete=models.CASCADE
    )
    heading = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

