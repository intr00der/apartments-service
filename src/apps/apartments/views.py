from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ApartmentForm, ApartmentFilteringForm
from .models import Apartment
from .services import create_apartment_by_form, verify_apartment


@login_required
def home(request):
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

        # if request.GET.get:
        # apartments = search_by_query(request)

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
        return render(request, 'apartments/home.html', {'apartments': apartments, 'form': form})
    print(form.errors)

    return render(request, 'apartments/home.html', {'apartments': apartments, 'form': form})


@login_required
def register_apartment(request):
    form = ApartmentForm(request.POST, request.FILES)
    if form.is_valid():
        create_apartment_by_form(request, form)
        return redirect('home')
    return render(request, 'apartments/apartment_register.html', {'form': form})


@login_required
def unverified_apartment_list(request):
    if request.method == 'GET':
        if request.user.is_superuser:
            apartments = Apartment.objects.filter(is_verified=False)
            return render(request, 'apartments/unverified_list.html', {'apartments': apartments})
        else:
            messages.error(request, "You're not allowed to visit that page.")
            redirect('home')
    return HttpResponse(status=500)


@login_required
def apartment_detail(request, apartment_pk):
    try:
        apartment = Apartment.objects.get(pk=apartment_pk)
        if apartment.owner.pk == request.user.pk:
            if request.method == 'POST':
                form = ApartmentForm(request.POST, instance=apartment)
                if form.is_valid():
                    form.save()
                    redirect('apartment-detail', {'form': form})
            else:
                form = ApartmentForm(instance=apartment)
            return render(request, 'apartments/apartment-form-profile.html', {'form':form})
        else:
            return render(request, 'apartments/apartment_detail.html', {'apartment': apartment})
    except Apartment.DoesNotExist:
        messages.error(request, 'Such apartment does not exist.')
        return redirect('home')


@login_required
def verify(request, apartment_pk):
    if request.method == 'GET':
        if request.user.is_superuser:
            verify_apartment(apartment_pk)
            messages.success(request, 'Apartment was verified successfully!')
            return redirect('unverified-list')
    return HttpResponse(status=500)


@login_required
def profile_apartment_list(request):
    if request.method == 'GET':
        apartments = Apartment.objects.filter(owner_id=request.user.pk)
        return render(request, 'apartments/users_apartment_list.html', {'apartments': apartments})
    return HttpResponse(status=500)
