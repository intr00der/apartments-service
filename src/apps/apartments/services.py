from django.contrib.auth import get_user_model

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

def search_by_query(request):
    pass