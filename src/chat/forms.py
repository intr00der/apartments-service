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

    def save_message_with_added_data(self):
        form_instance = self.save(commit=False)
        form_instance.sender = self.sender
        form_instance.receiver = self.receiver
        form_instance.booking = self.booking
        form_instance.is_seen_by_client = self.is_seen_by_client
        form_instance.is_seen_by_owner = self.is_seen_by_owner
        form_instance.save()
