from django import forms
from django.contrib.postgres.search import SearchVector

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

    def create_apartment_by_form(self):
        owner_id = self.user.pk
        country_id = Country.objects.get(name=self.cleaned_data.get('country')).id
        city_id = City.objects.get(name=self.cleaned_data.get('city')).id
        description = self.cleaned_data.get('description')
        square_area = self.cleaned_data.get('square_area')
        room_amount = self.cleaned_data.get('room_amount')
        bedroom_amount = self.cleaned_data.get('bedroom_amount')
        daily_rate = self.cleaned_data.get('daily_rate')
        registry_ordering = self.cleaned_data.get('registry_ordering')
        convenience_items = self.cleaned_data.get('convenience_items')
        opens_at = self.cleaned_data.get('opens_at')
        closes_at = self.cleaned_data.get('closes_at')

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
            opens_at=opens_at,
            closes_at=closes_at
        )

    def compare_room_and_bedroom_amounts(self, *args, **kwargs):
        room_amount = self.cleaned_data.get('room_amount')
        bedroom_amount = self.cleaned_data.get('bedroom_amount')
        if room_amount and bedroom_amount:
            if bedroom_amount > room_amount:
                raise forms.ValidationError(
                    {'bedroom_amount': ["It's not possible to have more bedrooms than rooms overall."]})

    def compare_opening_and_closing_dates(self, *args, **kwargs):
        opens_at = self.cleaned_data.get('opens_at')
        closes_at = self.cleaned_data.get('closes_at')
        if closes_at < opens_at:
            raise forms.ValidationError(
                {'closes_at': ["It's not possible to set the closing date earlier than the opening date."]})

    def clean(self, *args, **kwargs):
        self.compare_room_and_bedroom_amounts(self)
        self.compare_opening_and_closing_dates(self)
        return super().clean(*args, **kwargs)


class ApartmentFilteringForm(forms.ModelForm):
    amount_choices = Apartment.Amount.choices
    amount_choices[0] = (0, 'any amount')

    rating_choices = amount_choices
    rating_choices[0] = (0, 'any rating')

    search_bar = forms.CharField(required=False, label='Search by country, city, description')
    room_amount = forms.ChoiceField(required=False, choices=amount_choices)
    bedroom_amount = forms.ChoiceField(required=False, choices=amount_choices)
    daily_rate = forms.IntegerField(required=False)
    square_area = forms.IntegerField(required=False)
    convenience_items = forms.MultipleChoiceField(choices=Apartment.ConvenienceItems.choices,
                                                  widget=forms.CheckboxSelectMultiple, required=False)
    rating = forms.ChoiceField(required=False, choices=rating_choices)

    class Meta:
        model = Apartment
        fields = ('square_area', 'room_amount', 'bedroom_amount', 'daily_rate', 'convenience_items')

    def filter_apartments_by_query(self, request):
        apartments = Apartment.objects.filter(is_verified=True)
        text_query = request.POST.get('search_bar')
        daily_rate_query = request.POST.get('daily_rate')
        square_area_query = request.POST.get('square_area')
        room_amount_query = request.POST.get('room_amount')
        bedroom_amount_query = request.POST.get('bedroom_amount')
        convenience_item_query = request.POST.getlist('convenience_items')
        rating_query = request.POST.get('rating')

        if not square_area_query:
            square_area_query = 0
        if not room_amount_query:
            room_amount_query = 0
        if not rating_query:
            rating_query = 0
        if self.is_valid():
            self.save(commit=False)

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
            return apartments

    def compare_room_and_bedroom_amounts(self, *args, **kwargs):
        room_amount = self.cleaned_data.get('room_amount')
        bedroom_amount = self.cleaned_data.get('bedroom_amount')
        if room_amount and bedroom_amount:
            if bedroom_amount > room_amount:
                raise forms.ValidationError(
                    {'bedroom_amount': ["It's not possible to have more bedrooms than rooms overall."]})

    def clean(self, *args, **kwargs):
        self.compare_room_and_bedroom_amounts(self)
        return super().clean(*args, **kwargs)


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

    def create_booking_by_form(self):
        user = self.user
        apartment = self.apartment
        starts_at = self.cleaned_data.get('starts_at')
        ends_at = self.cleaned_data.get('ends_at')

        Booking.objects.create(
            user=user,
            apartment=apartment,
            starts_at=starts_at,
            ends_at=ends_at
        )

    def validate_booking_dates(self, *args, **kwargs):
        apartment_opens_at = self.apartment.opens_at
        apartment_closes_at = self.apartment.closes_at
        requested_start_date = parse_date_string(self.data.get('starts_at'))
        requested_end_date = parse_date_string(self.data.get('ends_at'))

        if requested_start_date > requested_end_date:
            raise forms.ValidationError({'ends_at': ["Starting date can't be later than ending date."]})
        if requested_start_date < apartment_opens_at:
            raise forms.ValidationError({'starts_at': ["Can't book an apartment before it's open."]})
        if requested_end_date > apartment_closes_at:
            raise forms.ValidationError({'ends_at': ["Can't book an apartment after it's closed."]})

        crossed_bookings = Booking.objects.filter(
            apartment_id=self.apartment.pk).filter(
            starts_at__range=[requested_start_date, requested_end_date]).filter(
            ends_at__range=[requested_start_date, requested_end_date])
        if crossed_bookings:
            raise forms.ValidationError(
                {'starts_at': ['Some or all dates the from chosen date interval are already booked']})

    def clean(self, *args, **kwargs):
        self.validate_booking_dates(self)
        return super().clean(*args, **kwargs)


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', [])
        self.apartment = kwargs.pop('apartment', [])
        return super().__init__(*args, **kwargs)

    class Meta:
        model = Review
        fields = ['heading', 'text', 'rating']

    def create_review_by_form(self):
        Review.objects.create(
            user=self.user,
            apartment=self.apartment,
            heading=self.cleaned_data.get('heading'),
            text=self.cleaned_data.get('text'),
            rating=self.cleaned_data.get('rating')
        )


