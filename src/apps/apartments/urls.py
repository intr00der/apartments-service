from django.urls import path
from .views import (
    home,
    register_apartment,
    unverified_apartment_list,
    apartment_detail,
    verify,
    profile_apartment_list,
)

urlpatterns = [
    path('', home, name='home'),
    path('register-apartment/', register_apartment, name='register-apartment'),
    path('unverified-list/', unverified_apartment_list, name='unverified-list'),
    path('apartments/<apartment_pk>/', apartment_detail, name='apartment-detail'),
    path('verify/<apartment_pk>', verify, name='verify'),
    path('my-apartments/', profile_apartment_list, name='profile-apartments-list'),
]
