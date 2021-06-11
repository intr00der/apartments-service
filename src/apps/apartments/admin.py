from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import (
    Country,
    City,
    Apartment,
    ApartmentPhoto,
    Booking,
    Review
)


class ApartmentAdmin(OSMGeoAdmin):
    default_lon = 4187639
    default_lat = 7509112
    default_zoom = 12


admin.site.register(Country)
admin.site.register(City)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(ApartmentPhoto)
admin.site.register(Booking)
admin.site.register(Review)
