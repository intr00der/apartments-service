from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)
from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import User

from .fields import ChoiceArrayField


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, related_name='regions', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(
        Region, related_name='cities', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Apartment(models.Model):
    class Amount(models.IntegerChoices):
        ONE = 1, _('одна')
        TWO = 2, _('две')
        THREE = 3, _('три')
        FOUR = 4, _('четыре')
        MORE_THAN_FOUR = 5, _('больше, чем четыре')

    class ConvenienceItems(models.TextChoices):
        WIFI = 'WIFI', _('Wi-Fi')
        CONDITIONER = 'COND', _('Кондиционер')
        WASHING_MACHINE = 'WSHM', _('Стиральная машина')
        DISHWASHER = 'DSHW', _('Посудомоечная машина')
        HAIRDRYER = 'HRDR', _('Сушилка для волос')
        MINIBAR = 'MNBR', _('Минибар')
        LANDLINE_PHONE = 'LLPH', _('Стационарный телефон')
        CLEAN_LINEN = 'CLLN', _('Чистое белье')

    owner = models.ForeignKey(
        User, related_name='apartments', on_delete=models.CASCADE
    )
    country = models.ForeignKey(
        Country, related_name='apartments', on_delete=models.PROTECT
    )
    region = models.ForeignKey(
        Region, related_name='apartments', on_delete=models.PROTECT
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

    def __str__(self):
        return f'{self.country}, {self.region}, {self.city}'


class ApartmentPhoto(models.Model):
    apartment = models.ForeignKey(
        Apartment, related_name='photos', on_delete=models.CASCADE
    )
    photo = models.ImageField(upload_to='apartments/images/')
    position = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.apartment} ({self.pk})'


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

    def __str__(self):
        return f'{self.user} - {self.apartment}' \
               f'({self.datetime_start} - {self.datetime_end})'


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

    def __str__(self):
        return f'{self.user} - {self.apartment} ({self.rating})'
