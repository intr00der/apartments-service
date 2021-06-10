from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Q
from django.shortcuts import render, redirect

import json

from .forms import (
    ApartmentForm,
    ApartmentFilteringForm,
    BookingForm,
    ReviewForm, PhotoForm,
)
from .models import Apartment, Booking, ApartmentPhoto
from .services import (
    verify_apartment,
    get_booked_days,
    can_review,
    get_bookings_page,
    get_apartments_page,
)
from users.services import verified_only


@login_required
def home(request):
    form = ApartmentFilteringForm(request.POST)
    page = get_apartments_page(form, request)
    return render(request, 'apartments/home.html', {'page': page, 'form': form})


@login_required
@verified_only
def register_apartment(request):
    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES, owner=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Apartment registered successfully! Now it's on the inspection.")
            return redirect('home')
    else:
        form = ApartmentForm()
    return render(request, 'apartments/apartment_register.html', {'form': form})


@login_required
@verified_only
def unverified_apartment_list(request):
    if request.user.is_superuser:
        apartments = Apartment.objects.filter(is_verified=False)
        return render(request, 'apartments/unverified_list.html', {'apartments': apartments})
    else:
        messages.error(request, "You're not allowed to visit that page.")
        return redirect('home')


@login_required
@verified_only
def apartment_detail(request, apartment_pk):
    try:
        apartment = Apartment.objects.get(pk=apartment_pk)
    except Apartment.DoesNotExist:
        messages.error(request, 'Such apartment does not exist.')
        return redirect('home')

    if apartment.owner.pk == request.user.pk:
        if request.method == 'POST':
            form = ApartmentForm(request.POST, request.FILES, instance=apartment)
            if form.is_valid():
                form.save()
                messages.success(request, 'Changes made successfully!')
        else:
            form = ApartmentForm(instance=apartment)

        photos = ApartmentPhoto.objects.filter(apartment=apartment).order_by('position')
        context = {'form': form, 'photos': photos, 'apartment_pk': apartment_pk}
        return render(request, 'apartments/apartment-form-profile.html', context)
    photos = ApartmentPhoto.objects.filter(apartment=apartment).order_by('position')
    return render(request, 'apartments/apartment_detail.html', {'apartment': apartment, 'photos': photos})


@login_required
@verified_only
def photo_detail(request, apartment_pk, photo_pk):
    try:
        photo = ApartmentPhoto.objects.select_related('apartment').get(apartment_id=apartment_pk, pk=photo_pk)
    except ApartmentPhoto.DoesNotExist:
        messages.error(request, 'Such photo does not exist')
        return redirect('home')
    if request.user.id == photo.apartment.owner_id:
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES, instance=photo, apartment_pk=apartment_pk)
            if form.is_valid():
                form.save()
                messages.success(request, 'Photo saved successfully!')
                return redirect('apartment-detail', apartment_pk)
        else:
            form = PhotoForm(instance=photo)
        return render(request, 'apartments/photo_detail.html', {'photo': photo, 'form': form})
    messages.error(request, "You can't choose photos for the apartment which you don't own.")
    return redirect('home')


@login_required
@verified_only
def add_photo(request, apartment_pk):
    try:
        apartment = Apartment.objects.get(pk=apartment_pk)
    except Apartment.DoesNotExist:
        messages.error(request, 'Such apartment does not exist.')
        return redirect('home')

    if request.user.id == apartment.owner_id:
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES, apartment_pk=apartment_pk)
            if form.is_valid():
                form.save()
                messages.success(request, 'Photo saved successfully!')
                return redirect('apartment-detail', apartment_pk)
        else:
            form = PhotoForm()
        return render(request, 'apartments/photo_detail.html', {'form': form})
    messages.error(request, "You can't choose photos for the apartment which you don't own.")
    return redirect('home')


@login_required
@verified_only
def verify(request, apartment_pk):
    if request.user.is_superuser:
        try:
            verify_apartment(apartment_pk)
            messages.success(request, 'Apartment was verified successfully!')
        except Apartment.DoesNotExist:
            messages.error(request, 'Such apartment does not exist.')
    return redirect('unverified-list')


@login_required
@verified_only
def profile_apartment_list(request):
    apartments = Apartment.objects.filter(owner_id=request.user.pk)
    return render(request, 'apartments/users_apartment_list.html', {'apartments': apartments})


@login_required
@verified_only
def book_apartment(request, apartment_pk):
    try:
        apartment = Apartment.objects.get(pk=apartment_pk)
    except Apartment.DoesNotExist:
        messages.error(request, 'Such apartment does not exist.')
        return redirect('home')

    booked_days = get_booked_days(apartment)
    booked_days_json = json.dumps(booked_days, cls=DjangoJSONEncoder)
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user, apartment=apartment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully booked!')
            return redirect('home')
    else:
        form = BookingForm()
    context = {'apartment': apartment, 'form': form, 'booked_days': booked_days_json}
    return render(request, 'apartments/book_apartment.html', context)


@login_required
@verified_only
def bookings_list(request):
    bookings = Booking.objects.filter(
        user=request.user).annotate(
        unread_messages=Count('booking_messages',
                              filter=Q(booking_messages__receiver=request.user, booking_messages__read=False))) \
        .order_by('unread_messages')
    page = get_bookings_page(request, bookings)
    return render(request, 'apartments/booking_list.html', {'page': page})


@login_required
@verified_only
def post_review(request, apartment_pk):
    try:
        apartment = Apartment.objects.get(pk=apartment_pk)
    except Apartment.DoesNotExist:
        messages.error(request, 'Such apartment does not exist.')
        return redirect('home')

    user = request.user
    user_can_review, error_msg = can_review(user, apartment)
    if user_can_review:
        if request.method == 'POST':
            form = ReviewForm(request.POST, user=user, apartment=apartment)
            if form.is_valid():
                form.save()
                messages.success(request, 'Review created successfully!')
                return redirect('apartment-detail', apartment_pk)
        else:
            form = ReviewForm()
        return render(request, 'apartments/review.html', {'apartment': apartment, 'form': form})
    messages.warning(request, error_msg)
    return redirect('home')


@login_required
@verified_only
def apartment_bound_bookings(request, apartment_pk):
    apartment = Apartment.objects.get(pk=apartment_pk)
    if request.user.id != apartment.owner_id:
        messages.error(request, "You're not allowed to see the bookings on an apartment which doesn't belong to you.")
        return redirect('home')

    bookings = Booking.objects.filter(
        apartment_id=apartment_pk).annotate(
        unread_messages=Count('booking_messages',
                              filter=Q(booking_messages__receiver=request.user, booking_messages__read=False))) \
        .order_by('unread_messages')
    page = get_bookings_page(request, bookings)
    context = {'apartment': apartment, 'page': page}
    return render(request, 'apartments/apartment_bound_bookings.html', context)
