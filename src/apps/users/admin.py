from django.contrib import admin

from .models import ApartmentServiceUser, ApartmentOwnerPassport

admin.site.register(ApartmentServiceUser)
admin.site.register(ApartmentOwnerPassport)

