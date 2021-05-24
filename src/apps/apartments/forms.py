from django import forms

from .models import Apartment


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = (
            'country', 'city', 'description', 'square_area', 'room_amount',
            'bedroom_amount', 'daily_rate', 'registry_ordering', 'convenience_items',
        )

    def compare_room_and_bedroom_amounts(self, *args, **kwargs):
        room_amount = self.cleaned_data.get('room_amount')
        bedroom_amount = self.cleaned_data.get('bedroom_amount')
        if room_amount and bedroom_amount:
            if bedroom_amount > room_amount:
                error_hint = "It's not possible to have more bedrooms than rooms overall."
                self.add_error(field='bedroom_amount', error=error_hint)

    def clean(self, *args, **kwargs):
        self.compare_room_and_bedroom_amounts(self)
        return super().clean(*args, **kwargs)


class ApartmentFilteringForm(forms.ModelForm):
    apartment_choices = Apartment.Amount.choices
    apartment_choices[0] = (0, 'any amount')

    search_bar = forms.CharField(required=False, label='Search by country, city, description')
    room_amount = forms.ChoiceField(required=False, choices=apartment_choices)
    bedroom_amount = forms.ChoiceField(required=False, choices=apartment_choices)
    daily_rate = forms.IntegerField(required=False)
    square_area = forms.IntegerField(required=False)
    convenience_items = forms.MultipleChoiceField(choices=Apartment.ConvenienceItems.choices, widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Apartment
        fields = ('square_area', 'room_amount', 'bedroom_amount', 'daily_rate', 'convenience_items')

    def compare_room_and_bedroom_amounts(self, *args, **kwargs):
        room_amount = self.cleaned_data.get('room_amount')
        bedroom_amount = self.cleaned_data.get('bedroom_amount')
        if room_amount and bedroom_amount:
            if bedroom_amount > room_amount:
                error_hint = "It's not possible to have more bedrooms than rooms overall."
                self.add_error(field='bedroom_amount', error=error_hint)

    def clean(self, *args, **kwargs):
        self.compare_room_and_bedroom_amounts(self)
        return super().clean(*args, **kwargs)
