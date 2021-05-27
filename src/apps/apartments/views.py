from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import (
    ApartmentForm,
    ApartmentFilteringForm,
    BookingForm,
    ReviewForm,
)
from .models import Apartment, Booking
from .services import (
    verify_apartment,
    get_booked_days,
    get_formatted_date_list,
    can_review,
)


@login_required
def home(request):
    form = ApartmentFilteringForm(request.POST)
    apartments = form.filter_apartments_by_query(request)
    return render(request, 'apartments/home.html', {'apartments': apartments, 'form': form})


@login_required
def register_apartment(request):
    user = request.user
    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            form.create_apartment_by_form()
            messages.success(request, "Apartment registered successfully! Now it's on the inspection.")
            return redirect('home')
    else:
        form = ApartmentForm()
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
                form = ApartmentForm(request.POST, request.FILES, instance=apartment)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Changes made successfully!')
                    redirect('apartment-detail', {'form': form})
            else:
                form = ApartmentForm(instance=apartment)
            return render(request, 'apartments/apartment-form-profile.html', {'form': form})
        else:
            return render(request, 'apartments/apartment_detail.html', {'apartment': apartment})
    except Apartment.DoesNotExist:
        messages.error(request, 'Such apartment does not exist.')
        return redirect('home')


@login_required
def verify(request, apartment_pk):
    try:
        if request.method == 'GET':
            if request.user.is_superuser:
                verify_apartment(apartment_pk)
                messages.success(request, 'Apartment was verified successfully!')
                return redirect('unverified-list')
        return HttpResponse(status=500)
    except Apartment.DoesNotExist:
        messages.error(request, 'Such apartment does not exist.')
        return redirect('home')


@login_required
def profile_apartment_list(request):
    if request.method == 'GET':
        apartments = Apartment.objects.filter(owner_id=request.user.pk)
        return render(request, 'apartments/users_apartment_list.html', {'apartments': apartments})
    return HttpResponse(status=500)


@login_required
def book_apartment(request, apartment_pk):
    try:
        apartment = Apartment.objects.get(pk=apartment_pk)
        user = request.user
        apartment.booked_days = get_formatted_date_list(get_booked_days(apartment))
        if request.method == 'POST':
            form = BookingForm(request.POST, user=user, apartment=apartment)
            if form.is_valid():
                form.create_booking_by_form()
                messages.success(request, 'Successfully booked!')
                return redirect('home')
        else:
            form = BookingForm()
        return render(request, 'apartments/book_apartment.html', {'apartment': apartment, 'form': form})
    except Apartment.DoesNotExist:
        messages.error(request, 'Such apartment does not exist.')
        return redirect('home')


def bookings_list(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    return render(request, 'apartments/booking_list.html', {'bookings': bookings})


def post_review(request, apartment_pk):
    try:
        user = request.user
        apartment = Apartment.objects.get(pk=apartment_pk)
        user_can_review, error_msg = can_review(user, apartment)
        if user_can_review:
            if request.method == 'POST':
                form = ReviewForm(request.POST, user=user, apartment=apartment)
                if form.is_valid():
                    form.create_review_by_form()
                    messages.success(request, 'Review created successfully!')
                    return redirect('apartment-detail', apartment_pk)
            else:
                form = ReviewForm()
            return render(request, 'apartments/review.html', {'apartment': apartment, 'form': form})
        messages.warning(request, error_msg)
        return redirect('home')
    except Apartment.DoesNotExist:
        messages.error(request, 'Such apartment does not exist.')
        return redirect('home')
