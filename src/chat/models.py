from django.db import models
from users.models import User
from apartments.models import Booking


class BookingMessage(models.Model):
    booking = models.ForeignKey(Booking, related_name='booking_messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_booking_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_booking_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
