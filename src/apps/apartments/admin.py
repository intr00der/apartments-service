from django.contrib import admin

from .models import Apartment, ApartmentPhoto, Reservation, Review

admin.site.register(Apartment)
admin.site.register(ApartmentPhoto)
admin.site.register(Reservation)
admin.site.register(Review)