from django.contrib import admin

from .models import (
    Country,
    City,
    Apartment,
    ApartmentPhoto,
    Booking,
    Review
)

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Apartment)
admin.site.register(ApartmentPhoto)
admin.site.register(Booking)
admin.site.register(Review)
