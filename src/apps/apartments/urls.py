from django.urls import path
from .views import (
    home,
    register_apartment,
    unverified_apartment_list,
    apartment_detail,
    verify,
    profile_apartment_list,
    book_apartment,
    post_review,
    bookings_list,
    apartment_bound_bookings,
    photo_detail,
)

urlpatterns = [
    path('', home, name='home'),
    path('profile/apartments/', profile_apartment_list, name='profile-apartments-list'),
    path('profile/bookings/', bookings_list, name='bookings-list'),
    path('apartments/register/', register_apartment, name='register-apartment'),
    path('apartments/unverified/', unverified_apartment_list, name='unverified-list'),
    path('apartments/<apartment_pk>/', apartment_detail, name='apartment-detail'),
    path('apartments/<apartment_pk>/book/', book_apartment, name='book-apartment'),
    path('apartments/<apartment_pk>/review/', post_review, name='review'),
    path('apartments/<apartment_pk>/verify/', verify, name='verify'),
    path('apartments/<apartment_pk>/bookings/', apartment_bound_bookings, name='apartment-bound-bookings'),
    path('apartments/<apartment_pk>/photos/<photo_pk>/', photo_detail, name='photo-detail')
]
