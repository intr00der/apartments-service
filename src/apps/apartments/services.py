from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator

from .models import Apartment, Booking

from datetime import (
    timedelta,
    datetime
)
from pyproj import Proj, transform

import json


def verify_apartment(apartment_pk):
    Apartment.objects.filter(id=apartment_pk).update(is_verified=True)


def calculate_timedelta(apartment):
    open_timedelta = (apartment.closes_at - apartment.opens_at).days
    default_days = 60
    default_timedelta = timedelta(days=default_days).days
    if open_timedelta > default_timedelta:
        return default_timedelta
    return open_timedelta


def parse_date_string(date_str):
    date_object = datetime.strptime(date_str, '%d.%m.%Y').date()
    return date_object


def get_date_range(start, end):
    return [start + timedelta(days=x) for x in range(0, (end - start).days)]


def get_booked_days(apartment):
    apartment_booking_dates = Booking.objects \
        .filter(apartment__pk=apartment.pk) \
        .values('starts_at', 'ends_at') \
        .order_by('starts_at')

    booked_days = []
    for date_interval in apartment_booking_dates:
        start = date_interval['starts_at']
        end = date_interval['ends_at']

        booking_date_range = [start + timedelta(days=x) for x in range(0, (end - start).days)]
        for dt in booking_date_range:
            booked_days.append(dt)
    return booked_days


def get_open_days(apartment):
    start = apartment.opens_at
    end = apartment.closes_at
    open_days = [start + timedelta(days=x) for x in range(0, (end - start).days)]
    return open_days


def get_available_days(apartment):
    booked_days = get_booked_days(apartment)
    open_days = get_open_days(apartment)
    available_days = [x for x in open_days if x not in booked_days]
    return available_days


def can_review(user, apartment):
    if user.id == apartment.owner_id:
        return False, "You can't leave a review on your own apartment."
    if not Booking.objects.filter(apartment=apartment, user=user):
        return False, "You can't leave a review on an apartment which you've never visited."
    return True, None


def filter_apartments_by_query(query_params):
    apartments = Apartment.objects.filter(is_verified=True)
    text = query_params.get('search_bar')
    daily_rate = query_params.get('daily_rate')
    square_area = query_params.get('square_area')
    room_amount = query_params.get('room_amount')
    bedroom_amount = query_params.get('bedroom_amount')
    convenience_items = query_params.getlist('convenience_items[]')
    rating = query_params.get('rating')
    location = query_params.get('location')

    if not square_area:
        square_area = 0
    if not room_amount:
        room_amount = 0
    if not bedroom_amount:
        bedroom_amount = 0
    if not rating:
        rating = 0
    if text:
        apartments = apartments.annotate(
            search=SearchVector('country__name') + SearchVector('city__name') + SearchVector('description')
        ).filter(search__icontains=text)
    if square_area:
        apartments = apartments.filter(square_area__gte=int(square_area))
    if daily_rate:
        apartments = apartments.filter(daily_rate__lte=daily_rate)
    if room_amount != 0:
        apartments = apartments.filter(room_amount__gte=room_amount)
        apartments = apartments.filter(bedroom_amount__gte=bedroom_amount)
    if convenience_items:
        apartments = apartments.filter(convenience_items__contains=convenience_items)
    if rating != 0:
        apartments = apartments.filter(average_rating__gte=rating)
    if location:
        query_point = format_coord_string_to_point(query_str=location)
        apartments = apartments.annotate(distance=Distance('location', query_point)).order_by('-distance')
    apartments = apartments.prefetch_related('apartmentphoto_set').select_related('country', 'city')
    return apartments


def format_coord_string_to_point(query_str):
    lat_lng = query_str.split(',')
    x = float(lat_lng[1])
    y = float(lat_lng[0])
    location = Point(x=x, y=y, srid=4326)
    return location


def get_bookings_page(request, bookings):
    paginator = Paginator(bookings, 20)
    page_number = request.GET.get('page')
    bookings_page = paginator.get_page(page_number)
    return bookings_page
