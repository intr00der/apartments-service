from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector

from .forms import ApartmentFilteringForm
from .models import Apartment, Country, City

User = get_user_model()


def create_apartment_by_form(request, form):
    owner_id = request.user.pk
    country_id = Country.objects.get(name=form.cleaned_data.get('country')).id
    city_id = City.objects.get(name=form.cleaned_data.get('city')).id
    description = form.cleaned_data.get('description')
    square_area = form.cleaned_data.get('square_area')
    room_amount = form.cleaned_data.get('room_amount')
    bedroom_amount = form.cleaned_data.get('bedroom_amount')
    daily_rate = form.cleaned_data.get('daily_rate')
    registry_ordering = form.cleaned_data.get('registry_ordering')
    convenience_items = form.cleaned_data.get('convenience_items')

    Apartment.objects.create(
        owner_id=owner_id,
        country_id=country_id,
        city_id=city_id,
        description=description,
        square_area=square_area,
        room_amount=room_amount,
        bedroom_amount=bedroom_amount,
        daily_rate=daily_rate,
        registry_ordering=registry_ordering,
        convenience_items=convenience_items,
    )


def verify_apartment(apartment_pk):
    apartment = Apartment.objects.get(id=apartment_pk)
    apartment.is_verified = True
    apartment.save()

def filter_apartments_by_query(request):
    apartments = Apartment.objects.filter(is_verified=True)
    form = ApartmentFilteringForm(request.POST)

    text_query = request.POST.get('search_bar')
    daily_rate_query = request.POST.get('daily_rate')
    square_area_query = request.POST.get('square_area')
    room_amount_query = request.POST.get('room_amount')
    bedroom_amount_query = request.POST.get('bedroom_amount')
    convenience_item_query = request.POST.getlist('convenience_items')

    if not square_area_query:
        square_area_query = 0
    if not room_amount_query:
        room_amount_query = 0
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
        return apartments, form