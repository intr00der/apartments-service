from django.urls import path

from .views import booking_chat

urlpatterns = [
    path('chat/<booking_id>', booking_chat, name='booking-chat')
]
