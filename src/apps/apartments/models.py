from django.db import models
from django.utils.translation import ugettext_lazy as _

from .fields import ChoiceArrayField

from statistics import mean


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
        NULL = 0, _('not specified')
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
        'users.User', related_name='apartments', on_delete=models.CASCADE
    )
    country = models.ForeignKey(
        Country, related_name='apartments', on_delete=models.PROTECT
    )
    city = models.ForeignKey(
        City, related_name='apartments', on_delete=models.PROTECT
    )
    description = models.TextField()
    square_area = models.PositiveSmallIntegerField()
    room_amount = models.IntegerField(choices=Amount.choices)
    bedroom_amount = models.IntegerField(choices=Amount.choices)
    daily_rate = models.DecimalField(max_digits=9, decimal_places=2)
    registry_ordering = models.FileField(upload_to='apartments/registry_scans/')
    convenience_items = ChoiceArrayField(
        models.CharField(default=None, max_length=50, choices=ConvenienceItems.choices, blank=True, null=True)
    )
    average_rating = models.FloatField(null=True, blank=True)
    opens_at = models.DateField(null=True, blank=True)
    closes_at = models.DateField(null=True, blank=True)
    is_open = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_verified:
            self.owner.is_owner = True
            self.owner.save()
        super().save(*args, **kwargs)


class ApartmentPhoto(models.Model):
    apartment = models.ForeignKey(
        Apartment, related_name='photos', on_delete=models.CASCADE
    )
    photo = models.ImageField(upload_to='apartments/images/')
    position = models.IntegerField(null=True, blank=True)


class Booking(models.Model):
    user = models.ForeignKey(
        'users.User', related_name='bookings', on_delete=models.PROTECT
    )
    apartment = models.ForeignKey(
        Apartment, related_name='bookings', on_delete=models.PROTECT
    )
    created_at = models.DateField(auto_now_add=True)
    starts_at = models.DateField()
    ends_at = models.DateField()


class Review(models.Model):
    class Rating(models.IntegerChoices):
        ZERO = 0, _('0')
        ONE = 1, _('1')
        TWO = 2, _('2')
        THREE = 3, _('3')
        FOUR = 4, _('4')
        FIVE = 5, _('5')

    user = models.ForeignKey(
        'users.User', related_name='reviews', on_delete=models.CASCADE)
    apartment = models.ForeignKey(
        Apartment, related_name='reviews', on_delete=models.CASCADE
    )
    heading = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(choices=Rating.choices)

    def calculate_average_rating(self):
        apartment_ratings = Review.objects.filter(apartment=self.apartment).values('rating')
        ratings_lst = [i['rating'] for i in apartment_ratings]
        ratings_lst.append(self.rating)
        avg = round(mean(ratings_lst), 2)
        self.apartment.average_rating = avg
        self.apartment.save()

    def save(self, *args, **kwargs):
        self.calculate_average_rating()
        super().save(*args, **kwargs)
