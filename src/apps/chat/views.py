from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apartments.models import Booking
from .models import BookingMessage
from .forms import BookingMessageForm


def booking_chat(request, booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
    except Booking.DoesNotExist:
        messages.error(request, 'The booking does not exist.')
        return redirect('home')

    if request.user != booking.user and request.user != booking.apartment.owner:
        messages.error(request, "You're not allowed to participate in the chat of someone else's booking!")
        return redirect('bookings-list')

    booking_messages = BookingMessage.objects.filter(booking_id=booking_id)
    booking_messages.filter(receiver=request.user).update(read=True)

    if request.method == 'POST':
        form = BookingMessageForm(request.POST, sender=request.user, booking=booking)
        if form.is_valid():
            form.save()
            return redirect('booking-chat', booking_id)
    else:
        form = BookingMessageForm()
    return render(request, 'chat/booking_chat.html', {'booking_messages': booking_messages, 'form': form})
