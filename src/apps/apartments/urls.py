from django.urls import path
from .views import current_datetime

urlpatterns = [
    path('', current_datetime)
]