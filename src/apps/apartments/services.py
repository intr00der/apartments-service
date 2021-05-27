from django.contrib.auth import get_user_model
from django.utils.dateformat import format

from .models import Apartment, Booking

from datetime import timedelta, date

User = get_user_model()


def verify_apartment(apartment_pk):
    apartment = Apartment.objects.get(id=apartment_pk)
    apartment.is_verified = True
    apartment.save()


def calculate_timedelta(apartment):
    open_timedelta = (apartment.closes_at - apartment.opens_at).days
    default_timedelta = timedelta(days=60).days
    if open_timedelta > default_timedelta:
        return default_timedelta
    return open_timedelta


def parse_date_string(date_str):
    date_lst = date_str.split('.')
    day = int(date_lst[0])
    month = int(date_lst[1])
    year = int(date_lst[2])
    return date(day=day, month=month, year=year)


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
        booked_days += [start + timedelta(days=x) for x in range(0, (end - start).days)]
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


def get_formatted_date_list(date_list):
    formatted_date_list = []
    for dt in date_list:
        formatted_date_list.append(format(dt, 'd.m.Y'))
    return formatted_date_list


def can_review(user, apartment):
    if user == apartment.owner:
        return False, "You can't leave a review on your own apartment."
    if not Booking.objects.filter(apartment=apartment, user=user):
        return False, "You can't leave a review on an apartment which you've never visited."
    return True, None
