def set_receiver(form):
    if form.sender == form.booking.apartment.owner:
        form.receiver = form.booking.user
    else:
        form.receiver = form.booking.apartment.owner
