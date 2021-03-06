from django.contrib import admin

from .models import (
    Country,
    City,
    Apartment,
    ApartmentPhoto,
    Reservation,
    Review
)

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Apartment)
admin.site.register(ApartmentPhoto)
admin.site.register(Reservation)
admin.site.register(Review)
