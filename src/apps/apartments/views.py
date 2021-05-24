from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ApartmentForm
from .models import Apartment
from .services import (
    create_apartment_by_form,
    verify_apartment,
    filter_apartments_by_query,
)


@login_required
def home(request):
    apartments, form = filter_apartments_by_query(request)
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
