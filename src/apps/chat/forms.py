from django import forms

from .models import BookingMessage
from .services import set_receiver


class BookingMessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop('sender', [])
        self.booking = kwargs.pop('booking', [])
        self.receiver = None
        self.is_seen_by_client = False
        self.is_seen_by_owner = False
        return super().__init__(*args, **kwargs)

    class Meta:
        model = BookingMessage
        fields = ['text']

    def clean(self):
        set_receiver(self)
        return super().clean()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.sender = self.sender
        instance.receiver = self.receiver
        instance.booking = self.booking
        instance.is_seen_by_client = self.is_seen_by_client
        instance.is_seen_by_owner = self.is_seen_by_owner
        if commit:
            instance.save()
