from django import forms
from django.db import models
from django.contrib.postgres.search import SearchVector
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import Apartment, Booking, Review, Country, City

from .services import parse_date_string


class ApartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', [])
        super().__init__(*args, **kwargs)

    class Meta:
        model = Apartment
        fields = (
            'country', 'city', 'description',
            'square_area', 'room_amount', 'bedroom_amount',
            'daily_rate', 'registry_ordering', 'convenience_items',
            'opens_at', 'closes_at'
        )

        widgets = {
            'opens_at': forms.TextInput(attrs={'class': 'genericDatepicker'}),
            'closes_at': forms.TextInput(attrs={'class': 'genericDatepicker'}),
        }

    def save_apartment_with_added_data(self):
        form_instance = self.save(commit=False)
        form_instance.owner = self.user
        form_instance.save()

    def compare_room_and_bedroom_amounts(self):
        room_amount = self.cleaned_data['room_amount']
        bedroom_amount = self.cleaned_data['bedroom_amount']
        if room_amount and bedroom_amount:
            if bedroom_amount > room_amount:
                raise forms.ValidationError({
                    'bedroom_amount': "It's not possible to have more bedrooms than rooms overall."
                })

    def compare_opening_and_closing_dates(self):
        opens_at = self.cleaned_data['opens_at']
        closes_at = self.cleaned_data['closes_at']
        if closes_at < opens_at:
            raise forms.ValidationError({
                'closes_at': "It's not possible to set the closing date earlier than the opening date."
            })

    def clean(self):
        self.compare_room_and_bedroom_amounts()
        self.compare_opening_and_closing_dates()
        return super().clean()


class ApartmentFilteringForm(forms.ModelForm):
    class AmountChoices(models.IntegerChoices):
        NULL = 0, _('Any amount')
        ONE = 1, _('One')
        TWO = 2, _('Two')
        THREE = 3, _('Three')
        FOUR = 4, _('Four')
        FIVE = 5, _('More than four')

    search_bar = forms.CharField(required=False, label='Search by country, city, description...')
    room_amount = forms.ChoiceField(required=False, choices=AmountChoices.choices)
    bedroom_amount = forms.ChoiceField(required=False, choices=AmountChoices.choices)
    daily_rate = forms.IntegerField(required=False)
    square_area = forms.IntegerField(required=False)
    convenience_items = forms.MultipleChoiceField(choices=Apartment.ConvenienceItems.choices,
                                                  widget=forms.CheckboxSelectMultiple, required=False)
    rating = forms.IntegerField(required=False, validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        model = Apartment
        fields = ('square_area', 'room_amount', 'bedroom_amount', 'daily_rate', 'convenience_items')

    def compare_room_and_bedroom_amounts(self, *args, **kwargs):
        room_amount = self.cleaned_data['room_amount']
        bedroom_amount = self.cleaned_data['bedroom_amount']
        if room_amount and bedroom_amount:
            if bedroom_amount > room_amount:
                raise forms.ValidationError({
                    'bedroom_amount': "It's not possible to have more bedrooms than rooms overall.",
                })

    def clean(self):
        self.compare_room_and_bedroom_amounts()
        return super().clean()


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', [])
        self.apartment = kwargs.pop('apartment', [])
        return super().__init__(*args, **kwargs)

    class Meta:
        model = Booking
        fields = ['starts_at', 'ends_at']
        widgets = {
            'starts_at': forms.TextInput(attrs={'class': 'bookingDatepicker'}),
            'ends_at': forms.TextInput(attrs={'class': 'bookingDatepicker'}),
        }

    def save_booking_with_added_data(self):
        form_instance = self.save(commit=False)
        form_instance.user = self.user
        form_instance.apartment = self.apartment
        form_instance.save()

    def validate_booking_dates(self):
        apartment_opens_at = self.apartment.opens_at
        apartment_closes_at = self.apartment.closes_at
        requested_start_date = parse_date_string(self.data['starts_at'])
        requested_end_date = parse_date_string(self.data['ends_at'])

        if requested_start_date > requested_end_date:
            raise forms.ValidationError({'ends_at': "Starting date can't be later than ending date."})
        if requested_start_date < apartment_opens_at:
            raise forms.ValidationError({'starts_at': "Can't book an apartment before it's open."})
        if requested_end_date > apartment_closes_at:
            raise forms.ValidationError({'ends_at': "Can't book an apartment after it's closed."})

        crossed_bookings = Booking.objects.filter(
            apartment_id=self.apartment.pk).filter(
            starts_at__range=[requested_start_date, requested_end_date]).filter(
            ends_at__range=[requested_start_date, requested_end_date])
        if crossed_bookings:
            raise forms.ValidationError({
                'starts_at': 'Some or all dates from the chosen date interval are already booked.'
            })

    def clean(self):
        self.validate_booking_dates()
        return super().clean()


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', [])
        self.apartment = kwargs.pop('apartment', [])
        return super().__init__(*args, **kwargs)

    class Meta:
        model = Review
        fields = ['heading', 'text', 'rating']

    def save_review_with_added_data(self):
        form_instance = self.save(commit=False)
        form_instance.user = self.user
        form_instance.apartment = self.apartment
        form_instance.save()
