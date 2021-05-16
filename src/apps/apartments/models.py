from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import \
    MinValueValidator, \
    MaxValueValidator, \
    DecimalValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from multiselectfield import MultiSelectField

from users.models import ApartmentServiceUser


class Apartment(models.Model):
    AMOUNT_CHOICES = (
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (5, 'More than four')
    )

    CONVENIENCE_ITEM_CHOICES = (
        ('wifi', 'WiFi'),
        ('conditioner', 'Conditioner'),
        ('washing_machine', 'Washing machine'),
        ('dishwasher', 'Dishwasher'),
        ('hairdryer', 'Hairdryer'),
        ('minibar', 'Mini-Bar'),
        ('landline_phone', 'Landline phone'),
        ('clean_linen', 'Clean linen'),
    )

    owner = models.ForeignKey(ApartmentServiceUser, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField()
    room_amount = models.CharField(max_length=20, choices=AMOUNT_CHOICES)
    bedroom_amount = models.CharField(max_length=20, choices=AMOUNT_CHOICES)
    daily_rate = models.FloatField(
        validators=[
            MinValueValidator(0),
            DecimalValidator(max_digits=9, decimal_places=2)
        ]
    )
    registry_ordering = models.FileField(upload_to='apartments/registry_scans/')
    convenience_items = MultiSelectField(
        choices=CONVENIENCE_ITEM_CHOICES
    )
    is_verified = models.BooleanField(default=False)


class ApartmentPhoto(models.Model):
    apartment = models.ForeignKey(
        Apartment,
        verbose_name='photo',
        on_delete=models.CASCADE
    )
    photo = models.ImageField(
        upload_to='apartments/images/'
    )


class Reservation(models.Model):
    user = models.ForeignKey(ApartmentServiceUser, on_delete=models.PROTECT)
    apartment = models.ForeignKey(Apartment, on_delete=models.PROTECT)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()


class Review(models.Model):
    user = models.ForeignKey(ApartmentServiceUser, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    heading = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
            DecimalValidator(max_digits=1, decimal_places=2)
        ]
    )
