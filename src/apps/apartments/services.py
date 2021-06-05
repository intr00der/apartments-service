import json

from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db.models import When, Case, Prefetch

from .models import Apartment, Booking, ApartmentPhoto

from datetime import (
    timedelta,
    datetime
)
from pyproj import Proj, transform
from math import sin, cos, sqrt, atan2, radians


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
    if user == apartment.owner:
        return False, "You can't leave a review on your own apartment."
    if not Booking.objects.filter(apartment=apartment, user=user):
        return False, "You can't leave a review on an apartment which you've never visited."
    return True, None


def filter_apartments_by_query(form, request):
    apartments = Apartment.objects.filter(is_verified=True)
    text_query = request.POST.get('search_bar')
    daily_rate_query = request.POST.get('daily_rate')
    square_area_query = request.POST.get('square_area')
    room_amount_query = request.POST.get('room_amount')
    bedroom_amount_query = request.POST.get('bedroom_amount')
    convenience_item_query = request.POST.getlist('convenience_items')
    rating_query = request.POST.get('rating')
    location_query = request.POST.get('location')

    if not square_area_query:
        square_area_query = 0
    if not room_amount_query:
        room_amount_query = 0
    if not rating_query:
        rating_query = 0
    if form.is_valid():
        form.save(commit=False)

        if text_query:
            apartments = apartments.annotate(
                search=SearchVector('country__name') + SearchVector('city__name') + SearchVector('description')
            ).filter(search__icontains=text_query)
        if square_area_query:
            apartments = apartments.filter(square_area__gte=int(square_area_query))
        if daily_rate_query:
            apartments = apartments.filter(daily_rate__lte=daily_rate_query)
        if room_amount_query != 0:
            apartments = apartments.filter(room_amount__gte=room_amount_query)
            apartments = apartments.filter(bedroom_amount__gte=bedroom_amount_query)
        if convenience_item_query:
            apartments = apartments.filter(convenience_items__contains=convenience_item_query)
        if rating_query != 0:
            apartments = apartments.filter(average_rating__gte=rating_query)
        if location_query:
            lat1, lng1 = format_coordinates_to_lng_lat(query_str=location_query)
            coord_dict = dict()
            for apartment in apartments:
                lat2_lng2 = apartment.lat_lng
                coord_dict[apartment.pk] = calculate_distance(lat1, lng1, lat2_lng2[0], lat2_lng2[1])
            whens = [When(pk=k, then=v) for k, v in coord_dict.items()]
            apartments = apartments.annotate(distance=Case(*whens)).order_by('-distance')
        # apartments = apartments.prefetch_related(
        #     Prefetch(
        #         'photos', queryset=ApartmentPhoto.objects.filter()
        #     )
        # )
        apartments = apartments.prefetch_related('photos')
    return apartments


def format_coordinates_to_lng_lat(query_str):
    query_dict = json.loads(query_str)
    input_formatter = Proj('epsg:3857')
    output_formatter = Proj('epsg:4326')
    x, y = query_dict['coordinates'][0], query_dict['coordinates'][1]
    lat, lng = transform(input_formatter, output_formatter, x, y)
    return lat, lng


def calculate_distance(lat1, lng1, lat2, lng2):
    earth_radius = 6378.137
    lat1 = radians(lat1)
    lon1 = radians(lng1)
    lat2 = radians(lat2)
    lon2 = radians(lng2)
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = round(earth_radius * c, 1)
    return distance


def get_apartments_page(form, request):
    apartments = filter_apartments_by_query(form, request)
    paginator = Paginator(apartments, 20)
    page_number = request.GET.get('page')
    apartments_page = paginator.get_page(page_number)
    return apartments_page


def get_bookings_page(request, bookings):
    paginator = Paginator(bookings, 20)
    page_number = request.GET.get('page')
    bookings_page = paginator.get_page(page_number)
    return bookings_page
